"""
Build Blender scene files for each template type.
Run with system Python (needs bpy only inside Blender) OR:
  blender --background --python build_scenes.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENES = ROOT / "blender" / "scenes"
SCRIPT = Path(__file__).resolve()


BLENDER_SCENE_CODE = '''
import bpy
from pathlib import Path

scenes_dir = Path(r"{scenes_dir}")
template = "{template}"
scenes_dir.mkdir(parents=True, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)

if template == "wall_art":
    bpy.ops.mesh.primitive_plane_add(size=1.2)
    bpy.context.object.name = "WallArt"
elif template == "rug":
    bpy.ops.mesh.primitive_plane_add(size=2.0)
    bpy.context.object.name = "Rug"
elif template == "tshirt_graphic":
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    bpy.context.object.name = "TShirt"
elif template == "wallpaper_swatch":
    bpy.ops.mesh.primitive_plane_add(size=1.0)
    bpy.context.object.name = "Wallpaper"
else:
    bpy.ops.mesh.primitive_plane_add(size=1.0)

mat = bpy.data.materials.new(name="TemplateMaterial")
mat.use_nodes = True
bpy.context.active_object.data.materials.append(mat)

bpy.ops.object.camera_add(location=(0, -2.5, 0.8), rotation=(1.1, 0, 0))
bpy.context.scene.camera = bpy.context.object

out = scenes_dir / f"{{template}}.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(out))
print("Wrote", out)
'''


TEMPLATES = ["wall_art", "rug", "tshirt_graphic", "wallpaper_swatch"]


def find_blender() -> str | None:
    import os
    import shutil

    env = os.environ.get("BLENDER_PATH")
    if env and Path(env).exists():
        return env
    found = shutil.which("blender")
    if found:
        return found
    for ver in ("4.4", "4.3", "4.2", "4.1", "4.0", "3.6"):
        p = Path(f"C:/Program Files/Blender Foundation/Blender {ver}/blender.exe")
        if p.exists():
            return str(p)
    return None


def main() -> None:
    blender = find_blender()
    if not blender:
        print(
            "Blender not found. Install Blender 4.x and set BLENDER_PATH, "
            "or add blender to PATH. Skipping scene build."
        )
        sys.exit(0)

    SCENES.mkdir(parents=True, exist_ok=True)
    for template in TEMPLATES:
        code = BLENDER_SCENE_CODE.format(scenes_dir=str(SCENES).replace("\\", "/"), template=template)
        print(f"Building scene: {template}")
        subprocess.run(
            [blender, "--background", "--python-expr", code],
            check=True,
        )
    print("All Blender scenes ready in", SCENES)


if __name__ == "__main__":
    main()
