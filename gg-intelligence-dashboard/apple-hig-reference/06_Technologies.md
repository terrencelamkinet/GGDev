# Technologies — AI Agent Instruction Spec
> Reference: Apple HIG — Technologies
> Covers: Widgets, Live Activities, App Clips, AR / RealityKit, CarPlay, HealthKit, HomeKit, iCloud, In-App Purchase, Machine Learning, Maps, Messages, NFC, PassKit, Photos, SharePlay, Shortcuts / App Intents, Sign in with Apple, Siri, WatchKit Complications

---

## Technology Integration Principles
1. Each technology must feel **native and seamless** — not bolted on.
2. Always provide a **graceful degradation path** when a technology is unavailable.
3. Follow Apple's **privacy requirements** for each technology's data usage.
4. Use **official system frameworks** — never replicate system functionality with custom code.

---

## 1. Widgets (WidgetKit)

### Widget Sizes
| Size | Points | Use Case |
|------|--------|----------|
| Small | 155×155 | Single metric, quick glance |
| Medium | 329×155 | Two-column info, charts |
| Large | 329×345 | Rich content, lists |
| Extra Large (iPad) | 715×345 | Dashboard views |
| Accessory Circular | 44×44 | Watch face, Lock Screen |
| Accessory Rectangular | 150×44 | Lock Screen banner |
| Accessory Inline | Text only | Lock Screen single line |

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| WGT-001 | Support all widget sizes — provide distinct layouts optimized for each. |
| WGT-002 | Widgets are **non-interactive** — use `Link` for deep link tap actions. |
| WGT-003 | Use `TimelineEntry` + `TimelineProvider` for scheduled content updates. |
| WGT-004 | Widget placeholder: use `redacted(reason: .placeholder)` for loading states. |
| WGT-005 | Refresh rate: respect system-managed timeline refresh — do not over-request. |
| WGT-006 | Widget configuration: use `AppIntentConfiguration` for user-configurable widgets. |
| WGT-007 | Deep link destination from widget tap must be **specific** (not just app root). |
| WGT-008 | Lock Screen widgets (Accessory): use `.widgetAccentable()` for adaptive coloring. |

---

## 2. Live Activities (ActivityKit)

### Live Activity Zones
```
Dynamic Island (iPhone 14 Pro+):
  Compact Leading   → Small icon/value (left of TrueDepth camera)
  Compact Trailing  → Small icon/value (right of TrueDepth camera)
  Minimal           → Single icon (when multiple Live Activities)
  Expanded          → Full-width expanded view (long-press)

Lock Screen Banner:
  Leading View      → Activity icon + primary info
  Trailing View     → Secondary metric
  Bottom Content    → Additional detail row
```

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| LAV-001 | Support both Dynamic Island and Lock Screen banner layouts. |
| LAV-002 | Compact views: maximum 2 pieces of information — icon + single value. |
| LAV-003 | Expanded view: provide meaningful real-time content (ETA, score, status). |
| LAV-004 | End Live Activity when the real-time event concludes — do not leave stale activities. |
| LAV-005 | Push updates via `ActivityKit` background updates or APNs — max update frequency: 1/min. |
| LAV-006 | Use `ActivityAttributes` to define static vs. dynamic content properties. |
| LAV-007 | Relevance score: set higher for urgent activities (delivery arriving, game overtime). |

---

## 3. App Clips

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| APC-001 | Maximum size: **50MB** for App Clip binary. |
| APC-002 | Focus on **one task** — parking payment, food order, check-in, etc. |
| APC-003 | Trigger sources: NFC tag, QR code, Maps, Safari, App Store, Siri Suggestions. |
| APC-004 | Offer full app download as a prominent CTA after task completion. |
| APC-005 | Sign in with Apple or phone number — do not require password account creation. |
| APC-006 | Ephemeral notification permission: available without explicit request in App Clips. |

---

## 4. Augmented Reality (ARKit / RealityKit)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| ARK-001 | Use `RealityView` (SwiftUI) or `ARSCNView` (UIKit) — do not build custom AR rendering. |
| ARK-002 | Always show onboarding for first-time AR users: how to point and move the device. |
| ARK-003 | Provide a non-AR fallback for unsupported devices. |
| ARK-004 | Request camera permission before AR session — provide clear purpose string. |
| ARK-005 | AR coaching overlay: use `ARCoachingOverlayView` for plane detection guidance. |
| ARK-006 | Object placement: use visual anchor indicators (rings, grid) to show valid placement zones. |
| ARK-007 | Lighting: use `AREnvironmentProbe` / `IBL` for realistic object lighting that matches surroundings. |
| ARK-008 | Performance: maintain 60fps — profile with Xcode Instruments (GPU, CPU, memory). |

---

## 5. CarPlay

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| CAR-001 | CarPlay apps: audio, communication, navigation, EV charging, fueling, parking, and quick food ordering. |
| CAR-002 | Design for **glanceability** — driver must understand content in under 2 seconds. |
| CAR-003 | Minimum tap target: **44×44pt** — larger preferred due to in-vehicle use. |
| CAR-004 | No complex interactions — single-tap actions only; no text input while driving. |
| CAR-005 | Screen adapts to vehicle display resolution — use adaptive layout. |
| CAR-006 | Audio apps must support `MPNowPlayingInfoCenter` for system media controls. |
| CAR-007 | Never require phone interaction to use CarPlay features. |

---

## 6. HealthKit

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| HLT-001 | Request only the specific `HKObjectType` data types needed — not broad health access. |
| HLT-002 | Explain clearly in permission prompt **why** each data type is needed. |
| HLT-003 | Health data is private — never sync to non-Apple servers without explicit user consent. |
| HLT-004 | Support Health app integration via `HKHealthStore` write + read permissions. |
| HLT-005 | Use HealthKit units and formatting — do not reformat system health values. |

---

## 7. iCloud (CloudKit / iCloud Drive)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| ICL-001 | Use `CloudKit` for database sync; `NSUbiquitousKeyValueStore` for small key-value sync. |
| ICL-002 | Handle iCloud unavailability gracefully — app must work fully in offline/local mode. |
| ICL-003 | Conflict resolution: use `CKRecord` change tags to detect and resolve sync conflicts. |
| ICL-004 | Never require iCloud sign-in to use core app features. |
| ICL-005 | Show sync status clearly in UI — user should always know if data is saved/syncing/error. |

---

## 8. In-App Purchase (StoreKit 2)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| IAP-001 | Use `StoreKit 2` API — never legacy `SKPaymentQueue`. |
| IAP-002 | All product descriptions must clearly state what is included before purchase. |
| IAP-003 | Subscription terms: display price, duration, and auto-renewal status prominently. |
| IAP-004 | Provide a restore purchases option (required by App Store guidelines). |
| IAP-005 | Use `Product.purchase()` and verify receipts server-side for entitlements. |
| IAP-006 | Never show IAP prompts during onboarding or without user-initiated interaction. |
| IAP-007 | Offer a free trial before subscription charge — use `introductoryOffer` in StoreKit. |

---

## 9. Machine Learning (Core ML / Create ML)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| CML-001 | Run inference on-device using `Core ML` — do not send user data to servers for ML processing without consent. |
| CML-002 | Model size: keep < 50MB for App Store download; use on-demand resources for larger models. |
| CML-003 | Use `Vision` framework for image/face analysis; `NaturalLanguage` for text analysis. |
| CML-004 | Show confidence scores when relevant to user decisions (medical, legal apps). |
| CML-005 | Privacy: declare all ML-based data analysis in Privacy Nutrition Labels. |

---

## 10. Maps (MapKit)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| MAP-001 | Use `MapKit` / `Map` SwiftUI view — not embedded web maps. |
| MAP-002 | Request location permission with `.whenInUse` — only upgrade to `.always` with clear justification. |
| MAP-003 | Custom annotations: use `MapAnnotation` with clear, recognizable pin/marker designs. |
| MAP-004 | Support both standard map and satellite view via user preference. |
| MAP-005 | Look Around: integrate `MKLookAroundScene` for street-level previews where available. |
| MAP-006 | Map clustering: use `MKClusterAnnotation` for dense annotation sets. |

---

## 11. NFC (Core NFC)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| NFC-001 | Use `NFCTagReaderSession` for reading NFC tags. |
| NFC-002 | NFC scanning: user must explicitly initiate — cannot scan in background. |
| NFC-003 | Show scanning UI while `NFCTagReaderSession` is active (system HUD provided). |
| NFC-004 | Handle `NFCError.sessionTimeout` gracefully — offer retry option. |
| NFC-005 | Declare `com.apple.developer.nfc.readersession.formats` entitlement. |

---

## 12. PassKit (Wallet)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| PSK-001 | Use `PKPassLibrary` to add passes — boarding passes, loyalty cards, tickets, coupons. |
| PSK-002 | Pass design: follow PassKit specifications for barcode type, colors, and field layout. |
| PSK-003 | Use `PKAddPassesViewController` — do not build a custom "Add to Wallet" flow. |
| PSK-004 | Push updates to passes server-side using PassKit web service spec (signed push notifications). |

---

## 13. Photos (PhotosKit)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| PHT-001 | Use `PHPickerViewController` (iOS 14+) — no `UIImagePickerController` for new apps. |
| PHT-002 | `PHPickerViewController` requires **no photo library permission** — prefer it for selection. |
| PHT-003 | Request `.readWrite` access only for apps that genuinely manage the photo library. |
| PHT-004 | Limited Photo Library access: handle gracefully when user selects specific photos only. |
| PHT-005 | Use `PhotosUI` `PhotosPicker` SwiftUI view for inline photo selection. |

---

## 14. SharePlay (Group Activities)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| SHP-001 | Use `GroupActivities` framework for synchronized shared experiences. |
| SHP-002 | Handle SharePlay unavailability — fallback to individual use. |
| SHP-003 | Use `GroupSessionMessenger` for real-time sync events between participants. |
| SHP-004 | Support FaceTime + SharePlay integration automatically via `GroupActivity` conformance. |

---

## 15. Shortcuts / App Intents

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| SRI-001 | Implement `AppIntent` for all key user actions — expose to Shortcuts app. |
| SRI-002 | Donate `INInteraction` shortcuts after the user completes an action. |
| SRI-003 | Support Siri suggestions via `INUIAddVoiceShortcutButton`. |
| SRI-004 | App Intents: define `title`, `description`, and parameter validation clearly. |
| SRI-005 | Shortcuts must work headlessly (without opening the app UI) where possible. |
| SRI-006 | Support Spotlight search integration via `CSSearchableItem` for key content. |

---

## 16. Sign in with Apple

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| SWA-001 | **Required** if any other social login (Google, Facebook) is offered. |
| SWA-002 | Use `ASAuthorizationAppleIDButton` — do not create a custom "Sign in with Apple" button. |
| SWA-003 | Handle credential state changes: `ASAuthorizationAppleIDProvider.getCredentialState`. |
| SWA-004 | Support private email relay — never require a non-Apple email. |
| SWA-005 | Store `userIdentifier` securely in Keychain — not `UserDefaults`. |

---

## 17. Siri (SiriKit / App Intents)

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| SIR-001 | Implement `AppIntent` conformance for all primary user tasks. |
| SIR-002 | Siri Shortcuts: show "Add to Siri" button after user completes a repeatable action. |
| SIR-003 | Voice responses: keep spoken responses brief — one to two sentences maximum. |
| SIR-004 | Support on-device Siri processing (no network requirement for intents). |
| SIR-005 | Use `INUIAddVoiceShortcutViewController` to let users record custom phrases. |

---

## 18. Wallet & Apple Pay

### AI Agent Rules
| Rule ID | Instruction |
|---------|-------------|
| APY-001 | Use `PKPaymentAuthorizationViewController` or `PKPaymentAuthorizationController`. |
| APY-002 | Apple Pay button: use `PKPaymentButton` only — do not create a custom Apple Pay button. |
| APY-003 | Show Apple Pay button **above other payment methods** (App Store requirement). |
| APY-004 | Verify payment token server-side before fulfilling any order. |
| APY-005 | Support `ApplePayLaterMerchantRequest` if offering Apple Pay Later integration. |

