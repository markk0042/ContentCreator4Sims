from __future__ import annotations

import json
import shutil
import struct
from pathlib import Path

from packager.dbpf import ResourceKey, parse_package, patch_package_textures_map, dds_dimensions
from packager.dds_convert import png_to_dds, sims4ize_dds
from packager.png_util import load_png_rgba, resize_cover_rgba

from .blender_runner import run_blender_texture
from . import config as settings


def load_manifest() -> dict:
    path = settings.templates_dir / "manifest.json"
    return json.loads(path.read_text(encoding="utf-8"))


def get_template(template_id: str) -> dict:
    manifest = load_manifest()
    for tpl in manifest["templates"]:
        if tpl["id"] == template_id:
            return tpl
    raise KeyError(f"Unknown template: {template_id}")


def parse_hex_int(value: str) -> int:
    return int(value, 16)


def process_image_fallback(input_path: Path, output_path: Path, width: int, height: int) -> None:
    from packager.image_convert import to_png
    from packager.png_util import encode_png_rgba

    src = input_path
    tmp = input_path.parent / "_converted.png"
    try:
        w, h, pixels = load_png_rgba(str(src))
    except ValueError:
        to_png(input_path, tmp)
        src = tmp
        w, h, pixels = load_png_rgba(str(src))
    out = resize_cover_rgba(w, h, pixels, width, height)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(encode_png_rgba(width, height, out))


def _collect_patch_keys(
    base_pkg: Path,
    tpl: dict,
    type_id: int,
    group_id: int,
) -> list[tuple[ResourceKey, int, int]]:
    """Return (resource key, width, height) for each DDS texture to replace."""
    _, entries = parse_package(base_pkg)
    keys: list[tuple[ResourceKey, int, int]] = []

    allowed_sizes = tpl.get("ddsPatchWidths")

    if tpl.get("patchAllPackageDds"):
        for entry in entries:
            if entry.key.type_id != type_id or entry.key.group_id != group_id:
                continue
            if entry.data[:4] != b"DDS ":
                continue
            w, h = dds_dimensions(entry.data)
            if allowed_sizes and w not in allowed_sizes:
                continue
            keys.append((entry.key, w, h))
        return keys

    res = tpl["textureResource"]
    inst_list = tpl.get("textureInstances") or [res["instance"]]
    for inst_hex in inst_list:
        inst = parse_hex_int(inst_hex)
        key = ResourceKey(
            type_id=type_id,
            group_id=group_id,
            instance_high=(inst >> 32) & 0xFFFFFFFF,
            instance_low=inst & 0xFFFFFFFF,
        )
        for entry in entries:
            if entry.key.matches(key) and entry.data[:4] == b"DDS ":
                w, h = dds_dimensions(entry.data)
                keys.append((key, w, h))
                break
    return keys


def run_conversion(
    *,
    job_id: str,
    template_id: str,
    source_path: Path,
    work_dir: Path,
) -> Path:
    tpl = get_template(template_id)
    width = int(tpl["textureWidth"])
    height = int(tpl["textureHeight"])

    texture_path = work_dir / "diffuse.png"
    scene_file = settings.blender_scenes_dir / tpl["blenderScene"]

    if settings.skip_blender:
        process_image_fallback(source_path, texture_path, width, height)
    else:
        try:
            run_blender_texture(
                scene_file=scene_file,
                input_image=source_path,
                output_texture=texture_path,
                width=width,
                height=height,
                template_id=template_id,
            )
        except (RuntimeError, FileNotFoundError):
            process_image_fallback(source_path, texture_path, width, height)

    base_pkg = settings.templates_dir / tpl["basePackage"]
    if not base_pkg.exists():
        raise FileNotFoundError(
            f"Base package missing: {base_pkg}. Run: python scripts/generate_dev_templates.py"
        )

    res = tpl["textureResource"]
    type_id = parse_hex_int(res["type"])
    group_id = parse_hex_int(res["group"])
    texture_format = tpl.get("textureFormat", "png").lower()

    patch_specs = _collect_patch_keys(base_pkg, tpl, type_id, group_id)
    if not patch_specs:
        raise ValueError(f"No DDS textures found to patch in {base_pkg.name}")

    _, base_entries = parse_package(base_pkg)
    ref_dds_by_key: dict[ResourceKey, bytes] = {}
    for entry in base_entries:
        if entry.key.type_id != type_id or entry.data[:4] != b"DDS ":
            continue
        ref_dds_by_key[entry.key] = entry.data

    raw_dds_by_size: dict[tuple[int, int], bytes] = {}
    key_to_data: dict[ResourceKey, bytes] = {}

    for key, w, h in patch_specs:
        size = (w, h)
        if texture_format == "dds":
            if size not in raw_dds_by_size:
                raw_dds_by_size[size] = png_to_dds(texture_path, w, h)
            ref = ref_dds_by_key.get(key)
            key_to_data[key] = (
                sims4ize_dds(raw_dds_by_size[size], ref)
                if ref is not None
                else sims4ize_dds(raw_dds_by_size[size])
            )
        else:
            from packager.png_util import encode_png_rgba

            w_src, h_src, pixels = load_png_rgba(str(texture_path))
            out = resize_cover_rgba(w_src, h_src, pixels, w, h)
            key_to_data[key] = encode_png_rgba(w, h, out)

    out_pkg = settings.outputs_dir / job_id / f"{template_id}_{job_id[:8]}.package"
    out_pkg.parent.mkdir(parents=True, exist_ok=True)
    replaced = patch_package_textures_map(base_pkg, out_pkg, key_to_data)

    guide_src = settings.templates_dir / "install_guides" / f"{tpl['installGuideId']}.md"
    if guide_src.exists():
        shutil.copy(guide_src, out_pkg.parent / "INSTALL.md")

    if replaced < len(patch_specs):
        raise RuntimeError(f"Only patched {replaced}/{len(patch_specs)} textures")

    return out_pkg
