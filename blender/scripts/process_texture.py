"""
Blender headless texture processor for ContentCreator4Sims.
Run:
  blender <scene.blend> --background --python process_texture.py -- \
    --input image.png --output texture.png --width 512 --height 512
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="User source image path")
    parser.add_argument("--output", required=True, help="Processed texture PNG path")
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--template", default="wall_art")
    return parser.parse_args(argv)


def main() -> None:
    import bpy

    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    mat = None
    for m in bpy.data.materials:
        if m.use_nodes:
            mat = m
            break
    if mat is None:
        mat = bpy.data.materials.new(name="CC4S_Material")
        mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    tex = nodes.new(type="ShaderNodeTexImage")
    tex.image = bpy.data.images.load(str(input_path))
    tex.extension = "CLIP"
    links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], output_node.inputs["Surface"])

    for obj in bpy.data.objects:
        if obj.type == "MESH":
            if obj.data.materials:
                obj.data.materials[0] = mat
            else:
                obj.data.materials.append(mat)

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE_NEXT" if bpy.app.version >= (4, 2, 0) else "BLENDER_EEVEE"
    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.film_transparent = True

    # Bake diffuse to target resolution
    bpy.context.view_layer.update()
    img = bpy.data.images.new(
        name="CC4S_Baked",
        width=args.width,
        height=args.height,
        alpha=True,
    )
    tex.image = img

    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        try:
            bpy.ops.object.bake(
                type="DIFFUSE",
                pass_filter={"COLOR"},
                margin=8,
                use_clear=True,
            )
        except Exception:
            # Fallback: resize source via image pixels copy
            src = bpy.data.images.load(str(input_path))
            src.scale(args.width, args.height)
            src.filepath_raw = str(output_path)
            src.file_format = "PNG"
            src.save()
            print(f"Saved resized texture (fallback): {output_path}")
            return
        finally:
            obj.select_set(False)

    img.filepath_raw = str(output_path)
    img.file_format = "PNG"
    img.save()
    print(f"Saved baked texture: {output_path}")


if __name__ == "__main__":
    main()
