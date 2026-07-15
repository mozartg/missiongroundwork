/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'brand-green': '#2E5E4E',
        'brand-green-dark': '#1f4539',
        'brand-stone': '#D9CDBA',
        'brand-slate': '#39434D',
        'brand-bg': '#F7F5F2',
        'brand-clay': '#A86E4A',
      },
      fontFamily: {
        fraunces: ['Fraunces', 'serif'],
        inter: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
