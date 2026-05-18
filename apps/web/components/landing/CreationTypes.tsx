"use client";

import { motion } from "framer-motion";
import { fadeUp, stagger } from "./motion";

const TYPES = [
  {
    id: "wall_art",
    name: "Wall art & posters",
    desc: "Frame your art as in-game wall decor.",
    gradient: "from-violet-600/40 to-fuchsia-500/30",
    emoji: "🖼️",
  },
  {
    id: "rug",
    name: "Rugs",
    desc: "Cozy floor pieces from your patterns.",
    gradient: "from-amber-600/30 to-rose-500/30",
    emoji: "🧶",
  },
  {
    id: "tshirt",
    name: "T-shirt graphics",
    desc: "Wearable graphic recolors for CAS.",
    gradient: "from-cyan-600/30 to-violet-500/30",
    emoji: "👕",
  },
  {
    id: "wallpaper",
    name: "Wallpaper swatches",
    desc: "Tileable build-mode wall styles.",
    gradient: "from-emerald-600/25 to-indigo-500/30",
    emoji: "🧱",
  },
];

export function CreationTypes() {
  return (
    <section id="templates" className="border-y border-white/5 bg-night-900/40 py-24">
      <motion.div
        className="mx-auto max-w-6xl px-4"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-80px" }}
        variants={stagger}
      >
        <motion.p variants={fadeUp} className="text-center text-sm uppercase tracking-[0.3em] text-enchant-pink">
          Supported today
        </motion.p>
        <motion.h2 variants={fadeUp} custom={1} className="mt-3 text-center font-display text-3xl text-enchant-gold md:text-4xl">
          Creation types
        </motion.h2>
        <motion.p variants={fadeUp} custom={2} className="mx-auto mt-4 max-w-2xl text-center text-white/60">
          MVP templates cover the most popular recolor workflows. More enchanted categories coming as we grow the forge.
        </motion.p>

        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {TYPES.map((t, i) => (
            <motion.div
              key={t.id}
              variants={fadeUp}
              custom={i + 2}
              whileHover={{ y: -6 }}
              className="card-enchant overflow-hidden"
            >
              <motion.div
                className={`flex h-36 items-center justify-center bg-gradient-to-br ${t.gradient}`}
                whileHover={{ scale: 1.02 }}
              >
                <span className="text-5xl drop-shadow-lg">{t.emoji}</span>
              </motion.div>
              <motion.div className="p-5">
                <h3 className="font-display text-lg text-white">{t.name}</h3>
                <p className="mt-2 text-sm text-white/55">{t.desc}</p>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </section>
  );
}
