from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from . import config as settings


def resolve_blender() -> str | None:
    if settings.blender_path and Path(settings.blender_path).exists():
        return settings.blender_path
    found = shutil.which("blender")
    if found:
        return found
    for ver in ("4.4", "4.3", "4.2", "4.1", "4.0", "3.6"):
        p = Path(f"C:/Program Files/Blender Foundation/Blender {ver}/blender.exe")
        if p.exists():
            return str(p)
    return None


def run_blender_texture(
    *,
    scene_file: Path,
    input_image: Path,
    output_texture: Path,
    width: int,
    height: int,
    template_id: str,
) -> None:
    blender = resolve_blender()
    if not blender:
        raise RuntimeError(
            "Blender not found. Install Blender 4.x and set BLENDER_PATH in .env "
            "or add blender to your PATH."
        )

    script = settings.blender_scripts_dir / "process_texture.py"
    if not scene_file.exists():
        raise FileNotFoundError(
            f"Blender scene missing: {scene_file}. Run: python blender/scripts/build_scenes.py"
        )

    cmd = [
        blender,
        str(scene_file),
        "--background",
        "--python",
        str(script),
        "--",
        "--input",
        str(input_image),
        "--output",
        str(output_texture),
        "--width",
        str(width),
        "--height",
        str(height),
        "--template",
        template_id,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Blender failed (code {result.returncode}):\n{result.stderr}\n{result.stdout}"
        )
    if not output_texture.exists():
        raise RuntimeError(f"Blender did not produce output: {output_texture}")
