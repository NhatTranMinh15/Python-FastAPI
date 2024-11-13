/** @type {import('tailwindcss').Config} */

import flowbite from "flowbite-react/tailwind";

export default {
  darkMode: 'selector',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    flowbite.content(),
  ],
  theme: {
    extend: {
      margin: {
        half: '50%'
      },
      inset: {
        '40%': '40%',
        half: '50%'
      },
      maxWidth: {
        "30ch": '30ch',
        "99%": "99%"
      },
      flexBasis: {

      },
      colors: {
        "gray-400-opaque-40": "#9ca3b066",
        "slate-200-opaque-40": "#e2e8f066",
        "rich-black": "#090909",
        "dark-lime-green": "#001500",
        "charleston-green": "#232B2B",
        "bright-gray": "#5F6062",
        "almond": "#EBE5D5",
        "dark-spring-green": "#19643F",
        "traditional-forest-green": "#0A5027",
        "white-smoke": "#f5f5f5",
        "white-chocolate": "#EBE5D5",
        "palm-leaf": "#759A3F",
        "eerie-black": "#020202",
        "dark-jungle-green": "#0D2818",
        "dark-green": "#04471C",
        "green-munsell": "#0A9548",
        "malachite": "#16DB65",
        "tea-green": "#bfffbf40",
      }
    },
  },
  plugins: [
    flowbite.plugin(),
  ],
}

