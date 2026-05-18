from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from typing import Any

from . import config as settings


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class JobStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._path = settings.jobs_file
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._write({"jobs": [], "credits": settings.free_credits_default})

    def _read(self) -> dict[str, Any]:
        return json.loads(self._path.read_text(encoding="utf-8"))

    def _write(self, data: dict[str, Any]) -> None:
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get_credits(self) -> int:
        with self._lock:
            return int(self._read().get("credits", settings.free_credits_default))

    def consume_credit(self) -> bool:
        with self._lock:
            data = self._read()
            credits = int(data.get("credits", 0))
            if credits <= 0:
                return False
            data["credits"] = credits - 1
            self._write(data)
            return True

    def create_job(self, template_id: str, source_filename: str) -> dict[str, Any]:
        job = {
            "id": str(uuid.uuid4()),
            "templateId": template_id,
            "status": "queued",
            "sourceFilename": source_filename,
            "outputPackage": None,
            "error": None,
            "createdAt": _now(),
            "updatedAt": _now(),
        }
        with self._lock:
            data = self._read()
            data["jobs"].insert(0, job)
            self._write(data)
        return job

    def update_job(self, job_id: str, **fields: Any) -> dict[str, Any] | None:
        with self._lock:
            data = self._read()
            for job in data["jobs"]:
                if job["id"] == job_id:
                    job.update(fields)
                    job["updatedAt"] = _now()
                    self._write(data)
                    return job
        return None

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        with self._lock:
            for job in self._read()["jobs"]:
                if job["id"] == job_id:
                    return job
        return None

    def list_jobs(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._read()["jobs"])


job_store = JobStore()
