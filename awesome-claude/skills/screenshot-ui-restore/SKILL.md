---
name: screenshot-ui-restore
description: Rebuild UI from a provided screenshot or image path. This skill should be used only when the user provides an image/screenshot and explicitly asks to implement that UI. Focus on UI implementation only, prefer project existing UI library or user-specified UI library, and handle mobile/pc scale restoration.
---

# Screenshot UI Restore

## Overview

Restore UI from screenshots into code with an explicit, repeatable workflow.
Trigger this skill only for screenshot-to-UI implementation tasks; skip non-UI and non-image requests.

## Strict Trigger Gate

Trigger only when all conditions are true:

- User provides a screenshot, image attachment, or image file path.
- User intent is to implement or restore UI from that image.
- Task scope is UI implementation.

Do not trigger when any condition is true:

- User asks only for design critique, style advice, or generic UI ideas.
- User asks for business logic, API, database, auth, or non-UI architecture work.
- User does not provide an image and asks only with text.

If image is missing but intent is screenshot restoration:

- Request image input first.
- Pause implementation until image exists.

## Scope Boundary

Implement only UI:

- Layout, spacing, typography, color, border radius, shadow, icon placement, states.
- Static interaction shell needed for visual parity (for example tabs active state).

Do not expand into:

- API calls, state management architecture, auth flow, database, backend logic.
- Product requirement changes not visible in screenshot.

## Implementation Priority

Apply this priority order for UI stack selection:

1. Use user-specified UI library first.
2. Use project existing UI library if already present.
3. Use project existing style system if no UI library is present.
4. Choose a minimal suitable UI library or native implementation as fallback.

Never introduce a second UI library if project already has a dominant one unless user asks.

## Execution Workflow

### Step 1: Confirm Input and Intent

- Confirm screenshot/image source (attachment or path).
- Confirm target screen type: mobile or pc.
- If unclear from request, infer from image ratio and component density:
  - mobile tendency: narrow viewport, dense vertical stacking.
  - pc tendency: wide viewport, multi-column layout.
- State the inferred target type before coding.

### Step 2: Inspect Project Styling Conventions

- Detect framework and styling baseline from project files.
- Detect preprocessors and unit conversion conventions:
  - `scss/sass/less/stylus`
  - `postcss-px-to-viewport`, `postcss-pxtorem`, `amfe-flexible`, custom vw/rem utils
  - root font-size strategy and mobile adaptation rules
- If project already has a unified `px -> vw/rem` conversion pipeline, keep style input in `px` and let build/runtime config handle conversion.
- Follow existing convention. Do not mix conflicting unit systems.

### Step 3: Resolve Design Width and Scaling

Check these global variables first:

- `AI_MOBILE_UI_DESIGN_DIMENSIONS`
- `AI_PC_UI_DESIGN_DIMENSIONS`

Interpretation rule:

- If variable exists, treat it as design dimension baseline of screenshot UI area.
- Detect whether screenshot appears scaled relative to that baseline.
- If scaled, implement proportional restoration.

Scaling rule:

- `scale = design_ui_width / measured_ui_width_in_screenshot`
- `target_size = measured_size_in_screenshot * scale`

If variables are missing:

- Inform user that global design dimension variables can improve fidelity.
- Continue current task by matching screenshot visual proportion directly.
- Do not block implementation.

### Step 4: Build UI Skeleton First

- Recreate structural layout before detail polish.
- Place major containers, sections, cards, lists, nav bars, action areas.
- Match alignment and spacing rhythm first.

### Step 5: Apply Visual Fidelity Pass

- Calibrate typography scale/weight/line-height.
- Calibrate color, radius, border, shadow, and icon size.
- Match component states visible in screenshot (active/disabled/highlighted).
- Use CSS variables/tokens from project when available.

### Step 6: Implement Responsive Behavior by Target

- For mobile target:
  - Respect project mobile conversion strategy; prefer `px` authoring and rely on project-configured `px -> vw/rem` conversion.
  - Prefer single-column composition and touch-friendly spacing.
- For pc target:
  - Respect desktop container width/grid strategy.
  - Keep column rhythm and whitespace matching screenshot composition.

### Step 7: Self-Check Before Delivery

- Compare code output with screenshot by checklist:
  - structure
  - spacing
  - typography
  - color
  - visual hierarchy
  - component state
- Avoid introducing non-visible features.
- Keep naming and file placement aligned with project conventions.

## Decision Rules

- If screenshot quality is low:
  - Implement closest deterministic approximation.
  - Mark uncertain areas explicitly.
- If part of screenshot is occluded:
  - Infer minimally from surrounding patterns.
  - Avoid speculative product logic.
- If user requests exact library:
  - Follow it even if another library exists, unless conflict is severe.

## Output Contract

Return:

- Implemented UI code in project style.
- Brief note on inferred target type (mobile/pc).
- Brief note on scaling decision:
  - variable found and scaling applied, or
  - variable not found and direct proportion matching used.
