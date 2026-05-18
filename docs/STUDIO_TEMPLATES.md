# Sims 4 Studio Base Templates

Dev packages in `templates/bases/` are **minimal DBPF texture containers** for pipeline testing. They validate the Blender → packager flow but are **not** full in-game objects.

## Production workflow

1. Create a recolor in **Sims 4 Studio** for wall art, rug, CAS shirt, or wallpaper.
2. Export the **base `.package`** before applying your texture (or export once and note the texture TGI).
3. Use **s4pe** or Studio's resource viewer to find the diffuse texture **Type / Group / Instance**.
4. Replace the file in `templates/bases/<id>.package`.
5. Update `templates/manifest.json` `textureResource` to match the real TGI.

## Blender scenes

Scenes in `blender/scenes/` control preview framing and bake resolution. Rebuild with:

```bash
npm run setup:blender
```

## Verify in-game

- Windows PC, legal copy of The Sims 4
- Only one `.package` per test to isolate issues
- Check `lastException.txt` in the Sims 4 folder if the game fails to load
