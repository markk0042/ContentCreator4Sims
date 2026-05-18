"use client";

import { motion } from "framer-motion";
import { fadeUp, stagger } from "./motion";

const STEPS = [
  {
    num: "01",
    title: "Choose a template",
    desc: "Pick wall art, rug, t-shirt graphic, or wallpaper swatch. Each template is a curated recolor base.",
    icon: "🪄",
  },
  {
    num: "02",
    title: "Upload your artwork",
    desc: "Drop PNG, JPG, or WebP. We crop and bake it to the template's texture specs in our workshop pipeline.",
    icon: "🖼️",
  },
  {
    num: "03",
    title: "We forge your .package",
    desc: "Blender prepares your texture; our packager builds a valid Sims 4 package file with install instructions.",
    icon: "⚗️",
  },
  {
    num: "04",
    title: "Install in The Sims 4",
    desc: "Copy to your Mods folder, enable custom content, restart — and enjoy your creation in-game on PC.",
    icon: "🏠",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24">
      <div className="mx-auto max-w-6xl px-4">
        <motion.div
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
          variants={stagger}
          className="text-center"
        >
          <motion.p variants={fadeUp} className="text-sm uppercase tracking-[0.3em] text-enchant-mint">
            Simple spellcasting
          </motion.p>
          <motion.h2 variants={fadeUp} custom={1} className="mt-3 font-display text-3xl text-enchant-gold md:text-4xl">
            How it works
          </motion.h2>
          <motion.p variants={fadeUp} custom={2} className="mx-auto mt-4 max-w-xl text-white/60">
            Four steps from canvas to Mods folder. Honest, template-based recolors — not magic mesh generation.
          </motion.p>
        </motion.div>

        <motion.div
          className="mt-16 grid gap-6 md:grid-cols-2 lg:grid-cols-4"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-60px" }}
          variants={stagger}
        >
          {STEPS.map((step, i) => (
            <motion.article
              key={step.num}
              variants={fadeUp}
              custom={i}
              className="card-enchant group relative overflow-hidden p-6 transition hover:border-enchant-violet/40"
            >
              <span className="absolute -right-2 -top-4 font-display text-6xl text-white/5">
                {step.num}
              </span>
              <span className="text-3xl">{step.icon}</span>
              <h3 className="mt-4 font-display text-xl text-white">{step.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-white/60">{step.desc}</p>
            </motion.article>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
