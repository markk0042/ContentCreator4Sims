"use client";

import { CreationTypes } from "./CreationTypes";
import { FAQ } from "./FAQ";
import { FinalCTA } from "./FinalCTA";
import { FreeTrial } from "./FreeTrial";
import { Gallery } from "./Gallery";
import { Hero } from "./Hero";
import { HowItWorks } from "./HowItWorks";
import { LandingFooter } from "./LandingFooter";
import { LandingNav } from "./LandingNav";
import { LegalSection } from "./LegalSection";
import { Pricing } from "./Pricing";

export function LandingPage() {
  return (
    <div className="landing-bg min-h-screen">
      <LandingNav />
      <Hero />
      <HowItWorks />
      <CreationTypes />
      <FreeTrial />
      <Pricing />
      <Gallery />
      <FAQ />
      <LegalSection />
      <FinalCTA />
      <LandingFooter />
    </div>
  );
}
