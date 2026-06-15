/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        clinic: {
          50: "#f3f6fb",
          100: "#e0e9f5",
          200: "#c2d4eb",
          300: "#94b5dc",
          400: "#6492c9",
          500: "#4478b8",
          600: "#3561a0",
          700: "#2d4f85",
          800: "#26426e",
          900: "#1f3559",
        },
        cream: {
          50: "#fffcf8",
          100: "#faf7f2",
          200: "#f3ece3",
          300: "#e8ddd0",
        },
        pet: {
          400: "#e9955f",
          500: "#d97a42",
          600: "#c46835",
        },
      },
      fontFamily: {
        sans: ["DM Sans", "system-ui", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 3px 0 rgb(31 53 89 / 0.06), 0 1px 2px -1px rgb(31 53 89 / 0.06)",
        "card-hover": "0 4px 12px 0 rgb(53 97 160 / 0.14)",
      },
    },
  },
  plugins: [],
};
