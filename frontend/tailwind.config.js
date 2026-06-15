/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        vet: {
          50: "#f5f0fa",
          100: "#e8dcf5",
          200: "#d4c2eb",
          300: "#b89cd9",
          400: "#9b75c9",
          500: "#7f52b8",
          600: "#6a3fa0",
          700: "#563286",
          800: "#43296b",
          900: "#321f52",
        },
        warm: {
          50: "#fff8f5",
          100: "#ffede4",
          200: "#ffddd0",
          300: "#ffc9b5",
        },
        accent: {
          400: "#ff8a65",
          500: "#f4511e",
          600: "#e64a19",
        },
        honey: {
          400: "#ffca28",
          500: "#ffb300",
        },
      },
      fontFamily: {
        sans: ["DM Sans", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 3px 0 rgb(50 31 82 / 0.08), 0 1px 2px -1px rgb(50 31 82 / 0.08)",
        "card-hover": "0 4px 14px 0 rgb(244 81 30 / 0.18)",
      },
    },
  },
  plugins: [],
};
