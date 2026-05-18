from __future__ import annotations

import json
import shutil
from pathlib import Path

from packager.dbpf import ResourceKey, patch_package_texture, patch_package_textures
from packager.dds_convert import png_to_dds
from packager.png_util import load_png_rgba, resize_cover_rgba, solid_png

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
    if input_path.suffix.lower() != ".png":
        tmp = input_path.parent / "_converted.png"
        to_png(input_path, tmp)
        src = tmp
    w, h, pixels = load_png_rgba(str(src))
    out = resize_cover_rgba(w, h, pixels, width, height)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(encode_png_rgba(width, height, out))


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

    def key_from_instance(inst_hex: str) -> ResourceKey:
        inst = parse_hex_int(inst_hex)
        return ResourceKey(
            type_id=type_id,
            group_id=group_id,
            instance_high=(inst >> 32) & 0xFFFFFFFF,
            instance_low=inst & 0xFFFFFFFF,
        )

    targets: list[ResourceKey] = []
    if tpl.get("textureInstances"):
        targets = [key_from_instance(h) for h in tpl["textureInstances"]]
    else:
        targets = [key_from_instance(res["instance"])]

    texture_format = tpl.get("textureFormat", "png").lower()
    if texture_format == "dds":
        texture_bytes = png_to_dds(texture_path, width, height)
    else:
        texture_bytes = texture_path.read_bytes()

    out_pkg = settings.outputs_dir / job_id / f"{template_id}_{job_id[:8]}.package"
    out_pkg.parent.mkdir(parents=True, exist_ok=True)
    if len(targets) == 1:
        patch_package_texture(base_pkg, out_pkg, targets[0], texture_bytes)
    else:
        patch_package_textures(base_pkg, out_pkg, targets, texture_bytes)

    guide_src = settings.templates_dir / "install_guides" / f"{tpl['installGuideId']}.md"
    if guide_src.exists():
        shutil.copy(guide_src, out_pkg.parent / "INSTALL.md")

    return out_pkg
