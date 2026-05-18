"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { fadeUp, stagger } from "./motion";

export function FreeTrial() {
  return (
    <section className="py-24">
      <motion.div
        className="mx-auto max-w-6xl px-4"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
      >
        <motion.div
          variants={fadeUp}
          className="relative overflow-hidden rounded-3xl border border-enchant-mint/30 bg-gradient-to-br from-enchant-mint/10 via-night-900 to-enchant-violet/10 p-10 md:p-14"
        >
          <motion.div
            className="pointer-events-none absolute right-0 top-0 h-64 w-64 rounded-full bg-enchant-mint/20 blur-[80px]"
            animate={{ x: [0, 20, 0], opacity: [0.3, 0.5, 0.3] }}
            transition={{ duration: 6, repeat: Infinity }}
          />
          <motion.div className="relative max-w-2xl">
            <span className="inline-block rounded-full border border-enchant-mint/40 bg-enchant-mint/10 px-4 py-1 text-sm font-medium text-enchant-mint">
              Free trial
            </span>
            <h2 className="mt-6 font-display text-3xl text-white md:text-4xl">
              2 free creations to start your forge
            </h2>
            <p className="mt-4 text-lg text-white/70">
              Sign up and craft two complete packages on us — full download, install guide, and
              in-game-ready output. No card required to begin your trial.
            </p>
            <ul className="mt-6 space-y-3 text-white/65">
              <li className="flex gap-3">
                <span className="text-enchant-gold">✦</span>
                Try every template type in the MVP
              </li>
              <li className="flex gap-3">
                <span className="text-enchant-gold">✦</span>
                Credits only used when a creation succeeds
              </li>
              <li className="flex gap-3">
                <span className="text-enchant-gold">✦</span>
                Upgrade anytime when you are ready for more
              </li>
            </ul>
            <Link href="/studio" className="btn-primary mt-8 inline-block">
              Claim your 2 free creations
            </Link>
          </motion.div>
        </motion.div>
      </motion.div>
    </section>
  );
}
