import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _load_dotenv() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

root_dir: Path = ROOT
data_dir: Path = ROOT / "data"
uploads_dir: Path = data_dir / "uploads"
outputs_dir: Path = data_dir / "outputs"
templates_dir: Path = ROOT / "templates"
blender_scenes_dir: Path = ROOT / "blender" / "scenes"
blender_scripts_dir: Path = ROOT / "blender" / "scripts"
jobs_file: Path = data_dir / "jobs.json"
blender_path: str | None = os.environ.get("BLENDER_PATH")
skip_blender: bool = os.environ.get("SKIP_BLENDER", "").lower() in ("1", "true", "yes")
free_credits_default: int = int(os.environ.get("FREE_CREDITS", "999"))
