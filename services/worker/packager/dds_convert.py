"""Convert PNG to DDS (BC3) for Sims 4 texture resources."""
from __future__ import annotations

import os
import shutil
import struct
import subprocess
from pathlib import Path

# repo root: services/worker/packager -> ../../../ 
_REPO_ROOT = Path(__file__).resolve().parents[3]
_BUNDLED_TEXCONV = _REPO_ROOT / "tools" / "texconv" / "texconv.exe"


def find_texconv() -> str | None:
    env = os.environ.get("TEXCONV_PATH")
    if env and Path(env).exists():
        return env
    if _BUNDLED_TEXCONV.exists():
        return str(_BUNDLED_TEXCONV)
    found = shutil.which("texconv")
    if found:
        return found
    kits = Path(r"C:\Program Files (x86)\Windows Kits\10\bin")
    if kits.exists():
        for texconv in sorted(kits.glob("**/texconv.exe"), reverse=True):
            return str(texconv)
    return None


def sims4ize_dds(dds_bytes: bytes, reference: bytes | None = None) -> bytes:
    """
    Make texconv output compatible with Sims 4 DST5 textures.

    With a reference, keep the template header (per swatch) and replace the full
    mip chain from texconv. Do not mix mip0 from one image with lower mips from
    another — that causes multicolor garbage in-game.
    """
    if dds_bytes[:4] != b"DDS ":
        raise ValueError("Not a DDS file")

    if reference is not None:
        if len(reference) != len(dds_bytes):
            raise ValueError(
                f"DDS size mismatch: generated {len(dds_bytes)} bytes, "
                f"template {len(reference)} bytes"
            )
        if reference[:4] != b"DDS ":
            raise ValueError("Reference is not a DDS file")
        buf = bytearray(reference[:128] + dds_bytes[128:])
    else:
        buf = bytearray(dds_bytes)

    buf[84:88] = b"DST5"
    struct.pack_into("<I", buf, 24, 0)
    return bytes(buf)


def png_to_dds(
    png_path: Path,
    width: int,
    height: int,
    *,
    reference_dds: bytes | None = None,
) -> bytes:
    """BC3_UNORM DDS bytes sized for Sims 4 rug-style textures."""
    texconv = find_texconv()
    if not texconv:
        raise RuntimeError(
            "texconv.exe not found. From the project folder run: npm run install:texconv "
            "(or scripts/install-texconv.ps1), then restart the worker. "
            "Required for DDS templates like the PS Flokati rug."
        )

    out_dir = png_path.parent / "dds_out"
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.dds"):
        old.unlink()

    subprocess.run(
        [
            texconv,
            "-y",
            "-f",
            "BC3_UNORM",
            "-srgbi",
            "-m",
            "10",
            "-w",
            str(width),
            "-h",
            str(height),
            "-o",
            str(out_dir),
            str(png_path),
        ],
        check=True,
        capture_output=True,
    )

    dds_files = list(out_dir.glob("*.dds"))
    if not dds_files:
        raise RuntimeError("texconv did not produce a DDS file")
    return sims4ize_dds(dds_files[0].read_bytes(), reference_dds)
