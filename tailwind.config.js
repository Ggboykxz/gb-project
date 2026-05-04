/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1B4F72',
          foreground: '#FFFFFF',
        },
        secondary: {
          DEFAULT: '#F39C12',
          foreground: '#000000',
        },
        success: {
          DEFAULT: '#27AE60',
          foreground: '#FFFFFF',
        },
        background: {
          light: '#F8F9FA',
          dark: '#1A1D23',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        heading: ['Sora', 'system-ui', 'sans-serif'],
        mono: ['Geist Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
