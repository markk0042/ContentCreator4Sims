"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { motion } from "framer-motion";
import { JobList } from "@/components/JobList";
import { TemplateGrid } from "@/components/TemplateGrid";
import { UploadPanel } from "@/components/UploadPanel";
import {
  fetchEntitlements,
  fetchJob,
  fetchJobs,
  fetchTemplates,
  type Job,
  type Template,
} from "@/lib/api";

export default function StudioPage() {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [credits, setCredits] = useState(0);
  const [canCreate, setCanCreate] = useState(true);
  const [health, setHealth] = useState<string>("checking…");

  const refresh = useCallback(async () => {
    const [tpl, ent, jobList] = await Promise.all([
      fetchTemplates(),
      fetchEntitlements(),
      fetchJobs(),
    ]);
    setTemplates(tpl);
    setCredits(ent.credits);
    setCanCreate(ent.canCreate);
    setJobs(jobList);
    if (!selectedId && tpl.length) setSelectedId(tpl[0].id);
  }, [selectedId]);

  useEffect(() => {
    refresh().catch(console.error);
    fetch("/health")
      .then((r) => r.json())
      .then((h) =>
        setHealth(
          h.blender
            ? `Blender: ${h.blender}`
            : h.skipBlender
              ? "Blender skipped (resize fallback)"
              : "Blender not found — install or set BLENDER_PATH",
        ),
      )
      .catch(() => setHealth("Worker offline — start with npm run dev:worker"));
  }, [refresh]);

  useEffect(() => {
    const pending = jobs.some(
      (j) => j.status === "queued" || j.status === "processing",
    );
    if (!pending) return;
    const t = setInterval(async () => {
      const list = await fetchJobs();
      setJobs(list);
      await fetchEntitlements().then((e) => {
        setCredits(e.credits);
        setCanCreate(e.canCreate);
      });
    }, 2000);
    return () => clearInterval(t);
  }, [jobs]);

  const onJobCreated = async (job: Job) => {
    setJobs((prev) => [job, ...prev]);
    const poll = async () => {
      const updated = await fetchJob(job.id);
      setJobs((prev) =>
        prev.map((j) => (j.id === job.id ? updated : j)),
      );
      if (updated.status === "queued" || updated.status === "processing") {
        setTimeout(poll, 1500);
      } else {
        refresh();
      }
    };
    poll();
  };

  return (
    <main className="mx-auto max-w-6xl px-4 py-10 pb-20">
      <header className="text-center">
        <Link
          href="/"
          className="text-sm text-enchant-mint/80 transition hover:text-enchant-mint"
        >
          ← SimForge Studio
        </Link>
        <motion.p
          className="mt-4 text-sm uppercase tracking-[0.3em] text-enchant-mint"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          Creation workshop
        </motion.p>
        <motion.h1
          className="mt-2 font-display text-4xl text-enchant-gold sm:text-5xl"
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
        >
          Forge your CC
        </motion.h1>
        <p className="mx-auto mt-4 max-w-2xl text-white/70">
          Pick a template, upload your art, and download a Sims 4{" "}
          <code className="text-enchant-pink">.package</code> for your Mods
          folder.
        </p>
        <p className="mt-3 text-xs text-white/40">{health}</p>
        <p className="mt-2 text-sm text-enchant-gold">
          Credits: {credits} ✦
        </p>
      </header>

      <section className="mt-12">
        <h2 className="mb-4 font-display text-2xl text-enchant-violet">
          1 · Choose a template
        </h2>
        <TemplateGrid
          templates={templates}
          selectedId={selectedId}
          onSelect={setSelectedId}
        />
      </section>

      <section className="mt-10 grid gap-8 lg:grid-cols-2">
        <motion.div>
          <h2 className="mb-4 font-display text-2xl text-enchant-violet">
            2 · Upload & create
          </h2>
          <UploadPanel
            templateId={selectedId}
            canCreate={canCreate}
            onJobCreated={onJobCreated}
          />
        </motion.div>
        <motion.div>
          <h2 className="mb-4 font-display text-2xl text-enchant-violet">
            3 · Your creations
          </h2>
          <JobList jobs={jobs} />
        </motion.div>
      </section>
    </main>
  );
}
