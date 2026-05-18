"""Convert uploaded images to PNG using Windows System.Drawing when available."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _is_png(data: bytes) -> bool:
    return len(data) >= 8 and data[:8] == b"\x89PNG\r\n\x1a\n"


def to_png(input_path: Path, output_path: Path) -> None:
    raw = input_path.read_bytes()
    if _is_png(raw):
        output_path.write_bytes(raw)
        return

    if sys.platform == "win32":
        ps = f"""
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile('{input_path}')
$img.Save('{output_path}', [System.Drawing.Imaging.ImageFormat]::Png)
$img.Dispose()
"""
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps],
            capture_output=True,
            text=True,
        )
        if r.returncode == 0 and output_path.exists():
            return

    raise ValueError(
        f"Cannot convert {input_path.suffix} without Blender. "
        "Upload PNG, install Blender, or use Windows with System.Drawing."
    )
