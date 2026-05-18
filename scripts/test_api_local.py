"""Localhost API smoke test (worker :8000)."""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys_path = ROOT / "services" / "worker"
import sys

sys.path.insert(0, str(sys_path))
from packager.png_util import solid_png

BASE = "http://127.0.0.1:8000"
png = ROOT / "data" / "test_upload.png"
png.write_bytes(solid_png(128, 128, (120, 60, 200, 255)))

# multipart via stdlib
boundary = "----cc4sboundary"
body = b""
body += f"--{boundary}\r\n".encode()
body += b'Content-Disposition: form-data; name="templateId"\r\n\r\nwall_art\r\n'
body += f"--{boundary}\r\n".encode()
body += (
    b'Content-Disposition: form-data; name="image"; filename="test.png"\r\n'
    b"Content-Type: image/png\r\n\r\n"
)
body += png.read_bytes()
body += f"\r\n--{boundary}--\r\n".encode()

req = urllib.request.Request(
    f"{BASE}/api/jobs",
    data=body,
    method="POST",
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
)
with urllib.request.urlopen(req, timeout=10) as r:
    job = json.loads(r.read())
job_id = job["id"]
print("Created job:", job_id, job["status"])

for _ in range(30):
    time.sleep(1)
    with urllib.request.urlopen(f"{BASE}/api/jobs/{job_id}", timeout=5) as r:
        job = json.loads(r.read())
    print("  status:", job["status"])
    if job["status"] in ("completed", "failed"):
        break

if job["status"] != "completed":
    raise SystemExit(f"FAILED: {job.get('error')}")

with urllib.request.urlopen(f"{BASE}/api/jobs/{job_id}/download", timeout=5) as r:
    pkg = r.read()
print(f"Download OK: {len(pkg)} bytes")
print("LOCALHOST TEST PASSED")
