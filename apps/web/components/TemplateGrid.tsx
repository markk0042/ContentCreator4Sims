"use client";

import { motion } from "framer-motion";
import type { Template } from "@/lib/api";

const CATEGORY_LABEL: Record<string, string> = {
  decor: "✨ Decor",
  cas: "👕 CAS",
  build: "🏠 Build",
};

type Props = {
  templates: Template[];
  selectedId: string | null;
  onSelect: (id: string) => void;
};

export function TemplateGrid({ templates, selectedId, onSelect }: Props) {
  return (
    <motion.div
      className="grid gap-4 sm:grid-cols-2"
      initial="hidden"
      animate="visible"
      variants={{
        visible: { transition: { staggerChildren: 0.08 } },
      }}
    >
      {templates.map((tpl) => {
        const active = selectedId === tpl.id;
        return (
          <motion.button
            key={tpl.id}
            type="button"
            variants={{
              hidden: { opacity: 0, y: 12 },
              visible: { opacity: 1, y: 0 },
            }}
            onClick={() => onSelect(tpl.id)}
            className={`card-enchant group p-5 text-left transition ${
              active
                ? "border-enchant-gold/60 ring-2 ring-enchant-gold/40"
                : "hover:border-enchant-violet/50"
            }`}
          >
            <span className="text-xs font-medium uppercase tracking-wider text-enchant-mint">
              {CATEGORY_LABEL[tpl.category] ?? tpl.category}
            </span>
            <h3 className="mt-2 font-display text-xl text-enchant-gold">
              {tpl.name}
            </h3>
            <p className="mt-2 text-sm text-white/70">{tpl.description}</p>
            <p className="mt-3 text-xs text-white/45">
              Texture {tpl.textureWidth}×{tpl.textureHeight}
            </p>
          </motion.button>
        );
      })}
    </motion.div>
  );
}
