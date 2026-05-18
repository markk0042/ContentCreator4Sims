from __future__ import annotations

import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from . import config as settings
from .blender_runner import resolve_blender
from .job_store import job_store
from .pipeline import load_manifest, run_conversion

app = Flask(__name__)
CORS(
    app,
    origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
)

executor = ThreadPoolExecutor(max_workers=2)
ALLOWED_EXT = {".png", ".jpg", ".jpeg", ".webp"}


def _process_job(job_id: str, template_id: str, source_path: Path) -> None:
    job_store.update_job(job_id, status="processing")
    work_dir = settings.data_dir / "work" / job_id
    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        out_pkg = run_conversion(
            job_id=job_id,
            template_id=template_id,
            source_path=source_path,
            work_dir=work_dir,
        )
        if not job_store.consume_credit():
            job_store.update_job(
                job_id,
                status="failed",
                error="No credits remaining",
            )
            return
        job_store.update_job(
            job_id,
            status="completed",
            outputPackage=str(out_pkg),
            error=None,
        )
    except Exception as exc:
        job_store.update_job(job_id, status="failed", error=str(exc))


@app.get("/health")
def health():
    return jsonify(
        {
            "ok": True,
            "blender": resolve_blender(),
            "skipBlender": settings.skip_blender,
            "credits": job_store.get_credits(),
        }
    )


@app.get("/api/templates")
def list_templates():
    return jsonify(load_manifest())


@app.get("/api/entitlements")
def entitlements():
    return jsonify(
        {
            "credits": job_store.get_credits(),
            "subscriptionActive": False,
            "canCreate": job_store.get_credits() > 0,
        }
    )


@app.get("/api/jobs")
def list_jobs():
    return jsonify({"jobs": job_store.list_jobs()})


@app.get("/api/jobs/<job_id>")
def get_job(job_id: str):
    job = job_store.get_job(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(job)


@app.get("/api/jobs/<job_id>/download")
def download_package(job_id: str):
    job = job_store.get_job(job_id)
    if not job or job["status"] != "completed" or not job.get("outputPackage"):
        return jsonify({"error": "Package not ready"}), 404
    path = Path(job["outputPackage"])
    if not path.exists():
        return jsonify({"error": "Package file missing"}), 404
    return send_file(path, as_attachment=True, download_name=path.name)


@app.get("/api/jobs/<job_id>/install-guide")
def install_guide(job_id: str):
    job = job_store.get_job(job_id)
    if not job or not job.get("outputPackage"):
        return jsonify({"error": "Job not found"}), 404
    guide = Path(job["outputPackage"]).parent / "INSTALL.md"
    if not guide.exists():
        return jsonify({"error": "Install guide not found"}), 404
    return send_file(guide, mimetype="text/markdown", as_attachment=True, download_name="INSTALL.md")


@app.post("/api/jobs")
def create_job():
    if job_store.get_credits() <= 0:
        return jsonify({"error": "No credits remaining"}), 402

    template_id = request.form.get("templateId")
    image = request.files.get("image")
    if not template_id or not image:
        return jsonify({"error": "templateId and image required"}), 400

    ext = Path(image.filename or "").suffix.lower()
    if ext not in ALLOWED_EXT:
        return jsonify({"error": f"Unsupported file type: {ext}"}), 400

    tpl_ids = {t["id"] for t in load_manifest()["templates"]}
    if template_id not in tpl_ids:
        return jsonify({"error": f"Unknown template: {template_id}"}), 400

    job = job_store.create_job(template_id, image.filename or "upload.png")
    dest = settings.uploads_dir / job["id"] / f"source{ext}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)

    executor.submit(_process_job, job["id"], template_id, dest)
    return jsonify(job), 202


def create_app() -> Flask:
    settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    settings.outputs_dir.mkdir(parents=True, exist_ok=True)
    return app


if __name__ == "__main__":
    create_app()
    from waitress import serve

    print("Worker http://127.0.0.1:8000")
    serve(app, host="127.0.0.1", port=8000, threads=4)
