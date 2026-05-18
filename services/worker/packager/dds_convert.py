"""Convert PNG to DDS (BC3/DXT5) for Sims 4 texture resources."""
from __future__ import annotations

import os
import shutil
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


def png_to_dds(png_path: Path, width: int, height: int) -> bytes:
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
    return dds_files[0].read_bytes()
