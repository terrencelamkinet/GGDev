***REMOVED*** KONGGER — UX, Animation & Interaction Specification
***REMOVED*** Professional-grade, referencing Instagram / Facebook interaction patterns

***REMOVED******REMOVED*** RESPONSE TIME TARGETS (Morgan's Law & Nielsen's Guidelines)
  Button tap → visual feedback:      0ms    (immediate, synchronous)
  Optimistic UI state update:        0ms    (no wait, assume success)
  API round-trip (cached):          <80ms
  API round-trip (first load):     <300ms
  Page transition (SPA):           <150ms
  Image skeleton → reveal:         <500ms  (skeleton shown instantly)
  Feed scroll next batch:          <200ms  (prefetched 3 screens ahead)
  Error state appearance:          <100ms  (after confirmed API failure)

***REMOVED******REMOVED*** BUTTON INTERACTION DESIGN

***REMOVED******REMOVED******REMOVED*** Primary Button (Post, Save, Send)
  Resting:     background ***REMOVED***4a90d9, scale 1.0, shadow-md
  Hover:       background ***REMOVED***357ab8, scale 1.02, shadow-lg, transition 150ms ease-out
  Active/tap:  scale 0.96, shadow-sm, background ***REMOVED***2d6a9f, duration 80ms
  Loading:     spinner replaces label, pointer-events none, opacity 0.8
  Success:     checkmark icon → fade back to label, 1200ms
  Error:       shake animation 300ms, border-color error-red, label restored

  CSS reference:
    transition: transform 80ms cubic-bezier(0.16,1,0.3,1),
                background 150ms ease, box-shadow 150ms ease;
    &:active { transform: scale(0.96); }

***REMOVED******REMOVED******REMOVED*** Like Button (heart)
  Tap:         heart scale 0→1.4→1.0 in 400ms (spring physics)
               colour transitions grey → red during scale-up
               haptic feedback (navigator.vibrate([10]) on mobile)
  Already liked: reverse animation, red → grey, scale 1.2→1.0

***REMOVED******REMOVED******REMOVED*** Neighbour / Follow Button
  Pending:     "Pending..." text, pulsing opacity 0.6↔1.0, 1.5s loop
  Accepted:    tick icon + "Neighbours", green flash 600ms then neutral

***REMOVED******REMOVED*** PAGE TRANSITIONS

***REMOVED******REMOVED******REMOVED*** Hash Router Transitions (CSS only, no JS library needed)
  Enter:       translateX(+24px) + opacity(0) → translateX(0) + opacity(1)
               duration: 200ms, easing: cubic-bezier(0.16,1,0.3,1)
  Exit:        translateX(0) + opacity(1) → translateX(-24px) + opacity(0)
               duration: 150ms, easing: ease-in

  Implementation:
    .page { animation: pageEnter 200ms cubic-bezier(0.16,1,0.3,1) forwards; }
    @keyframes pageEnter { from { transform:translateX(24px); opacity:0; } }

***REMOVED******REMOVED******REMOVED*** Modal / Sheet (Profile editor, gift sender)
  Mobile:      slide up from bottom, translateY(100%)→0, 280ms spring
  Desktop:     fade + scale 0.96→1.0, 200ms
  Dismiss:     reverse, 180ms ease-in, backdrop fades out
  Overlay:     backdrop-filter blur(4px), rgba black 0→0.5

***REMOVED******REMOVED*** FEED & SCROLL PERFORMANCE (Instagram model)

***REMOVED******REMOVED******REMOVED*** Virtual Scroll
  Render only visible posts + 3 screens above/below (windowing)
  Prefetch next page when user reaches 70% scroll position
  Image lazy-load with IntersectionObserver threshold 0.1
  Skeleton cards shown for unprefetched items

***REMOVED******REMOVED******REMOVED*** Post Card Animation
  Initial load:  stagger-in, each card delays +40ms (max 5 cards staggered)
                 translateY(16px) + opacity(0) → base, 300ms
  New post:      slides in from top, pushes feed down, 250ms spring
  Delete:        collapses height to 0 + opacity fade, 300ms, then removed from DOM

***REMOVED******REMOVED******REMOVED*** Image in Post
  Loading:       blurred placeholder (LQIP pattern), shimmer overlay
  Loaded:        blur(8px)→blur(0) over 400ms, opacity 0.6→1.0
  Error:         grey box with camera icon, "Image unavailable" label

***REMOVED******REMOVED*** PROFILE PAGE (Xanga room model)

***REMOVED******REMOVED******REMOVED*** Visitor Counter
  Number:        animate count-up on first view, 800ms, easing ease-out
  New visitor:   +1 count pop animation, scale 1.3→1.0 with colour flash

***REMOVED******REMOVED******REMOVED*** Cover Photo
  Parallax scroll: moves at 0.3× scroll speed on desktop
  Mobile:         fixed position, no parallax (performance)

***REMOVED******REMOVED******REMOVED*** Music Widget
  Idle:          album art rotates at 4rpm (CSS animation, paused when not playing)
  Playing:       rotation resumes, equaliser bars animate beside title
  Note bubbles:  ♪ ♩ floats upward every 8s, opacity fade out at top

***REMOVED******REMOVED******REMOVED*** Ad Board
  Hover:         gentle pulse glow on border, 2s loop
  Click:         ripple effect from click origin, link opens in new tab

***REMOVED******REMOVED*** FORM INTERACTIONS

***REMOVED******REMOVED******REMOVED*** Text Input
  Focus:         border transitions from --color-border to --color-primary, 150ms
                 label floats up (floating label pattern), 200ms
  Typing:        character count shows if near limit
  Validation:    red border + error message appear after 500ms of stopped typing (debounce)
  Success:       green tick icon fades in on valid field

***REMOVED******REMOVED******REMOVED*** Mood Selector (post mood)
  Display:       emoji grid, 2 rows × 5 columns
  Selection:     selected emoji scales 1.0→1.3→1.1, ring highlight
  Deselect:      previous selection shrinks back to 1.0

***REMOVED******REMOVED******REMOVED*** Post Composer
  Expand:        textarea height animates from 1 line → 4 lines on focus, 200ms
  Character bar: progress bar fills as user types, turns amber at 80%, red at 95%
  Attach media:  drag-and-drop zone pulses border on dragover

***REMOVED******REMOVED*** NOTIFICATION SYSTEM

***REMOVED******REMOVED******REMOVED*** Notification Bell
  Unread badge:  appears with scale 0→1.2→1.0 spring, 300ms
  Number update: flip animation (card flip on Y axis), 200ms
  Read:          badge fades out, 200ms

***REMOVED******REMOVED******REMOVED*** Notification Item
  New:           left border accent, background slightly highlighted
  Hover:         background shifts to --color-surface-2, 120ms
  Mark read:     accent fades out, 300ms transition

***REMOVED******REMOVED*** TOAST MESSAGES

  Success:       slide in from top-right, green accent, icon + message, 3s auto-dismiss
  Error:         slide in from top-right, red accent, persists until dismissed
  Info:          neutral, 2s auto-dismiss
  Animation in:  translateX(+100%) → 0, 250ms cubic-bezier(0.16,1,0.3,1)
  Animation out: translateX(+100%), opacity→0, 200ms ease-in

***REMOVED******REMOVED*** DARK MODE TRANSITION
  Toggle:        all colour CSS variables transition over 250ms
                 moon/sun icon rotates 180° + fade crossfade, 300ms
                 no flash of wrong theme (theme set before first paint via script in <head>)

***REMOVED******REMOVED*** MOBILE-SPECIFIC INTERACTIONS

***REMOVED******REMOVED******REMOVED*** Pull-to-Refresh
  Pull threshold: 60px
  Indicator:     spinner appears at top, rotates
  Release:       API refetch, feed reloads with stagger animation

***REMOVED******REMOVED******REMOVED*** Bottom Navigation
  Active tab:    icon scales 1.0→1.15, label slides up, accent colour
  Tap feedback:  background pill expands from icon, 150ms
  Badge:         red dot, pulses once on first appear

***REMOVED******REMOVED******REMOVED*** Swipe Gestures
  Post card:     swipe left reveals quick-like, swipe right reveals share
  Modal:         swipe down to dismiss (velocity > 0.3px/ms triggers close)

***REMOVED******REMOVED*** PERFORMANCE BUDGET
  First Contentful Paint:  < 1.2s on 4G
  Largest Contentful Paint: < 2.0s on 4G
  Cumulative Layout Shift:  < 0.05 (images always have explicit dimensions)
  Time to Interactive:     < 3.0s on 4G
  JS bundle initial:       < 150KB gzipped
  CSS:                     < 30KB gzipped
  Each post image:         WebP, max 800px wide, max 150KB
