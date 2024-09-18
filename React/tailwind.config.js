/** @type {import('tailwindcss').Config} */

import flowbite from "flowbite-react/tailwind";

export default {
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

      }
    },
  },
  plugins: [
    flowbite.plugin(),
  ],
}

