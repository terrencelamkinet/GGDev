import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "***REMOVED***eef2ff",
          100: "***REMOVED***e0e7ff",
          200: "***REMOVED***c7d2fe",
          300: "***REMOVED***a5b4fc",
          400: "***REMOVED***818cf8",
          500: "***REMOVED***6366f1",
          600: "***REMOVED***4f46e5",
          700: "***REMOVED***4338ca",
          800: "***REMOVED***3730a3",
          900: "***REMOVED***312e81",
          950: "***REMOVED***1e1b4b",
        },
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
