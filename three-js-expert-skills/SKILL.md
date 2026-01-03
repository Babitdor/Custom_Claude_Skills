---
name: three-js-expert-skills
description: Provides expert guidance, code snippets, and optimization advice for building, debugging, and scaling Three.js applications.
---

# Three.js Expert Skills

## Description

The **three-js-expert-skills** skill equips developers with concise, production‑ready Three.js solutions. It can generate scene setups, advanced material pipelines, performance‑optimised patterns, and step‑by‑step troubleshooting advice, drawing from the latest tutorials and best‑practice resources.

## When to Use

- Building a new interactive 3D web experience from scratch.
- Debugging lighting, shadows, or performance issues in an existing Three.js project.
- Migrating a Three.js scene to React Three Fiber or adding real‑time post‑processing effects.

## How to Use

### Step 1: Define the Goal
Provide a clear, short description of the desired outcome (e.g., “create a rotating Earth with realistic atmosphere and orbit controls”).

### Step 2: Request Targeted Code or Advice
Ask the skill for the specific artifact you need: a full HTML/JS boilerplate, a shader snippet, an optimization checklist, or a migration guide.

### Step 3: Integrate & Iterate
Copy the generated code into your project, run it, and ask follow‑up questions for tweaks, debugging, or performance tuning.

## Best Practices

- **Modularise**: Keep geometry, materials, and controls in separate modules or files.
- **Profile Early**: Use `renderer.info` and tools like `r3f-perf` to monitor draw calls and texture memory from day one.
- **Leverage PBR**: Prefer `MeshStandardMaterial` or `MeshPhysicalMaterial` with proper HDR environment maps for realistic lighting.

## Examples

### Example 1: Interactive Rotating Cube

**User Request:** “I need a minimal Three.js example that shows a rotating cube with orbit controls and responsive resizing.”

**Approach:**
1. Generate a Vite‑compatible HTML/JS boilerplate that imports Three.js via CDN.
2. Add a `PerspectiveCamera`, `WebGLRenderer`, `OrbitControls`, and a simple `BoxGeometry` mesh.
3. Include a resize listener that updates the camera aspect and renderer size on window resize.

### Example 2: Optimising a Heavy GLTF Scene

**User Request:** “My GLTF model runs at 15 fps on a mid‑range laptop. How can I improve performance?”

**Approach:**
1. Suggest mesh merging and geometry simplification (use `BufferGeometryUtils.mergeVertices`).
2. Recommend texture compression (basis/ASTC) and lowering max texture size.
3. Advise enabling `renderer.shadowMap.enabled = false` if shadows aren’t critical, and using `InstancedMesh` for repeated objects.

## Notes

- The skill returns **runnable code snippets** but does not host assets; you must provide URLs for models, textures, or HDR maps.
- Advanced GPU‑specific features (e.g., WebGPU) are outside the current scope; stick to WebGL‑based Three.js APIs.