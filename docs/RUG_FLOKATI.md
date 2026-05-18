# PS Flokati rug template (licensed CC)

The file `templates/bases/rug.package` is **PS Flokati 2** from your licensed CC source.

## What SimForge does

- Replaces **33** DDS color swatches (512×512 only). The shared **256×256** map is a normal/detail channel and must not be overwritten (doing so causes brown + multicolor garbage in-game).
- Converts via `texconv`, then **DST5** headers per swatch (plain `DXT5` breaks in-game).
- Outputs a **new** `.package` for the player’s Mods folder.

## Requirements

- **texconv.exe** (DirectXTex, Windows SDK) on PATH for DDS conversion.
- Worker running with the updated packager (index parser fix for full Studio packages).

## Re-import a newer CC version

1. Replace `templates/bases/rug.package` with the new `.package`.
2. Run:

```powershell
python scripts/extract_texture_instances.py templates/bases/rug.package
```

3. Paste the JSON array into `templates/manifest.json` → `rug.textureInstances`.
4. Confirm `textureResource.type` / `group` still match (usually `0x00b2d882` / `0x80000000`).

## Legal

Keep written permission on file. Credit the creator where their license requires it.
