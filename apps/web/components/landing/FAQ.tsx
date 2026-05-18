"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { fadeUp, stagger } from "./motion";

const FAQS = [
  {
    q: "Is SimForge Studio official?",
    a: "No. SimForge Studio is an independent fan-made tool. We are not affiliated with, endorsed by, or sponsored by Electronic Arts, Maxis, or The Sims franchise.",
  },
  {
    q: "Can any image become any Sims item?",
    a: "No — and we will never claim that. We support template-based recolors: your image replaces textures on curated bases (posters, rugs, shirt graphics, wallpaper swatches).",
  },
  {
    q: "What file do I get?",
    a: "A Sims 4 .package file for PC plus clear install instructions for your Mods folder. Enable custom content and restart the game after installing.",
  },
  {
    q: "Do I need Sims 4 Studio or Blender?",
    a: "You do not need Studio to use SimForge. Blender runs on our side for texture baking. Advanced creators can swap in Studio-exported base templates for deeper compatibility.",
  },
  {
    q: "What images can I upload?",
    a: "Only images you own or have permission to use. No copyrighted characters, logos, or brands you do not control. You agree to this when uploading.",
  },
  {
    q: "How do free creations work?",
    a: "New accounts receive 2 successful creation credits. A credit is only spent when your package is generated successfully — failed jobs do not count.",
  },
];

export function FAQ() {
  const [open, setOpen] = useState<number | null>(0);

  return (
    <section id="faq" className="py-24">
      <motion.div
        className="mx-auto max-w-3xl px-4"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
      >
        <motion.p variants={fadeUp} className="text-center text-sm uppercase tracking-[0.3em] text-enchant-mint">
          Questions & answers
        </motion.p>
        <motion.h2 variants={fadeUp} custom={1} className="mt-3 text-center font-display text-3xl text-enchant-gold">
          FAQ
        </motion.h2>

        <div className="mt-12 space-y-3">
          {FAQS.map((item, i) => (
            <motion.div key={item.q} variants={fadeUp} custom={i + 2} className="card-enchant overflow-hidden">
              <button
                type="button"
                className="flex w-full items-center justify-between gap-4 px-5 py-4 text-left"
                onClick={() => setOpen(open === i ? null : i)}
                aria-expanded={open === i}
              >
                <span className="font-medium text-white">{item.q}</span>
                <motion.span
                  animate={{ rotate: open === i ? 45 : 0 }}
                  className="text-xl text-enchant-gold"
                >
                  +
                </motion.span>
              </button>
              <AnimatePresence>
                {open === i && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.25 }}
                  >
                    <p className="border-t border-white/10 px-5 pb-4 pt-3 text-sm leading-relaxed text-white/60">
                      {item.a}
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </section>
  );
}
