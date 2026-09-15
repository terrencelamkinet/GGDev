# Inputs — AI Agent Instruction Spec
> Reference: Apple HIG — Inputs
> Covers: Touch, Keyboard, Apple Pencil, Game Controllers, Pointer (Mouse/Trackpad), Eye Tracking, Action Button, Digital Crown, Remote & Siri Remote

---

## Input Method Overview

| Input Method | Platform | Primary Use |
|-------------|----------|-------------|
| Touch | iOS, iPadOS | Tap, swipe, pinch, rotate — primary mobile input |
| Keyboard | iOS, iPadOS, macOS | Text entry, keyboard shortcuts |
| Apple Pencil | iPadOS | Precise drawing, annotation, handwriting |
| Game Controller | iOS, iPadOS, macOS, tvOS | Gaming, media navigation |
| Pointer (Mouse/Trackpad) | iPadOS, macOS | Cursor navigation, hover, right-click |
| Eye Tracking | iOS (accessibility) | Pointer control for motor disabilities |
| Action Button | iPhone 15 Pro+ | Customizable hardware shortcut |
| Digital Crown | watchOS | Scroll, zoom, value adjustment |
| Apple TV Remote | tvOS | Focus navigation, swipe, click |
| Voice (Siri) | All platforms | Voice commands, app intents |

---

## 1. Touch (iOS / iPadOS)

### Touch Gesture Library
| Gesture | Action | System Use |
|---------|--------|-----------|
| Tap | Primary selection | Button press, item selection |
| Double-tap | Secondary action | Zoom in, text selection |
| Long press | Contextual menu / pick up | Drag initiation, context menu |
| Swipe (directional) | Navigate, reveal, dismiss | Back navigation, swipe actions |
| Pinch | Scale content | Zoom in/out on maps, photos |
| Rotate | Rotate content | Image rotation |
| Pan / Drag | Move content | Scroll, drag-and-drop |
| Edge swipe (left) | Navigate back | System back gesture |

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| TCH-001 | Design for **thumb-first** interaction — primary actions in the bottom 60% of screen. |
| TCH-002 | Minimum touch target: **44×44pt** — pad small icons with invisible hit area. |
| TCH-003 | Never override system swipe-from-left-edge (back navigation) gesture. |
| TCH-004 | System swipe-from-bottom-edge (home indicator) cannot be blocked. |
| TCH-005 | Multi-touch gestures must have a single-touch fallback (accessibility). |
| TCH-006 | Provide `UILongPressGestureRecognizer` for context menus on content items. |
| TCH-007 | Avoid requiring complex multi-finger gestures for primary actions. |
| TCH-008 | Touch feedback: visual state change must occur within **100ms** of touch. |

### One-Handed Reach Zone Design
```
iPhone 14/15 Layout (Portrait):
┌─────────────────────┐
│ ░░░░░░░░░░░░░░░░░░░ │  ← Difficult zone (thumbs rarely reach)
│ ░░░░░░░░░░░░░░░░░░░ │
│ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ │  ← Moderate zone
│ ████████████████████ │  ← Easy zone (primary actions here)
│ ████████████████████ │
│ [──────────────────] │  ← Tab bar / bottom actions
└─────────────────────┘
```

---

## 2. Keyboard (iOS / iPadOS / macOS)

### Keyboard Types
| `UIKeyboardType` | Use Case |
|-----------------|----------|
| `.default` | General text input |
| `.emailAddress` | Email fields |
| `.URL` | URL / web address fields |
| `.numberPad` | Numeric-only input (no decimal) |
| `.decimalPad` | Numeric with decimal point |
| `.phonePad` | Phone number input |
| `.namePhonePad` | Name or phone |

### Text Content Types (AutoFill)
| `UITextContentType` | AutoFill Behavior |
|--------------------|------------------|
| `.username` | Credential username |
| `.password` | Password with keychain |
| `.newPassword` | Strong password suggestion |
| `.oneTimeCode` | SMS OTP auto-fill |
| `.emailAddress` | Email address fill |
| `.telephoneNumber` | Phone number fill |
| `.fullStreetAddress` | Address fill from Contacts |

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| KBD-001 | Use `textContentType` on all input fields for AutoFill integration. |
| KBD-002 | Use `keyboardType` appropriate to the expected input for each field. |
| KBD-003 | Handle `UIResponder.resignFirstResponder()` when tapping outside a text field. |
| KBD-004 | Adjust scroll view content inset when keyboard appears — use `keyboardLayoutGuide`. |
| KBD-005 | Provide `returnKeyType` (`.next`, `.done`, `.search`, `.go`) appropriate to context. |
| KBD-006 | macOS / iPadOS with keyboard: implement all critical app functions as **keyboard shortcuts**. |
| KBD-007 | Register keyboard shortcuts with `UIKeyCommand` / `.keyboardShortcut()` modifier. |
| KBD-008 | Respect hardware keyboard presence on iPad — do not show soft keyboard redundantly. |

### Essential Keyboard Shortcuts (macOS / iPadOS)
| Shortcut | Action |
|----------|--------|
| `Cmd+N` | New item |
| `Cmd+S` | Save |
| `Cmd+Z` | Undo |
| `Cmd+Shift+Z` | Redo |
| `Cmd+C / V / X` | Copy / Paste / Cut |
| `Cmd+F` | Find / Search |
| `Cmd+W` | Close window/tab |
| `Cmd+Q` | Quit app (macOS) |
| `Cmd+,` | Open preferences (macOS) |

---

## 3. Apple Pencil (iPadOS)

### Pencil Input Capabilities
| Feature | Pencil Gen | Description |
|---------|-----------|-------------|
| Pressure sensitivity | 1st, 2nd, Pro | 4096 levels of pressure |
| Tilt detection | 1st, 2nd, Pro | Azimuth + altitude angle |
| Double-tap | 2nd, Pro | Switch tool action |
| Squeeze | Pro | Contextual action trigger |
| Barrel roll | Pro | Tool rotation |
| Low latency (ProMotion) | All (120Hz iPad) | 9ms latency on ProMotion displays |

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| PCL-001 | Use `PKCanvasView` (PencilKit) for drawing — do not build a custom canvas unless required. |
| PCL-002 | Support palm rejection when Pencil is the active input. |
| PCL-003 | Register double-tap action via `UIPencilInteraction` — common use: switch between draw and erase. |
| PCL-004 | Provide a fallback touch-based tool when Pencil is unavailable. |
| PCL-005 | Scribble: support `UIScribbleInteraction` for handwriting-to-text in all text fields. |
| PCL-006 | Hover preview (Pencil Pro): show tool preview before touch contact using `UIPencilHoverPoseInteraction`. |

---

## 4. Game Controllers

### Controller Support
| Controller Type | Framework | Notes |
|---------------|-----------|-------|
| MFi Extended | `GameController` | Standard L/R sticks, triggers, ABXY, bumpers |
| Xbox Controller | `GameController` | Direct support iOS 13+ |
| PlayStation DualShock/DualSense | `GameController` | Direct support iOS 14+ |
| Apple TV Remote | `GameController` | Basic D-pad input |

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| GCT-001 | Support `GCController.controllers()` — detect connected controllers on app launch and during session. |
| GCT-002 | Always provide **on-screen touch controls** as a fallback when no controller is connected. |
| GCT-003 | Show controller button glyphs using SF Symbols (`.gamecontroller.*` symbol set). |
| GCT-004 | Support button remapping via system settings — do not enforce fixed button layouts. |
| GCT-005 | Respond to `GCController.controllerDidConnectNotification` to dynamically update UI. |
| GCT-006 | Test with: MFi controller, Xbox controller, and PlayStation controller for cross-compatibility. |

---

## 5. Pointer (Mouse / Trackpad) — iPadOS / macOS

### Pointer Interaction Types
| Type | Behavior | Use When |
|------|----------|----------|
| `.highlight` | Highlights element, pointer morphs | Buttons, links |
| `.lift` | Element lifts toward pointer | Cards, icons |
| `.hover` | Custom hover region | Custom interactive areas |
| `.automatic` | System-inferred behavior | Default |

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| PTR-001 | iPadOS: add `UIPointerInteraction` to interactive elements for visual cursor feedback. |
| PTR-002 | macOS: implement hover states (`onHover {}`) for all interactive elements. |
| PTR-003 | Right-click (secondary click) must trigger context menu — use `.contextMenu {}`. |
| PTR-004 | Scroll wheel / trackpad: two-finger scroll must work natively in all scroll views. |
| PTR-005 | Pinch gesture on trackpad must mirror touch pinch behavior (zoom). |
| PTR-006 | Avoid relying on hover-only states for critical functionality — touch users won't see them. |

---

## 6. Eye Tracking (Accessibility — iOS)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| EYT-001 | Eye Tracking uses `UIPointerInteraction` automatically — ensure all interactive elements are accessible via pointer. |
| EYT-002 | All interactive elements must be focusable with appropriate `accessibilityFrame`. |
| EYT-003 | Avoid small or clustered interactive elements — spacing is critical for accurate eye targeting. |
| EYT-004 | Test with AssistiveTouch in pointer mode to simulate eye tracking behavior. |

---

## 7. Action Button (iPhone 15 Pro+)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| ACB-001 | Register app-specific actions via `AppIntents` framework for system Action Button assignment. |
| ACB-002 | Action Button actions must be **single, discrete actions** — not menus. |
| ACB-003 | Common use cases: Quick Note, Toggle Feature, Launch Specific Screen, Trigger Shortcut. |
| ACB-004 | App Action Button intents should complete quickly (< 1 second) with haptic confirmation. |

---

## 8. Digital Crown (watchOS)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| CRN-001 | Map Digital Crown rotation to the primary scrollable content on every screen. |
| CRN-002 | Use `focusable()` + `.digitalCrownRotation()` modifier on scrollable views. |
| CRN-003 | Crown press = back/home navigation (system behavior — do not override). |
| CRN-004 | Support haptic feedback on crown detents using `.digitalCrownRotation(detents:)`. |

---

## 9. Apple TV Remote / Siri Remote

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| RMT-001 | All interactive elements must be **focusable** via `isFocusable = true`. |
| RMT-002 | Use `TVUIKit` or SwiftUI focus engine — never build custom focus management. |
| RMT-003 | Swipe gestures on Touch surface: map to scroll/pan in the active content area. |
| RMT-004 | Menu button: navigate back or dismiss modals — never override for other actions. |
| RMT-005 | Design for **10-foot UI**: large text (minimum 24pt), high contrast, simple layouts. |

