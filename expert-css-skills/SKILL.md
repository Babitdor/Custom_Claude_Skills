---
name: expert-css-skills
description: Provides expert‑level CSS guidance, code generation, and optimization for complex layouts, modern features, and cross‑browser compatibility.
---

# Expert CSS Skills

## Description

The **expert-css-skills** skill helps users create, troubleshoot, and refine advanced CSS code. It delivers precise solutions for responsive layouts, custom properties, animations, accessibility, and performance‑focused styling.

## When to Use

- Building a responsive UI with Flexbox, Grid, or Container Queries.
- Implementing custom properties, theming, or advanced animations.
- Solving cross‑browser compatibility issues or optimizing CSS for performance.

## How to Use

### Step 1: Define the Problem
Provide a clear description of the visual goal, target browsers, and any constraints (e.g., file size, theming system).

### Step 2: Request the Solution
Ask the skill for a complete CSS snippet, explanation of the technique, or a step‑by‑step refactor.

### Step 3: Review & Iterate
Validate the output in your environment, then request tweaks, fallbacks, or accessibility improvements as needed.

## Best Practices

- Use **custom properties** for theming and maintainability.
- Prefer **Flexbox** for one‑dimensional layouts and **Grid** for two‑dimensional layouts.
- Include **vendor prefixes** only when necessary; rely on modern browsers’ native support and feature queries.

## Examples

### Example 1: Responsive Card Grid

**User Request:** "Create a responsive card grid that shows 4 columns on desktop, 2 on tablet, and 1 on mobile, with a gap of 1.5rem and a fallback for IE11."

**Approach:**
1. Write a CSS Grid layout with `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));` and a `gap: 1.5rem;`.
2. Add a media query for older browsers that switches to a Flexbox fallback (`display: flex; flex-wrap: wrap;`).
3. Include necessary vendor prefixes (`-ms-grid`) for IE11 and test the layout across browsers.

## Notes

- Always test advanced features (e.g., container queries, `@property`) in the browsers you support.
- The skill does not execute code; verify all generated CSS in a live environment before deployment.