import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        night: {
          950: "#0f0a1a",
          900: "#1a1028",
          800: "#2a1a42",
        },
        enchant: {
          gold: "#e8c547",
          pink: "#f4a4d0",
          mint: "#7ee0c9",
          violet: "#9b6dff",
        },
      },
      fontFamily: {
        display: ["Georgia", "Cambria", "Times New Roman", "serif"],
        body: ["Segoe UI", "system-ui", "sans-serif"],
      },
      boxShadow: {
        glow: "0 0 40px rgba(155, 109, 255, 0.35)",
        gold: "0 0 24px rgba(232, 197, 71, 0.25)",
      },
    },
  },
  plugins: [],
};

export default config;
