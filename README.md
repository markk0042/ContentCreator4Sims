# ContentCreator4Sims

Local-first web app: upload an image → **Blender** bakes a template texture → Python worker patches a Sims 4 **`.package`** file for PC Mods folder install.

Auth, Supabase, Stripe, and domain deployment are **intentionally deferred**.

## Prerequisites

- **Node.js** 20+
- **Python** 3.11+ (3.14 works; uses Flask + stdlib PNG — no Pillow required)
- **Blender** 4.x (recommended) — [blender.org](https://www.blender.org/)
  - Or set `SKIP_BLENDER=true` in `.env` to use Pillow resize only (faster dev, no 3D bake)

## Quick start (Windows)

```powershell
cd C:\Users\markk\Desktop\ContentCreator4Sims

# Install deps + dev template packages (+ Blender scenes if Blender is installed)
npm run setup

# Terminal 1 — API worker (port 8000)
npm run dev:worker

# Terminal 2 — Web UI (port 3001)
npm run dev
```

Open **http://localhost:3001** (port 3001 avoids conflicts if something else uses 3000)

## Project layout

```
apps/web/              Next.js UI (fantasy theme)
services/worker/       FastAPI + queue + DBPF packager
blender/scenes/        Per-template .blend files
blender/scripts/       Headless texture bake
templates/             manifest.json + base .package files
data/                  uploads, outputs, jobs.json (local state)
scripts/               generate_dev_templates.py
```

## How conversion works

1. User picks template (wall art, rug, t-shirt graphic, wallpaper swatch).
2. Image saved to `data/uploads/<jobId>/`.
3. **Blender** (or Pillow fallback) produces `diffuse.png` at template resolution.
4. **Packager** copies the base `.package` and replaces the PNG resource (DBPF patch).
5. User downloads `.package` + `INSTALL.md`.

## Blender configuration

```env
# .env in repo root (optional)
BLENDER_PATH=C:\Program Files\Blender Foundation\Blender 4.2\blender.exe
SKIP_BLENDER=false
```

Rebuild scene files:

```powershell
npm run setup:blender
```

## In-game CC (important)

Dev packages in `templates/bases/` are **minimal texture containers** for testing the pipeline. For real Sims 4 items, export base packages from **Sims 4 Studio** and update `templates/manifest.json` resource IDs — see [docs/STUDIO_TEMPLATES.md](docs/STUDIO_TEMPLATES.md).

## Local credits

`data/jobs.json` stores jobs and credits (default **999** for local dev). Reset credits:

```json
{ "jobs": [], "credits": 999 }
```

## API (worker :8000)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Blender path, credits |
| GET | `/api/templates` | Template manifest |
| POST | `/api/jobs` | `multipart`: `templateId`, `image` |
| GET | `/api/jobs/:id` | Job status |
| GET | `/api/jobs/:id/download` | `.package` file |

## Later (not in this build)

- Supabase auth + Postgres
- Stripe €9/mo subscription
- JWT, production domain, cloud storage

## License

MIT — not affiliated with Electronic Arts or The Sims 4.
