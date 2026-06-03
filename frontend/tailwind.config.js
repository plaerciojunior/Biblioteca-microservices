/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.html',
    './**/*.razor',
  ],
  theme: {
    extend: {
      colors: {
        "surface-bright": "#fef7fe",
        "primary-fixed-dim": "#d6baff",
        "outline": "#7b7580",
        "on-background": "#1d1b1f",
        "background": "#FFF8ED", 
        "primary-container": "#D1B3FF", 
        "secondary-container": "#FFB7C5",
        "surface-container-lowest": "#FFF8ED", 
        "surface-container-low": "#FFF8ED",
        "surface-variant": "#e7e0e7",
        "on-surface": "#1d1b1f",
        "on-surface-variant": "#4a454f",
        "error": "#ba1a1a",
        "secondary": "#864e5a"
      },
      borderRadius: { "DEFAULT": "0px", "lg": "0px", "xl": "0px", "full": "0px" },
      spacing: { 
          "gutter": "24px", 
          "unit": "8px", 
          "container-max": "1536px",
          "margin-mobile": "16px",
          "margin-desktop": "40px",
          "shadow-offset": "5px",
          "border-width": "2px"
      },
      fontFamily: {
        "headline-lg": ["Hanken Grotesk"],
        "headline-md": ["Hanken Grotesk"],
        "body-md": ["Hanken Grotesk"],
        "body-lg": ["Hanken Grotesk"],
        "label-md": ["Space Grotesk"],
        "label-sm": ["Space Grotesk"]
      },
      backgroundImage: {
        'grid-pattern': 'linear-gradient(to right, #e7e0e7 1px, transparent 1px), linear-gradient(to bottom, #e7e0e7 1px, transparent 1px)'
      }
    }
  }
}