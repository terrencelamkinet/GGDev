# Designing for Platforms — AI Agent Instruction Spec
> Reference: Apple HIG — "Designing for iOS / Game / Desktop"

---

## 1. Designing for iOS

### Platform Context
- Primary input: **Touch** (finger, thumb gestures)
- Screen form: Portrait-dominant; supports landscape
- Navigation paradigm: Stack-based, tab-based, or content-driven

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| IOS-001 | Default to portrait layout; support landscape where content benefits (video, maps). |
| IOS-002 | Use `NavigationStack` + `TabView` as the primary structural pattern. |
| IOS-003 | Respect safe area insets on all sides — never place interactive elements in notch/home indicator zones. |
| IOS-004 | Minimum tap target: 44×44 points for all interactive controls. |
| IOS-005 | Design for one-handed use when possible; place primary actions in thumb-reachable zones (bottom half of screen). |
| IOS-006 | Support system gestures: swipe-to-go-back (NavigationStack), swipe-to-dismiss (sheets). Never override these without explicit reason. |
| IOS-007 | Font: SF Pro (system default). Never use a fixed font size — use Dynamic Type semantic styles (`.body`, `.headline`, `.caption`). |
| IOS-008 | Support both Light Mode and Dark Mode using semantic color tokens. |
| IOS-009 | Use standard iOS transitions: push (navigation), slide-up (sheets), fade (modals). |
| IOS-010 | Status bar: always use system-managed. Never occlude with custom overlays. |

### Screen Density & Layout Grid
- Base grid: **8pt grid system**
- Margins: 16pt (compact), 20pt (regular)
- Maximum content width on iPad: 680pt (centered)

### Adaptive Layouts (iPhone → iPad)
```
Compact Width (iPhone):    Single-column, TabView navigation
Regular Width (iPad):      Two-column split view or sidebar navigation
```

### Key UIKit / SwiftUI APIs
- `UINavigationController` / `NavigationStack`
- `UITabBarController` / `TabView`
- `UIScrollView` / `ScrollView`
- `UITableView` / `List`
- `UISplitViewController` / `NavigationSplitView`

---

## 2. Designing for Game (iOS / macOS / tvOS)

### Platform Context
- Input: Touch, Game Controller, Keyboard+Mouse (macOS), Apple TV Remote
- Experience: Immersive, full-screen, real-time interaction
- Key challenge: Avoiding system UI interference during gameplay

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| GAME-001 | Games should run full-screen with all system chrome hidden during active gameplay. |
| GAME-002 | Use `preferredScreenEdgesDeferringSystemGestures` to protect swipe areas critical to gameplay. |
| GAME-003 | Support MFi Game Controllers via `GameController` framework. Provide on-screen controls as fallback. |
| GAME-004 | All UI elements (HUD, menus) must use readable contrast ratios even against complex backgrounds. |
| GAME-005 | Pause game state when app is backgrounded or interrupted (phone call, notification). |
| GAME-006 | Support Game Center for leaderboards and achievements where applicable. |
| GAME-007 | Use `Metal` or `RealityKit` for rendering; avoid UIKit for game-loop-critical rendering. |
| GAME-008 | Audio: respect system silent mode for non-essential sounds; critical game audio may override. |
| GAME-009 | Provide haptic feedback using `UIImpactFeedbackGenerator` for impactful in-game events. |
| GAME-010 | For tvOS games: design for focus-based navigation; all interactive elements must be focusable. |

### Game UI Layout Zones
```
Safe Zone (Content):    Central 85% of screen — game world, characters
HUD Zone (Overlay):     Corners and edges — score, health, minimap
Menu Zone (Modal):      Full-screen overlay — pause, settings, leaderboard
```

### Accessibility in Games
- Provide subtitle/caption support for narrative content
- Allow remapping of game controls
- Support "Reduce Motion" — provide alternative camera/transition options

---

## 3. Designing for Desktop (macOS)

### Platform Context
- Primary input: **Mouse/Trackpad** + **Keyboard**
- Window management: Resizable, multi-window, full-screen
- Key paradigm: Menu bar, toolbar, sidebar, content area

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| MAC-001 | Structure app using Menu Bar + Toolbar + Sidebar + Content Area pattern. |
| MAC-002 | All destructive actions must have an undo mechanism (`Cmd+Z`). |
| MAC-003 | Support keyboard shortcuts for all primary actions; document them in the Help menu. |
| MAC-004 | Design hover states for all interactive elements — desktop users expect cursor feedback. |
| MAC-005 | Windows must be resizable; content must reflow gracefully from compact to expanded width. |
| MAC-006 | Use `NSToolbar` / SwiftUI `toolbar` for window-level actions (not navigation). |
| MAC-007 | Use `NSSplitViewController` / `NavigationSplitView` for sidebar + detail layouts. |
| MAC-008 | Contextual menus (right-click) must be available for all interactive content items. |
| MAC-009 | Support copy-paste, drag-and-drop for all content types natively. |
| MAC-010 | Respect system-level Dark Mode, accent color, and accessibility contrast preferences. |

### Desktop Layout Anatomy
```
┌─────────────────────────────────────────┐
│  Menu Bar (System-managed)              │
├─────────────────────────────────────────┤
│  Toolbar (App actions, search)          │
├──────────┬──────────────────────────────┤
│          │                              │
│ Sidebar  │    Content / Detail Area     │
│ (Nav)    │    (Primary workspace)       │
│          │                              │
├──────────┴──────────────────────────────┤
│  Status Bar / Inspector (optional)      │
└─────────────────────────────────────────┘
```

### macOS Window Types
| Type | Use Case |
|------|----------|
| Document window | File-based editing apps |
| Utility window | Floating tools, inspector panels |
| Panel | Non-blocking auxiliary content |
| Full-screen space | Immersive single-task experiences |
| Sheet | Modal action attached to parent window |

