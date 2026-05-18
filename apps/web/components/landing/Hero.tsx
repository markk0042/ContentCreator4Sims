"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export function Hero() {
  return (
    <section className="relative overflow-hidden pt-28 pb-20 md:pt-36 md:pb-28">
      <motion.div
        className="pointer-events-none absolute -left-32 top-20 h-96 w-96 rounded-full bg-enchant-violet/30 blur-[100px]"
        animate={{ scale: [1, 1.15, 1], opacity: [0.4, 0.55, 0.4] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="pointer-events-none absolute -right-24 top-40 h-80 w-80 rounded-full bg-enchant-pink/25 blur-[90px]"
        animate={{ scale: [1.1, 1, 1.1], opacity: [0.35, 0.5, 0.35] }}
        transition={{ duration: 7, repeat: Infinity, ease: "easeInOut" }}
      />

      <motion.div
        className="relative mx-auto max-w-6xl px-4 text-center"
        initial="hidden"
        animate="visible"
        variants={{
          visible: { transition: { staggerChildren: 0.12 } },
        }}
      >
        <motion.p
          variants={{
            hidden: { opacity: 0, y: 12 },
            visible: { opacity: 1, y: 0 },
          }}
          className="text-sm font-medium uppercase tracking-[0.35em] text-enchant-mint"
        >
          Independent fan creation tool
        </motion.p>

        <motion.h1
          variants={{
            hidden: { opacity: 0, y: 24 },
            visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
          }}
          className="mt-6 font-display text-4xl leading-tight sm:text-5xl md:text-6xl lg:text-7xl"
        >
          <span className="bg-gradient-to-r from-enchant-gold via-white to-enchant-pink bg-clip-text text-transparent">
            Turn your artwork
          </span>
          <br />
          <span className="text-white">into Sims 4 custom content</span>
        </motion.h1>

        <motion.p
          variants={{
            hidden: { opacity: 0 },
            visible: { opacity: 1 },
          }}
          className="mx-auto mt-6 max-w-2xl text-lg text-white/70 md:text-xl"
        >
          Upload an image, choose a template, and download a ready-to-install{" "}
          <span className="text-enchant-pink">.package</span> for PC — no modding
          degree required. Template recolors crafted in our magical workshop.
        </motion.p>

        <motion.div
          variants={{
            hidden: { opacity: 0, y: 16 },
            visible: { opacity: 1, y: 0 },
          }}
          className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
        >
          <Link href="/studio" className="btn-primary min-w-[220px] text-lg">
            Upload your art ✦
          </Link>
          <a href="#how-it-works" className="btn-secondary min-w-[180px] text-center">
            See how it works
          </a>
        </motion.div>

        <motion.div
          variants={{ hidden: { opacity: 0 }, visible: { opacity: 1 } }}
          className="mt-12 flex flex-wrap items-center justify-center gap-6 text-sm text-white/50"
        >
          <span className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-enchant-mint" />
            2 free creations
          </span>
          <span className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-enchant-gold" />
            Install guides included
          </span>
          <span className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-enchant-violet" />
            PC Mods folder ready
          </span>
        </motion.div>

        <motion.div
          variants={{ hidden: { opacity: 0, scale: 0.95 }, visible: { opacity: 1, scale: 1 } }}
          className="card-enchant mx-auto mt-16 max-w-3xl overflow-hidden p-1"
        >
          <motion.div
            className="relative rounded-xl bg-gradient-to-br from-night-800 via-night-900 to-night-800 p-8 md:p-12"
            animate={{ boxShadow: ["0 0 40px rgba(155,109,255,0.2)", "0 0 60px rgba(232,197,71,0.15)", "0 0 40px rgba(155,109,255,0.2)"] }}
            transition={{ duration: 4, repeat: Infinity }}
          >
            <motion.div
              className="mx-auto flex h-32 w-32 items-center justify-center rounded-2xl border-2 border-dashed border-enchant-violet/50 bg-enchant-violet/10 md:h-40 md:w-40"
              whileHover={{ scale: 1.03, borderColor: "rgba(244,164,208,0.8)" }}
            >
              <span className="text-5xl md:text-6xl">🖼️</span>
            </motion.div>
            <p className="mt-6 font-display text-xl text-enchant-gold">
              Your image → enchanted texture → .package
            </p>
            <p className="mt-2 text-sm text-white/50">
              Blender-powered baking · trusted template pipeline
            </p>
          </motion.div>
        </motion.div>
      </motion.div>
    </section>
  );
}
