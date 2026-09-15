# Foundations — AI Agent Instruction Spec
> Reference: Apple HIG — Foundations
> Covers: Accessibility, Color, Dark Mode, Icons, Images, Layout, Materials, Motion, Privacy, SF Symbols, Typography

---

## 1. Accessibility

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| ACC-001 | All interactive elements must have `accessibilityLabel` — descriptive action labels, not control type names. |
| ACC-002 | Minimum touch target: **44×44pt** for all tappable controls. |
| ACC-003 | Text contrast ratio: **4.5:1** for body text; **3:1** for large text (18pt+ regular or 14pt+ bold). |
| ACC-004 | Support Dynamic Type — use semantic text styles; never hardcode font sizes. |
| ACC-005 | Respect `UIAccessibility.isReduceMotionEnabled` — replace animations with cross-fades. |
| ACC-006 | VoiceOver reading order must match visual reading order (left-to-right, top-to-bottom). |
| ACC-007 | Never communicate state using color alone — always pair with a label, icon, or pattern. |
| ACC-008 | Support `UIAccessibility.isReduceTransparencyEnabled` for material/blur backgrounds. |
| ACC-009 | Use `accessibilityHint` to describe the result of an interaction when label alone is insufficient. |
| ACC-010 | Test with Accessibility Inspector (Xcode) before every QA cycle. |

---

## 2. Color

### Color System
```
Semantic (Adaptive) Colors   → Automatically adapt to Light/Dark Mode
System Colors                → Apple-defined palette (red, blue, green, etc.)
Custom Colors                → App-specific, must be defined for both modes
```

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| CLR-001 | Use **semantic color tokens** (`.label`, `.secondaryLabel`, `.systemBackground`, `.systemFill`) — never hardcode hex values for UI chrome. |
| CLR-002 | Define custom colors in **Asset Catalog** with Light and Dark Mode variants. |
| CLR-003 | Limit palette: 1 primary brand color, 1 accent/interactive color, semantic neutrals. |
| CLR-004 | Never use color as the sole indicator of state (error, success, warning). |
| CLR-005 | Test all color combinations with **color blindness simulators** (protanopia, deuteranopia, tritanopia). |
| CLR-006 | Tint color (accent): use consistently for interactive elements (links, buttons, toggles). |

### System Color Palette Reference
| Token | Light Mode | Dark Mode | Use Case |
|-------|-----------|-----------|----------|
| `.systemBackground` | White | Black | Primary container |
| `.secondarySystemBackground` | Light Gray | Dark Gray | Secondary surfaces |
| `.label` | Black | White | Primary text |
| `.secondaryLabel` | Gray | Light Gray | Secondary/meta text |
| `.systemBlue` | #007AFF | #0A84FF | Tint / interactive |
| `.systemRed` | #FF3B30 | #FF453A | Destructive / error |
| `.systemGreen` | #34C759 | #30D158 | Success / positive |

---

## 3. Dark Mode

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| DRK-001 | Support Dark Mode natively using semantic color tokens (automatic adaptation). |
| DRK-002 | Test every screen in both Light and Dark modes before releasing. |
| DRK-003 | Images and icons should have Dark Mode variants if they contain embedded color. |
| DRK-004 | Do NOT invert images or photos for Dark Mode — only invert UI chrome. |
| DRK-005 | Materials (blur, vibrancy) automatically adapt — prefer them over solid fills. |

---

## 4. Icons

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| ICN-001 | App Icon: must be provided at 1024×1024pt (App Store) — system scales down automatically. |
| ICN-002 | App Icon must not contain transparency; use solid background. |
| ICN-003 | In-app icons: **always use SF Symbols** before creating custom icons. |
| ICN-004 | SF Symbols must be used with matching weight to surrounding text (`.font(.body)` → symbol `.body` scale). |
| ICN-005 | Custom icons must follow SF Symbol grid and optical balance. |
| ICN-006 | Icons should be universally understood — avoid locale-specific metaphors. |

---

## 5. Images & Media

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| IMG-001 | Provide images at 1x, 2x, and 3x resolutions in Asset Catalog. |
| IMG-002 | Use `contentMode: .scaleAspectFit` or `.scaleAspectFill` — never distort images. |
| IMG-003 | All images must have `accessibilityLabel` or be marked `isAccessibilityElement = false` if decorative. |
| IMG-004 | Support Dark Mode image variants in Asset Catalog for images with embedded color/text. |
| IMG-005 | Video content must support captions/subtitles. |

---

## 6. Layout

### Grid System
```
Base Unit:      8pt
Margin:         16pt (compact), 20pt (regular/iPad)
Gutter:         8pt between columns
Safe Areas:     Top (status bar), Bottom (home indicator), Leading/Trailing (notch)
```

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| LAY-001 | Use the **8pt grid** for all spacing values (8, 16, 24, 32, 40...). |
| LAY-002 | Respect `safeAreaInsets` — never place content under the notch, Dynamic Island, or home indicator. |
| LAY-003 | Use `LazyVStack` / `LazyHStack` for long scrolling lists — never load all cells eagerly. |
| LAY-004 | Support all iPhone/iPad screen sizes — use adaptive layouts with `GeometryReader` or Auto Layout. |
| LAY-005 | Use `ScrollView` for content that may exceed the viewport — never truncate content without scroll. |
| LAY-006 | Avoid hardcoded pixel values for padding/sizing — use relative / adaptive units. |

---

## 7. Materials (Blur / Vibrancy)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| MAT-001 | Use system materials (`.regularMaterial`, `.thinMaterial`, `.ultraThinMaterial`) for overlay surfaces. |
| MAT-002 | Materials automatically adapt to Light/Dark Mode and accessibility settings — prefer over custom blurs. |
| MAT-003 | Use vibrancy effects for text or icons layered on materials for legibility. |
| MAT-004 | Avoid stacking multiple translucent layers — creates visual noise and performance issues. |

---

## 8. Motion & Animation

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| MOT-001 | All animations must have a **purpose** — communicate state change, guide attention, or provide feedback. |
| MOT-002 | Default animation duration: **0.25–0.35s** for transitions; **0.15s** for micro-interactions. |
| MOT-003 | Use spring animations (`withSpring`) for natural feel — avoid linear for UI motion. |
| MOT-004 | Always check `UIAccessibility.isReduceMotionEnabled` — provide static/fade alternatives. |
| MOT-005 | Never use looping animations that distract from content. |
| MOT-006 | Page transitions: use system defaults unless a custom transition serves a clear UX purpose. |

---

## 9. Privacy

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| PRV-001 | Request permissions **only when needed** and provide a clear usage explanation (purpose string). |
| PRV-002 | Request permission at first-use, not at app launch. |
| PRV-003 | If the user denies a permission, gracefully degrade the feature — do not block the app. |
| PRV-004 | Never store sensitive data in `UserDefaults` — use `Keychain` for credentials/tokens. |
| PRV-005 | Implement App Tracking Transparency (ATT) if using cross-app tracking. |
| PRV-006 | Privacy Nutrition Labels in App Store must accurately reflect all data collection. |

---

## 10. SF Symbols

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| SFS-001 | Use SF Symbols as the default icon library — 6,000+ symbols available. |
| SFS-002 | Symbols inherit the font size and weight of surrounding text automatically. |
| SFS-003 | Use rendering modes: `.monochrome`, `.hierarchical`, `.palette`, or `.multicolor` as appropriate. |
| SFS-004 | For custom icons, follow the SF Symbol design grid (baseline, cap height, optical bounds). |
| SFS-005 | Symbols respond to Dynamic Type, Bold Text, and accessibility scaling automatically. |

---

## 11. Typography

### Type Scale (Dynamic Type)
| Text Style | Default Size | Use Case |
|------------|-------------|----------|
| `.largeTitle` | 34pt | Hero headers, screen titles |
| `.title` | 28pt | Section headers |
| `.title2` | 22pt | Sub-section headers |
| `.title3` | 20pt | Card titles |
| `.headline` | 17pt (semibold) | List item primary labels |
| `.body` | 17pt | Primary content text |
| `.callout` | 16pt | Emphasized secondary text |
| `.subheadline` | 15pt | Supporting information |
| `.footnote` | 13pt | Metadata, timestamps |
| `.caption` | 12pt | Image captions |
| `.caption2` | 11pt | Micro labels |

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| TYP-001 | Always use Dynamic Type semantic styles — never hardcode `font(.system(size: 17))`. |
| TYP-002 | Default system font: **SF Pro** (iOS/macOS). Use `.font(.system(.body))` for automatic selection. |
| TYP-003 | Line height must accommodate accessibility font scaling (up to 310% of default). |
| TYP-004 | Text alignment: left-aligned for body text; center only for short headings or CTAs. |
| TYP-005 | Minimum contrast ratio for text: 4.5:1 (body), 3:1 (large text). |

