"use client";

import Link from "next/link";
import { motion } from "framer-motion";

export function FinalCTA() {
  return (
    <section className="pb-24 pt-8">
      <motion.div
        className="mx-auto max-w-4xl px-4 text-center"
        initial={{ opacity: 0, y: 32 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <motion.div
          className="relative overflow-hidden rounded-3xl border border-enchant-violet/40 bg-gradient-to-br from-enchant-violet/25 via-night-900 to-enchant-pink/20 px-8 py-16 md:px-16"
          animate={{
            boxShadow: [
              "0 0 60px rgba(155,109,255,0.25)",
              "0 0 80px rgba(244,164,208,0.2)",
              "0 0 60px rgba(155,109,255,0.25)",
            ],
          }}
          transition={{ duration: 5, repeat: Infinity }}
        >
          <h2 className="font-display text-3xl text-white md:text-4xl">
            Ready to enchant your Mods folder?
          </h2>
          <p className="mx-auto mt-4 max-w-lg text-white/70">
            Join creators who turn sketches, logos, and fan art into playable custom content —
            honestly, beautifully, and without modding wizardry.
          </p>
          <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.98 }}>
            <Link
              href="/studio"
              className="btn-primary mt-10 inline-block min-w-[260px] text-lg shadow-gold"
            >
              Upload your art — start free ✦
            </Link>
          </motion.div>
          <p className="mt-6 text-xs text-white/40">
            2 free creations · then €9/month · cancel anytime
          </p>
        </motion.div>
      </motion.div>
    </section>
  );
}
