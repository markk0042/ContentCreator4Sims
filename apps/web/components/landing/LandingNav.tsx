"use client";

import Link from "next/link";
import { motion } from "framer-motion";

const LINKS = [
  { href: "#how-it-works", label: "How it works" },
  { href: "#templates", label: "Templates" },
  { href: "#pricing", label: "Pricing" },
  { href: "#faq", label: "FAQ" },
];

export function LandingNav() {
  return (
    <motion.header
      className="fixed inset-x-0 top-0 z-50 border-b border-white/5 bg-night-950/70 backdrop-blur-xl"
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link href="/" className="group flex items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-enchant-violet to-enchant-pink text-lg shadow-glow">
            ✦
          </span>
          <span className="font-display text-lg text-enchant-gold group-hover:text-white">
            SimForge Studio
          </span>
        </Link>
        <nav className="hidden items-center gap-8 text-sm text-white/70 md:flex">
          {LINKS.map((l) => (
            <a key={l.href} href={l.href} className="transition hover:text-enchant-mint">
              {l.label}
            </a>
          ))}
        </nav>
        <Link href="/studio" className="btn-primary text-sm">
          Start creating
        </Link>
      </div>
    </motion.header>
  );
}
