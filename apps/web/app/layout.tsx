import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SimForge Studio — Turn your artwork into Sims 4 custom content",
  description:
    "Independent fan tool for template-based Sims 4 CC. Upload art, download .package files for PC. Not affiliated with EA or Maxis.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
