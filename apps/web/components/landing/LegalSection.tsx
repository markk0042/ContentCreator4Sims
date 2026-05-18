"use client";

import { motion } from "framer-motion";
import { fadeUp, stagger } from "./motion";

export function LegalSection() {
  return (
    <section id="legal" className="py-16">
      <motion.div
        className="mx-auto max-w-4xl px-4"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        variants={stagger}
      >
        <motion.div
          variants={fadeUp}
          className="rounded-2xl border border-amber-500/25 bg-amber-500/5 p-8 md:p-10"
        >
          <h2 className="font-display text-2xl text-amber-200/90">
            Legal & intellectual property
          </h2>
          <motion.div variants={fadeUp} custom={1} className="mt-6 space-y-4 text-sm leading-relaxed text-white/65">
            <p>
              <strong className="text-white/90">Independent fan tool.</strong> SimForge Studio
              is created by fans for the custom content community. It is not affiliated with,
              connected to, or approved by Electronic Arts, Maxis, or The Sims™.
            </p>
            <p>
              <strong className="text-white/90">No EA branding.</strong> We do not use official
              logos, plumbobs, or game assets in our marketing. References to “Sims 4” describe
              compatibility only.
            </p>
            <p>
              <strong className="text-white/90">Your content, your responsibility.</strong> You
              must own or have explicit rights to every image you upload. Do not submit
              copyrighted characters, brand logos, celebrity likenesses, or material you cannot
              license. We may remove content and suspend accounts that violate these rules.
            </p>
            <p>
              <strong className="text-white/90">Game & modding policies.</strong> You are
              responsible for complying with EA’s terms and your local laws. Custom content is
              used at your own risk; always back up your save and Mods folder.
            </p>
          </motion.div>
        </motion.div>
      </motion.div>
    </section>
  );
}
