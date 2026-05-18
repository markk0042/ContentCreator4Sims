"use client";

import { motion } from "framer-motion";
import { fadeUp, stagger } from "./motion";

const MOCKUPS = [
  {
    title: "Gallery wall set",
    tag: "Wall art",
    colors: ["#6b4ce6", "#f4a4d0", "#2d1f4e"],
  },
  {
    title: "Sunset living rug",
    tag: "Rug",
    colors: ["#e8a84a", "#c45c8a", "#1a1028"],
  },
  {
    title: "Creator merch tee",
    tag: "CAS graphic",
    colors: ["#7ee0c9", "#9b6dff", "#0f0a1a"],
  },
  {
    title: "Dreamy bedroom walls",
    tag: "Wallpaper",
    colors: ["#b8a0ff", "#ffd4e8", "#3d2a5c"],
  },
  {
    title: "Cozy study poster",
    tag: "Wall art",
    colors: ["#4a9e6e", "#e8c547", "#1a2838"],
  },
  {
    title: "Plumbob-free patterns",
    tag: "Rug",
    colors: ["#ff6b9d", "#4ecdc4", "#2a1a42"],
  },
];

function MockupCard({
  title,
  tag,
  colors,
  index,
}: (typeof MOCKUPS)[0] & { index: number }) {
  return (
    <motion.figure
      variants={fadeUp}
      custom={index}
      whileHover={{ y: -8, rotate: index % 2 === 0 ? 1 : -1 }}
      className="card-enchant group overflow-hidden"
    >
      <motion.div
        className="relative aspect-[4/3] overflow-hidden"
        style={{
          background: `linear-gradient(135deg, ${colors[0]}, ${colors[1]} 50%, ${colors[2]})`,
        }}
      >
        <div className="absolute inset-4 rounded-lg border border-white/20 bg-black/20 backdrop-blur-sm" />
        <div className="absolute bottom-4 left-4 right-4 rounded-lg bg-night-950/60 px-3 py-2 backdrop-blur-md">
          <div className="h-2 w-2/3 rounded-full bg-white/30" />
          <motion.div
            className="mt-2 h-16 rounded-md bg-gradient-to-r from-white/20 to-white/5"
            animate={{ opacity: [0.5, 0.8, 0.5] }}
            transition={{ duration: 3, repeat: Infinity, delay: index * 0.2 }}
          />
        </div>
        <span className="absolute right-3 top-3 rounded-full bg-night-950/70 px-2 py-0.5 text-xs text-enchant-mint">
          {tag}
        </span>
      </motion.div>
      <figcaption className="p-4">
        <p className="font-display text-enchant-gold">{title}</p>
        <p className="text-xs text-white/45">Example mockup — your art, your style</p>
      </figcaption>
    </motion.figure>
  );
}

export function Gallery() {
  return (
    <section className="border-y border-white/5 bg-night-900/30 py-24">
      <motion.div
        className="mx-auto max-w-6xl px-4"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-60px" }}
        variants={stagger}
      >
        <motion.p variants={fadeUp} className="text-center text-sm uppercase tracking-[0.3em] text-enchant-violet">
          Inspiration gallery
        </motion.p>
        <motion.h2 variants={fadeUp} custom={1} className="mt-3 text-center font-display text-3xl text-enchant-gold">
          See what you could forge
        </motion.h2>
        <motion.p variants={fadeUp} custom={2} className="mx-auto mt-4 max-w-xl text-center text-white/55">
          Stylized previews only — no game screenshots or EA assets. Your uploads become your unique CC.
        </motion.p>

        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {MOCKUPS.map((m, i) => (
            <MockupCard key={m.title} {...m} index={i} />
          ))}
        </div>
      </motion.div>
    </section>
  );
}
