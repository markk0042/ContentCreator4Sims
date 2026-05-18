"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { fadeUp, stagger } from "./motion";

const FEATURES = [
  "Unlimited template recolors",
  "Blender-powered texture workshop",
  "Downloadable .package files",
  "Step-by-step install guides",
  "Creation history & re-downloads",
  "Priority queue (coming soon)",
];

export function Pricing() {
  return (
    <section id="pricing" className="py-24">
      <motion.div
        className="mx-auto max-w-6xl px-4"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
      >
        <motion.div variants={fadeUp} className="text-center">
          <p className="text-sm uppercase tracking-[0.3em] text-enchant-gold">Pricing</p>
          <h2 className="mt-3 font-display text-3xl text-white md:text-4xl">
            Keep forging for €9/month
          </h2>
          <p className="mx-auto mt-4 max-w-lg text-white/60">
            After your free creations, subscribe to keep the workshop open. Cancel anytime.
          </p>
        </motion.div>

        <motion.div
          variants={fadeUp}
          custom={2}
          className="card-enchant mx-auto mt-12 max-w-md overflow-hidden border-enchant-gold/30"
        >
          <div className="bg-gradient-to-r from-enchant-violet/20 to-enchant-pink/20 px-8 py-6 text-center">
            <p className="text-sm uppercase tracking-wider text-enchant-pink">Studio Pro</p>
            <p className="mt-2 font-display text-5xl text-enchant-gold">
              €9
              <span className="text-lg font-body text-white/50">/month</span>
            </p>
          </div>
          <ul className="space-y-3 px-8 py-8">
            {FEATURES.map((f) => (
              <li key={f} className="flex gap-3 text-sm text-white/75">
                <span className="text-enchant-mint">✓</span>
                {f}
              </li>
            ))}
          </ul>
          <motion.div className="border-t border-white/10 px-8 py-6" whileHover={{ scale: 1.01 }}>
            <Link href="/studio" className="btn-primary block w-full text-center">
              Start free, upgrade later
            </Link>
            <p className="mt-3 text-center text-xs text-white/40">
              Secure billing via Stripe when subscriptions launch
            </p>
          </motion.div>
        </motion.div>
      </motion.div>
    </section>
  );
}
