# KONGGER UX + Animation Specification

## Design Philosophy
Inspired by Instagram and early Facebook: fast, warm, personal.
Dunbar rule: max 30 neighbours. Private by default.

## Response Time Targets

| Action                    | Target   | Method                          |
|---------------------------|----------|---------------------------------|
| Button press feedback     | 0ms      | CSS :active { transform:scale(.96) } |
| Like button              | 0ms UI   | Optimistic update (no wait)     |
| Page navigation          | <150ms   | Hash router + CSS translateX    |
| Feed first load          | <300ms   | Skeleton → API → real cards     |
| Feed next page           | <200ms   | Prefetch at 70% scroll depth    |
| Profile load             | <250ms   | Cache TTL 60s in memory         |
| Input validation         | 500ms    | Debounce, never on keydown      |
| Toast notification       | 280ms    | Slide-in + auto-dismiss 3s      |
| Modal open/close         | 200ms    | CSS backdrop-filter + transform |

## Animation Timing Functions
--transition-fast:    80ms cubic-bezier(0.16,1,0.3,1)   /* micro-interactions */
--transition-base:    180ms cubic-bezier(0.16,1,0.3,1)  /* buttons, hover states */
--transition-slow:    320ms cubic-bezier(0.16,1,0.3,1)  /* page transitions */
--spring-pop:         400ms cubic-bezier(0.34,1.56,0.64,1) /* like heart, badge */

## Heart / Like Button Flow
1. User taps → 0ms: optimistic update (♡→♥, count +1, color change)
2. 0-400ms: heart does scale(0 → 1.4 → 1.0) spring animation
3. If API error: revert count + show error toast
4. Never block UI for API round-trip

## Scroll-Reveal Cards
IntersectionObserver threshold=0.1
Cards enter: opacity 0→1, translateY 12px→0 over 320ms
Stagger: each card 80ms apart (CSS nth-child delay)

## Page Transitions (Hash Router)
Leave: opacity 1→0, translateX 0→-20px (160ms)
Enter: opacity 0→1, translateX 20px→0 (220ms)

## Mobile Specifics (375px)
- Bottom navigation bar (56px height, 5 items)
- Modal sheets slide up from bottom, 85dvh max
- Post card images 240px height (consistent thumb zone)
- All tap targets minimum 44×44px
- Haptic-like :active state on every button

## Visitor Count Animation
- Number counts up from 0 to actual value in 800ms
- Uses requestAnimationFrame for smooth count
- Easing: ease-out (decelerate toward final number)

## Skeleton Loading
Shimmer animation: 1.5s ease-in-out infinite
Light mode: #edeae5 → #e6e4df → #edeae5
Dark mode: #262523 → #2d2c2a → #262523
Always mirrors real component layout exactly

## Mood Selection
Emoji grid: 5×2 layout of 10 mood options
Selected mood: scale(1.15), border: var(--color-primary), spring animation
Unselected: scale(1.0), border: transparent

## Colour Palette (Xanga-Inspired, Copyright-Safe)
Surface:    warm off-white #f7f6f2 / dark #171614
Accent:     deep burgundy-rose primary
Secondary:  teal #01696f for CTAs
Gold:       #d19900 for premium elements
Text:       #28251d / #cdccca (dark mode)
