# Apple Human Interface Guidelines — AI Agent Instruction Spec
> Auto-generated specification for AI Agents designing Apple platform apps.
> Based on: https://developer.apple.com/design/human-interface-guidelines/
> Last updated reference: June 2026

## Purpose
This specification translates Apple's Human Interface Guidelines (HIG) into structured, machine-readable instruction sets that AI Agents can use when generating mobile app UI specs, code scaffolding, design tokens, and UX logic.

## Core Design Principles
| Principle | Instruction |
|-----------|-------------|
| **Clarity** | Every UI element must be legible, functional, and unambiguous. Labels must describe the action, not the control (e.g., "Send Payment" not "Submit"). |
| **Deference** | UI chrome must recede; content must lead. Avoid persistent toolbars that compete with content. |
| **Depth** | Use visual layers, motion, and hierarchy to communicate structure and enable navigation. |
| **Hierarchy** | Establish visual hierarchy so users know what is important at a glance. |
| **Harmony** | Align interface elements with Apple hardware/software concentric design. |
| **Consistency** | Adopt platform conventions. Use system components before custom alternatives. |

## File Structure
```
00_INDEX.md                     ← This file (overview + navigation)
01_Designing_for_Platforms.md   ← iOS, Game, Desktop design targets
02_Foundations.md               ← Color, Typography, Layout, Motion, Icons, etc.
03_Patterns.md                  ← Navigation, Search, Onboarding, Feedback, etc.
04_Components.md                ← Buttons, Bars, Controls, Views, Presentation
05_Inputs.md                    ← Touch, Keyboard, Pencil, Game Controller, etc.
06_Technologies.md              ← Widgets, Live Activities, ARKit, Siri, Apple Pay, etc.
```

## AI Agent Usage Instructions
- Reference the relevant `.md` spec file for each design phase.
- Always prefer **system-provided components** (UIKit / SwiftUI) over custom controls.
- All layouts must be validated against **safe area insets** for all iPhone/iPad models.
- **Accessibility** is a first-class requirement — not a post-launch feature.
- Every spec must target a minimum **44×44pt tap target** for interactive elements.
- Apps must support **Dynamic Type** and **Dark Mode** by default.
