"use client";

import { motion } from "framer-motion";
import {
  downloadUrl,
  installGuideUrl,
  type Job,
} from "@/lib/api";

const STATUS: Record<string, { label: string; color: string }> = {
  queued: { label: "Queued", color: "text-white/60" },
  processing: { label: "Weaving…", color: "text-enchant-mint" },
  completed: { label: "Ready", color: "text-enchant-gold" },
  failed: { label: "Failed", color: "text-red-300" },
};

type Props = {
  jobs: Job[];
};

export function JobList({ jobs }: Props) {
  if (jobs.length === 0) {
    return (
      <p className="text-sm text-white/50">No creations yet. Start your first spell above.</p>
    );
  }

  return (
    <ul className="space-y-3">
      {jobs.map((job) => {
        const st = STATUS[job.status] ?? STATUS.queued;
        return (
          <motion.li
            key={job.id}
            layout
            className="card-enchant flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between"
          >
            <motion.div>
              <p className="font-medium text-enchant-pink">{job.templateId}</p>
              <p className="text-xs text-white/50">{job.sourceFilename}</p>
              <p className={`mt-1 text-sm ${st.color}`}>{st.label}</p>
              {job.error && (
                <p className="mt-1 text-xs text-red-300">{job.error}</p>
              )}
            </motion.div>
            {job.status === "completed" && (
              <div className="flex flex-wrap gap-2">
                <a className="btn-primary text-center text-sm" href={downloadUrl(job.id)}>
                  Download .package
                </a>
                <a
                  className="btn-secondary text-sm"
                  href={installGuideUrl(job.id)}
                  target="_blank"
                  rel="noreferrer"
                >
                  Install guide
                </a>
              </div>
            )}
          </motion.li>
        );
      })}
    </ul>
  );
}
