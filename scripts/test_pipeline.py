"""Quick local pipeline test without HTTP."""
import sys
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "worker"))

from packager.png_util import solid_png
from app.pipeline import run_conversion

job_id = str(uuid4())
work = ROOT / "data" / "work" / job_id
work.mkdir(parents=True, exist_ok=True)
src = work / "source.png"
src.write_bytes(solid_png(256, 256, (200, 100, 50, 255)))

out = run_conversion(
    job_id=job_id,
    template_id="wall_art",
    source_path=src,
    work_dir=work,
)
print("OK:", out, "size", out.stat().st_size)
