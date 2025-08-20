/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0f0f0f',
        secondary: '#1a1a1a',
        accent: '#2d2d2d',
        highlight: '#3d3d3d',
        'text-primary': '#ffffff',
        'text-secondary': '#b0b0b0',
        border: '#404040',
        success: '#00ff88',
        warning: '#ff6b35',
        info: '#00b4d8',
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #2d2d2d 100%)',
        'gradient-card': 'linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%)',
      },
      boxShadow: {
        'dark': '0 8px 32px rgba(0, 0, 0, 0.8)',
        'light': '0 4px 16px rgba(255, 255, 255, 0.1)',
        'glow-green': '0 0 20px rgba(0, 255, 136, 0.3)',
        'glow-blue': '0 0 20px rgba(0, 180, 216, 0.3)',
      }
    },
  },
  plugins: [],
};