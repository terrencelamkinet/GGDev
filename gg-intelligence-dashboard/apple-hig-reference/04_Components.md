# Components — AI Agent Instruction Spec
> Reference: Apple HIG — Components
> Covers: Content, Layout & Organization, Menus & Actions, Navigation & Search, Presentation, Selection & Input, Status, System Experiences

---

## Component Design Principles
1. **Always prefer system components** over custom implementations.
2. **System components** automatically handle: accessibility, Dark Mode, Dynamic Type, haptics, animations.
3. **Custom components** must manually implement all the above.
4. All components must meet **44×44pt minimum tap target**.

---

## 1. Content Components

### 1.1 Text Views
| Property | Specification |
|----------|--------------|
| Primary text | `.body` style, `.label` color |
| Secondary text | `.subheadline` or `.footnote`, `.secondaryLabel` color |
| Truncation | `.lineLimit(2)` for list items; none for detail views |
| Selection | System text selection supported by default |

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| TXT-001 | Use `Text` (SwiftUI) / `UILabel` — not `UITextView` for non-editable content. |
| TXT-002 | Support text selection and copy for all substantive content. |
| TXT-003 | Use `AttributedString` for mixed formatting (bold, link, color) within a single label. |

### 1.2 Images
```swift
// SwiftUI
Image("photo")
    .resizable()
    .scaledToFit()
    .accessibilityLabel("Description of image")
```

### 1.3 Charts (Swift Charts)
| Rule ID | Instruction |
|---------|-------------|
| CHT-001 | Use `Swift Charts` framework for all data visualization. |
| CHT-002 | Charts must include accessibility descriptions for VoiceOver. |
| CHT-003 | Use semantic colors from system palette — never hardcode chart colors. |
| CHT-004 | Provide a data table as an accessibility alternative to visual charts. |

---

## 2. Layout & Organization

### 2.1 Lists & Tables
```
List Types:
  Plain          → Continuous rows, no section headers
  Grouped        → Rows grouped in sections with headers/footers
  Inset Grouped  → Rounded-corner grouped style (iOS 13+)
  Sidebar        → For iPad/Mac sidebar navigation
```

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| LST-001 | Use `List` (SwiftUI) / `UITableView` for all row-based scrolling content. |
| LST-002 | Row height: minimum 44pt; use `.automatic` row height for variable content. |
| LST-003 | Swipe actions: leading (positive, `.systemGreen`) and trailing (destructive, `.systemRed`). |
| LST-004 | Edit mode: support select-all, delete, and reorder where applicable. |
| LST-005 | Use section headers to group logically related rows. |

### 2.2 Grids
| Rule ID | Instruction |
|---------|-------------|
| GRD-001 | Use `LazyVGrid` / `LazyHGrid` for image galleries and card layouts. |
| GRD-002 | Grid columns: adaptive (fill available width) or fixed (consistent item sizes). |
| GRD-003 | Minimum item size: 44×44pt for touch targets in a grid. |

### 2.3 Scroll Views
| Rule ID | Instruction |
|---------|-------------|
| SCR-001 | Content must extend to bottom safe area — add `.safeAreaInset(edge: .bottom)` padding. |
| SCR-002 | Horizontal scroll: indicate via partial visibility of next item (show 10–15% of next card). |
| SCR-003 | Paging scroll: use `.scrollTargetBehavior(.paging)` for onboarding or media carousels. |

### 2.4 Split Views (iPad / Mac)
| Rule ID | Instruction |
|---------|-------------|
| SPL-001 | Use `NavigationSplitView` for iPad and Mac two/three-column layouts. |
| SPL-002 | Sidebar minimum width: 240pt; content area minimum: 320pt. |
| SPL-003 | On iPhone, split view collapses to single-column automatically. |

---

## 3. Menus & Actions

### 3.1 Buttons
| Button Style | Use Case |
|-------------|----------|
| `.bordered` / `.borderedProminent` | Primary CTAs |
| `.plain` | Inline text actions |
| `.borderless` | Toolbar / navigation actions |
| Destructive | Red color, confirmation required |

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| BTN-001 | One **primary action** per screen — use `.borderedProminent` style. |
| BTN-002 | Destructive buttons: red color, placed last, require confirmation alert. |
| BTN-003 | Disabled state: reduce opacity to 30% — never remove the element. |
| BTN-004 | Loading state: replace button label with `ProgressView` inline — disable interaction. |
| BTN-005 | Icon-only buttons must have `accessibilityLabel`. |
| BTN-006 | Minimum button height: 44pt; minimum width: 44pt. |

### 3.2 Context Menus
| Rule ID | Instruction |
|---------|-------------|
| CTX-001 | Use `.contextMenu {}` for long-press or right-click menus on content items. |
| CTX-002 | Maximum 5 actions in a context menu — group with submenus if more needed. |
| CTX-003 | Destructive actions in context menus: use `.destructive` role (red, placed last). |
| CTX-004 | Include SF Symbol icons for all context menu items. |

### 3.3 Action Sheets / Confirmation Dialogs
| Rule ID | Instruction |
|---------|-------------|
| ACT-001 | Use `.confirmationDialog` for presenting multiple choices. |
| ACT-002 | Always include a Cancel button — placed at the bottom (system handles). |
| ACT-003 | On iPad: action sheets present as popovers anchored to the triggering element. |

---

## 4. Navigation & Search

### 4.1 Tab Bar
```
Max Tabs:     5 items
Item anatomy: Icon (SF Symbol) + Label
Active state: System tint color
Badges:       Numeric (count) or dot (unread indicator)
Position:     Bottom on iPhone; sidebar on iPad (regular width)
```

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| TAB-001 | Tab bar: max 5 items; use "More" tab or sidebar if more sections exist. |
| TAB-002 | Always show text labels under tab bar icons. |
| TAB-003 | On iPad (regular width): convert to sidebar automatically using `NavigationSplitView`. |
| TAB-004 | Tab badges: use for unread counts — clear on tab open. |
| TAB-005 | Never use tab bar as a toolbar — it's for top-level navigation only. |

### 4.2 Navigation Bar
| Rule ID | Instruction |
|---------|-------------|
| NBR-001 | Large title on root screens; inline title on drill-down screens. |
| NBR-002 | Max 2 trailing bar button items; 1 leading (Back auto-generated). |
| NBR-003 | Search bar attaches below navigation bar using `UISearchController`. |
| NBR-004 | Back button label: truncate to parent screen title if long; use "Back" as fallback. |

### 4.3 Toolbar
| Rule ID | Instruction |
|---------|-------------|
| TBR-001 | Toolbars hold context-specific actions for the current screen — not navigation. |
| TBR-002 | Toolbar items: icon + optional label; 3–5 items maximum. |
| TBR-003 | Use `.toolbar` modifier in SwiftUI for placement (`.bottomBar`, `.navigationBarTrailing`). |

### 4.4 Sidebar (iPad / Mac)
| Rule ID | Instruction |
|---------|-------------|
| SDB-001 | Sidebar replaces tab bar on iPad (regular width) and Mac. |
| SDB-002 | Sidebar groups: use `Section` with headers for organizational clarity. |
| SDB-003 | Support drag-and-drop reordering of sidebar items when applicable. |

---

## 5. Presentation

### 5.1 Alerts
```
Alert Anatomy:
  Title (required)    → Short, descriptive — "Delete Message?"
  Message (optional)  → One sentence context
  Actions (1–2)       → [Cancel] [Destructive Action]
```

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| ALT-001 | Maximum 2 actions in an alert (Cancel + primary action). |
| ALT-002 | Default (safe) action: left/first; destructive action: right/last with `.destructive` role. |
| ALT-003 | Alert title: question or statement — never vague ("Warning!" is not acceptable). |
| ALT-004 | Never use alerts for promotional content or tips. |
| ALT-005 | Prefer in-context feedback (inline errors, toasts) over alerts where possible. |

### 5.2 Sheets
| Rule ID | Instruction |
|---------|-------------|
| SHT-001 | Sheet: present with `.sheet {}` modifier for tasks requiring temporary focus. |
| SHT-002 | Resizable sheets: provide `.medium` and `.large` detents for height flexibility. |
| SHT-003 | Sheets include a drag indicator at the top — system-provided, do not replicate. |
| SHT-004 | Navigation inside sheets: use `NavigationStack` — dismiss propagates to sheet root. |

### 5.3 Popovers
| Rule ID | Instruction |
|---------|-------------|
| POP-001 | Popovers on iPad: anchor to the control that triggered them. |
| POP-002 | On iPhone: popovers become full sheets automatically. |
| POP-003 | Popovers dismiss on tap outside — never require an explicit close button for simple menus. |

---

## 6. Selection & Input

### 6.1 Text Fields
| Rule ID | Instruction |
|---------|-------------|
| TFD-001 | Use `TextField` with appropriate `textContentType` for AutoFill support. |
| TFD-002 | Always show placeholder text describing the expected input. |
| TFD-003 | Show character limits inline (e.g., "140/280") when applicable. |
| TFD-004 | Use `SecureField` for passwords — with show/hide toggle. |

### 6.2 Pickers
| Type | Use Case |
|------|----------|
| `Picker` (wheel) | Date/time, short value lists |
| `Picker` (segmented) | 2–5 mutually exclusive options |
| `DatePicker` | Date/time selection |
| `ColorPicker` | Color selection |
| `PhotosPicker` | Image/video selection from library |

### 6.3 Toggles & Switches
| Rule ID | Instruction |
|---------|-------------|
| TGL-001 | Use `Toggle` for binary on/off settings. |
| TGL-002 | Label must clearly describe what is toggled — "Enable Notifications" not "Notifications". |
| TGL-003 | Toggle responds immediately — no Save button required. |

### 6.4 Sliders & Steppers
| Rule ID | Instruction |
|---------|-------------|
| SLD-001 | Use `Slider` for continuous value selection (volume, brightness, price range). |
| SLD-002 | Use `Stepper` for precise integer increments (quantity, age, count). |
| SLD-003 | Show current value label adjacent to slider. |

---

## 7. Status

### 7.1 Progress Indicators
| Type | Use Case |
|------|----------|
| `ProgressView()` (spinner) | Indeterminate loading |
| `ProgressView(value:total:)` (bar) | Determinate progress (upload, download) |
| Skeleton views | Content placeholder while loading |

### 7.2 Badges
| Rule ID | Instruction |
|---------|-------------|
| BDG-001 | App icon badge: numeric count for notifications/unread items. |
| BDG-002 | Tab bar badge: use for unread counts; clear when user views the section. |
| BDG-003 | Badge text: max 3 digits — show "99+" for counts over 99. |

---

## 8. System Experiences

### 8.1 Widgets
| Rule ID | Instruction |
|---------|-------------|
| WGT-001 | Support all three widget sizes: small, medium, large. |
| WGT-002 | Widgets are non-interactive snapshots (except for specific interactive widget components). |
| WGT-003 | Widget content must load quickly — use `TimelineProvider` for scheduled updates. |
| WGT-004 | Deep link from widget tap to specific app content using URL schemes. |

### 8.2 App Clips
| Rule ID | Instruction |
|---------|-------------|
| APC-001 | App Clip binary: maximum 50MB. |
| APC-002 | App Clip must focus on one specific task — not the full app. |
| APC-003 | Offer full app download upon task completion. |

