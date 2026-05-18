"use client";

import Link from "next/link";

export function LandingFooter() {
  return (
    <footer className="border-t border-white/5 py-12">
      <div className="mx-auto max-w-6xl px-4 text-center text-sm text-white/45">
        <p className="font-display text-enchant-gold">SimForge Studio</p>
        <p className="mx-auto mt-2 max-w-2xl">
          Independent fan tool · Not affiliated with Electronic Arts, Maxis, or The Sims™
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-6">
          <Link href="/studio" className="hover:text-enchant-mint">
            Workshop
          </Link>
          <a href="#legal" className="hover:text-enchant-mint">
            Legal
          </a>
          <a href="#faq" className="hover:text-enchant-mint">
            FAQ
          </a>
        </div>
        <p className="mt-8 text-xs text-white/30">
          © {new Date().getFullYear()} SimForge Studio. The Sims™ is a trademark of Electronic Arts Inc.
        </p>
      </div>
    </footer>
  );
}
