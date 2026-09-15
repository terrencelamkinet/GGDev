/** @type {import('tailwindcss').Config} */
export default {
  theme: {
    extend: {
    colors: {
        primary: {
            '50': 'hsl(280, 68%, 97%)',
            '100': 'hsl(280, 68%, 94%)',
            '200': 'hsl(280, 68%, 86%)',
            '300': 'hsl(280, 68%, 76%)',
            '400': 'hsl(280, 68%, 64%)',
            '500': 'hsl(280, 68%, 50%)',
            '600': 'hsl(280, 68%, 40%)',
            '700': 'hsl(280, 68%, 32%)',
            '800': 'hsl(280, 68%, 24%)',
            '900': 'hsl(280, 68%, 16%)',
            '950': 'hsl(280, 68%, 10%)',
            DEFAULT: '#af52de'
        },
        secondary: {
            '50': 'hsl(241, 61%, 97%)',
            '100': 'hsl(241, 61%, 94%)',
            '200': 'hsl(241, 61%, 86%)',
            '300': 'hsl(241, 61%, 76%)',
            '400': 'hsl(241, 61%, 64%)',
            '500': 'hsl(241, 61%, 50%)',
            '600': 'hsl(241, 61%, 40%)',
            '700': 'hsl(241, 61%, 32%)',
            '800': 'hsl(241, 61%, 24%)',
            '900': 'hsl(241, 61%, 16%)',
            '950': 'hsl(241, 61%, 10%)',
            DEFAULT: '#5856d6'
        },
        accent: {
            '50': 'hsl(3, 100%, 97%)',
            '100': 'hsl(3, 100%, 94%)',
            '200': 'hsl(3, 100%, 86%)',
            '300': 'hsl(3, 100%, 76%)',
            '400': 'hsl(3, 100%, 64%)',
            '500': 'hsl(3, 100%, 50%)',
            '600': 'hsl(3, 100%, 40%)',
            '700': 'hsl(3, 100%, 32%)',
            '800': 'hsl(3, 100%, 24%)',
            '900': 'hsl(3, 100%, 16%)',
            '950': 'hsl(3, 100%, 10%)',
            DEFAULT: '#ff3b30'
        },
        'neutral-50': '#3c3c43',
        'neutral-100': '#000000',
        'neutral-200': '#ffffff',
        'neutral-300': '#787880',
        'neutral-400': '#e5e5ea',
        'neutral-500': '#f2f2f7',
        'neutral-600': '#c6c6c8',
        background: '#f2f2f7',
        foreground: '#000000'
    },
    fontFamily: {
        body: [
            'Times New Roman',
            'sans-serif'
        ]
    },
    fontSize: {
        '9': [
            '9px',
            {
                lineHeight: 'normal'
            }
        ],
        '10': [
            '10px',
            {
                lineHeight: 'normal',
                letterSpacing: '0.5px'
            }
        ],
        '11': [
            '11px',
            {
                lineHeight: 'normal',
                letterSpacing: '0.5px'
            }
        ],
        '12': [
            '12px',
            {
                lineHeight: '16.2px'
            }
        ],
        '13': [
            '13px',
            {
                lineHeight: 'normal'
            }
        ],
        '15': [
            '15px',
            {
                lineHeight: 'normal'
            }
        ],
        '16': [
            '16px',
            {
                lineHeight: 'normal'
            }
        ],
        '17': [
            '17px',
            {
                lineHeight: '22.1px'
            }
        ],
        '18': [
            '18px',
            {
                lineHeight: 'normal'
            }
        ],
        '20': [
            '20px',
            {
                lineHeight: 'normal'
            }
        ],
        '24': [
            '24px',
            {
                lineHeight: 'normal'
            }
        ],
        '28': [
            '28px',
            {
                lineHeight: '33.6px'
            }
        ]
    },
    spacing: {
        '5': '20px',
        '8': '32px',
        '12': '48px',
        '111': '444px',
        '1px': '1px',
        '27px': '27px'
    },
    borderRadius: {
        md: '10px',
        lg: '13px',
        full: '999px'
    },
    boxShadow: {
        sm: 'rgb(175, 82, 222) 0px 0px 8px 0px'
    },
    transitionDuration: {
        '150': '0.15s',
        '200': '0.2s'
    },
    container: {
        center: true,
        padding: '0px'
    },
    maxWidth: {
        container: '393px'
    }
},
  },
};
