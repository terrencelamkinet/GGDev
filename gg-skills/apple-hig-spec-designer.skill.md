---
name: apple-hig-spec-designer
version: 1
summary: Generate Apple-platform mobile app specifications and screen specs using Apple Human Interface Guidelines as an agent-executable design system.
license: Reference-based internal skill
sources:
  - https://developer.apple.com/design/human-interface-guidelines
  - https://developer.apple.com/design/human-interface-guidelines/designing-for-ios
  - https://developer.apple.com/design/human-interface-guidelines/components
  - https://developer.apple.com/design/
---

# Apple HIG Spec Designer

Use this skill when designing a mobile app, game UI, or desktop app specification for Apple platforms. This skill translates Apple Human Interface Guidelines into agent-executable instructions for generating structured `.md` specs, screen definitions, component contracts, and review rubrics.

## Goal

Produce app specifications that feel native to Apple platforms, prefer system conventions over custom invention, and are complete enough for product, design, and engineering handoff. Apple’s HIG emphasizes hierarchy, harmony, and consistency across platform experiences.[cite:1]

## Design principles

Always optimize for these principles first:
- Hierarchy: create a clear visual and interaction hierarchy.[cite:1]
- Harmony: align UI choices with hardware, software, and system experiences.[cite:1]
- Consistency: adopt platform conventions and standard system components whenever possible.[cite:1][cite:3]
- Native-first: prefer Apple patterns before custom interaction models.[cite:2][cite:3]
- Task clarity: every screen must make the primary action obvious.

## When to use

Use this skill when the user asks for any of the following:
- Design a new iOS, iPadOS, macOS, watchOS, tvOS, or visionOS app spec
- Convert product ideas into screen specifications
- Produce Apple-style UX documentation in Markdown
- Audit an existing app concept for Apple HIG compliance
- Generate pattern selection, component selection, and interaction rules

Do not use this skill for Android-first or web-first products unless the user explicitly wants Apple-platform adaptation.

## Required output artifacts

The default output should be one or more Markdown files. A complete delivery should usually contain:
- `00_Product_Overview.md`
- `01_Information_Architecture.md`
- `02_User_Flows.md`
- `03_Screen_Specs.md`
- `04_Component_Contracts.md`
- `05_Design_Tokens_and_Foundations.md`
- `06_Pattern_Decisions.md`
- `07_Accessibility_and_Review.md`

For smaller requests, compress the structure, but do not omit:
- Product context
- Screen specs
- States and edge cases
- Accessibility
- Design review checklist

## Agent workflow

Follow this sequence strictly.

### 1. Interpret product context

Extract or infer:
- Product type
- Primary platform: iPhone, iPad, Mac, game, or multi-platform
- Target users
- Core tasks
- Usage frequency
- Data density
- Trust, privacy, and permission sensitivity
- Online/offline expectations

If the request is under-specified, define explicit assumptions and label them as assumptions.

### 2. Choose platform conventions

Select patterns according to Apple platform norms:
- iPhone: navigation stack, tab bar, sheets, large-title roots when appropriate.[cite:2]
- Mac: sidebar, toolbar, multi-column or windowed workflows.
- Games: immersive full-screen presentation, controller-aware UI, gameplay-safe overlays.[cite:10][cite:41][cite:44]
- Component usage should prefer system-defined elements because Apple explicitly recommends familiar and consistent system components.[cite:3]

### 3. Build information architecture

Define:
- Top-level destinations
- Primary and secondary navigation
- Deep-link destinations
- Search entry points
- Modal vs push navigation boundaries
- Maximum reasonable hierarchy depth

### 4. Generate user flows

For each core task, define:
- Entry point
- Preconditions
- Happy path
- Alternate path
- Error path
- Empty state
- Loading state
- Success confirmation
- Permission denial path
- Offline or interrupted path

### 5. Generate screen specs

Every screen spec must include this schema:

```md
## Screen: <name>
- Purpose:
- Primary user goal:
- Primary action:
- Secondary actions:
- Entry points:
- Exit points:
- Navigation model:
- Content hierarchy:
- Key components:
- Default state:
- Loading state:
- Empty state:
- Error state:
- Success state:
- Permissions involved:
- Accessibility notes:
- Analytics events:
- Edge cases:
```

No screen is complete without state coverage.

### 6. Assign component contracts

For each major component, define:
- Name
- Purpose
- Props or configurable content
- Variants
- States
- Interaction behavior
- Accessibility requirements
- Platform-specific notes
- Reuse rules

### 7. Run HIG review

Evaluate the draft on:
- Hierarchy
- Harmony
- Consistency
- Safe-area awareness
- Touch target adequacy
- Dynamic Type support
- Dark Mode readiness
- System component preference
- Motion restraint
- Permission timing
- Clarity of primary actions

## Decision rules

Use these decision rules when generating new specs.

### Navigation

```text
IF the app has 3–5 top-level peer destinations on iPhone
THEN prefer a Tab Bar.

IF the app has more than 5 top-level destinations
THEN refactor IA or prefer sidebar-based navigation on larger devices.

IF the workflow is drill-down and sequential
THEN prefer a Navigation Stack.

IF a task is temporary and self-contained
THEN prefer a Sheet rather than full navigation takeover.
```

### Search

```text
IF users seek known items from medium or large datasets
THEN provide search as a first-class entry point.

IF search is frequent and task-critical
THEN expose it high in the hierarchy, not buried in settings or overflow menus.
```

### Forms

```text
IF the form is short and low-risk
THEN keep it on one screen with inline validation.

IF the form is long, sensitive, or cognitively heavy
THEN split into progressive steps with clear progress feedback.
```

### Modality

```text
IF the user must resolve a focused task before continuing
THEN use a modal presentation.

IF the task can be postponed without harm
THEN keep the user in normal navigation flow.
```

### Components

```text
IF a standard Apple component exists
THEN use it before inventing a custom equivalent.

IF a custom component is necessary
THEN document why the system component is insufficient and define accessibility behavior explicitly.
```

## Writing rules for generated Markdown

Every generated Markdown spec should:
- Use clear section headings
- Separate product-level decisions from screen-level details
- Be implementation-friendly for design and engineering teams
- Distinguish assumptions from confirmed requirements
- Use concise bullets over long narrative paragraphs
- Avoid decorative language
- Use tables for comparisons and mappings

## Accessibility minimums

Always require:
- Minimum 44×44pt touch targets where relevant to touch interfaces
- Dynamic Type support for text scaling
- Sufficient contrast and non-color-only state signaling
- VoiceOver-friendly labels for controls
- Reduced Motion fallback where motion is used
- Logical focus and reading order

These are consistent with Apple’s design guidance and platform expectations.[cite:2][cite:3]

## Review rubric

Every final spec must end with a rubric table like this:

| Dimension | Score 1-5 | Notes |
|---|---:|---|
| Platform fidelity |  |  |
| Navigation clarity |  |  |
| Primary action clarity |  |  |
| State completeness |  |  |
| Accessibility completeness |  |  |
| Component consistency |  |  |
| HIG compliance confidence |  |  |

Then provide:
- Top 3 design risks
- Top 3 unresolved assumptions
- Recommended next design iteration

## Output modes

### Mode A: New app spec

Create a full app spec package.

### Mode B: Single feature spec

Create:
- feature overview
- user flow
- affected screens
- component deltas
- review checklist

### Mode C: HIG audit

Audit an existing concept or screen set against this rubric:
- compliant
- partially compliant
- non-compliant
- recommendation

## Style calibration

- Favor native-feeling, calm, obvious interactions over novelty.
- Prefer removal over addition when a UI feels crowded.
- If unsure, use standard Apple conventions.
- Explain deviations from standard patterns explicitly.

## Example prompt patterns

- Design an iPhone budgeting app spec using apple-hig-spec-designer.
- Convert this product brief into Apple-platform screen specs.
- Audit these app screens for HIG compliance and rewrite the spec.
- Generate a Markdown feature spec for an iPad inventory workflow.

