"use client";

import { motion } from "framer-motion";
import { useRef, useState } from "react";
import { createJob, type Job } from "@/lib/api";

type Props = {
  templateId: string | null;
  canCreate: boolean;
  onJobCreated: (job: Job) => void;
};

export function UploadPanel({ templateId, canCreate, onJobCreated }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onFile = (f: File | null) => {
    setFile(f);
    setError(null);
    if (preview) URL.revokeObjectURL(preview);
    if (f) setPreview(URL.createObjectURL(f));
    else setPreview(null);
  };

  const submit = async () => {
    if (!templateId || !file) return;
    setLoading(true);
    setError(null);
    try {
      const job = await createJob(templateId, file);
      onJobCreated(job);
      onFile(null);
      if (inputRef.current) inputRef.current.value = "";
    } catch (e) {
      setError(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div className="card-enchant p-6">
      <h2 className="font-display text-2xl text-enchant-pink">
        Cast your creation
      </h2>
      <p className="mt-1 text-sm text-white/60">
        Upload PNG, JPG, or WebP. Blender bakes it into your template texture.
      </p>

      {!canCreate && (
        <p className="mt-4 rounded-lg border border-enchant-gold/30 bg-night-800/80 px-4 py-3 text-sm text-enchant-gold">
          No credits left. Reset <code className="text-enchant-mint">data/jobs.json</code>{" "}
          for local testing.
        </p>
      )}

      <motion.div
        className="mt-5 flex min-h-[160px] cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-enchant-violet/40 bg-night-800/40 p-6 transition hover:border-enchant-pink/60"
        onClick={() => inputRef.current?.click()}
        whileHover={{ scale: 1.01 }}
      >
        {preview ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={preview}
            alt="Preview"
            className="max-h-48 rounded-lg object-contain shadow-gold"
          />
        ) : (
          <>
            <span className="text-4xl">🖼️</span>
            <span className="mt-2 text-sm text-white/70">
              Click to choose an image
            </span>
          </>
        )}
        <input
          ref={inputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp"
          className="hidden"
          onChange={(e) => onFile(e.target.files?.[0] ?? null)}
        />
      </motion.div>

      {error && (
        <p className="mt-3 text-sm text-red-300">{error}</p>
      )}

      <button
        type="button"
        className="btn-primary mt-5 w-full"
        disabled={!templateId || !file || !canCreate || loading}
        onClick={submit}
      >
        {loading ? "Weaving your spell…" : "Create .package"}
      </button>
    </motion.div>
  );
}
