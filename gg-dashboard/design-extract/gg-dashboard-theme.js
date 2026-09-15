// React Theme — extracted from http://localhost:7870
// Compatible with: Chakra UI, Stitches, Vanilla Extract, or any CSS-in-JS

/**
 * TypeScript type definition for this theme:
 *
 * interface Theme {
 *   colors: {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    foreground: string;
    neutral50: string;
    neutral100: string;
    neutral200: string;
    neutral300: string;
    neutral400: string;
    neutral500: string;
    neutral600: string;
 *   };
 *   fonts: {
    body: string;
    mono: string;
 *   };
 *   fontSizes: {
    '9': string;
    '10': string;
    '11': string;
    '12': string;
    '13': string;
    '15': string;
    '16': string;
    '17': string;
    '18': string;
    '20': string;
    '24': string;
    '28': string;
 *   };
 *   space: {
    '1': string;
    '20': string;
    '27': string;
    '32': string;
    '48': string;
    '444': string;
 *   };
 *   radii: {
    md: string;
    lg: string;
    full: string;
 *   };
 *   shadows: {
    sm: string;
 *   };
 *   states: {
 *     hover: { opacity: number };
 *     focus: { opacity: number };
 *     active: { opacity: number };
 *     disabled: { opacity: number };
 *   };
 * }
 */

export const theme = {
  "colors": {
    "primary": "#af52de",
    "secondary": "#5856d6",
    "accent": "#ff3b30",
    "background": "#f2f2f7",
    "foreground": "#000000",
    "neutral50": "#3c3c43",
    "neutral100": "#000000",
    "neutral200": "#ffffff",
    "neutral300": "#787880",
    "neutral400": "#e5e5ea",
    "neutral500": "#f2f2f7",
    "neutral600": "#c6c6c8"
  },
  "fonts": {
    "body": "'Times New Roman', sans-serif",
    "mono": "'SF Mono', monospace"
  },
  "fontSizes": {
    "9": "9px",
    "10": "10px",
    "11": "11px",
    "12": "12px",
    "13": "13px",
    "15": "15px",
    "16": "16px",
    "17": "17px",
    "18": "18px",
    "20": "20px",
    "24": "24px",
    "28": "28px"
  },
  "space": {
    "1": "1px",
    "20": "20px",
    "27": "27px",
    "32": "32px",
    "48": "48px",
    "444": "444px"
  },
  "radii": {
    "md": "10px",
    "lg": "13px",
    "full": "999px"
  },
  "shadows": {
    "sm": "rgb(175, 82, 222) 0px 0px 8px 0px"
  },
  "states": {
    "hover": {
      "opacity": 0.08
    },
    "focus": {
      "opacity": 0.12
    },
    "active": {
      "opacity": 0.16
    },
    "disabled": {
      "opacity": 0.38
    }
  }
};

// MUI v5 theme
export const muiTheme = {
  "palette": {
    "primary": {
      "main": "#af52de",
      "light": "hsl(280, 68%, 75%)",
      "dark": "hsl(280, 68%, 45%)"
    },
    "secondary": {
      "main": "#5856d6",
      "light": "hsl(241, 61%, 74%)",
      "dark": "hsl(241, 61%, 44%)"
    },
    "background": {
      "default": "#f2f2f7",
      "paper": "#f2f2f7"
    },
    "text": {
      "primary": "#000000",
      "secondary": "#ffffff"
    }
  },
  "typography": {
    "fontFamily": "'Arial', sans-serif",
    "h2": {
      "fontSize": "24px",
      "fontWeight": "400",
      "lineHeight": "normal"
    },
    "h3": {
      "fontSize": "20px",
      "fontWeight": "700",
      "lineHeight": "normal"
    },
    "body1": {
      "fontSize": "16px",
      "fontWeight": "400",
      "lineHeight": "normal"
    }
  },
  "shape": {
    "borderRadius": 10
  },
  "shadows": [
    "rgb(175, 82, 222) 0px 0px 8px 0px"
  ]
};

export default theme;
