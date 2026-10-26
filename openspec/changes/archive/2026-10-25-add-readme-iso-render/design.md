## Context

- Geometry lives in `src/pj3106m_model/model.py`: `build_housing()`, `build_shell()` and
  `build_leads()` return separate CadQuery solids. `build_assembly()` colours them from
  `params.HOUSING_COLOR`, `SHELL_COLOR` and `LEAD_COLOR` for the STEP.
- `src/pj3106m_model/build.py` is the `pj3106m-build` CLI. Its `--preview` option writes
  monochrome SVG projections of the fused solid to the gitignored `build/` directory. The
  `iso` direction is (1, 1, 1).
- `matplotlib` (with numpy and Pillow) is already in `uv.lock` through cadquery → vtk,
  but `pyproject.toml` doesn't declare it.
- `tests/test_pj3106m.py::test_committed_outputs_are_current` keeps STEP/STL in sync with
  the source. There's no equivalent for images.
- Frame: +Y is the plug opening, +Z is up, and pins 2/4/6 are on +X (see README
  "Coordinate frame").

## Goals / Non-Goals

**Goals:**
- One function that turns the three part solids into a coloured, shaded, equal-aspect
  isometric PNG, using only matplotlib's Agg backend (headless, no display, no GPU).
- A render you can reproduce on the same locked environment. PNG metadata that changes
  between runs (timestamps, software string) is stripped so the committed file only changes
  when the geometry or the colours change.

**Non-Goals:**
- Replacing or changing the existing SVG `--preview` output.
- A pixel-exact regression test against the committed PNG.
- Using VTK/OCP viewers or any offscreen OpenGL context.

## Decisions

### 1. Tessellate, cull, subdivide, then painter-sort in 2D
Each part solid is tessellated with `Shape.tessellate(0.02 mm, 0.2 rad)`. Triangles facing
away from the camera are dropped. CadQuery returns outward winding, so `n·view > 0` keeps
only the visible side. The rest are split at the midpoint of their longest edge until every
edge is ≤ 0.12 mm. Each triangle gets a face colour: the part's base RGB from `params`,
shaded (see 2). All triangles are projected orthographically onto the camera plane with
numpy, sorted far-to-near by centroid depth, and drawn as **one 2D `PolyCollection`**.

- *Why not mplot3d `Poly3DCollection` (the original plan):* a first try showed the
  painter's sort going wrong with CAD tessellation's long sliver triangles: the bore and
  nose showed through the housing. Doing the projection and sort in our own code makes the
  draw order explicit and easy to test.
- *Why subdivide:* the painter's algorithm only works when triangles are small compared
  with the gaps between surfaces. At 0.3 mm there were still speckles where the gold shell
  sits flush in its pocket. At 0.12 mm (about 200k triangles) edges are clean, and the
  render takes about 5 s.
- *Alternatives:* `plot_trisurf` per part (the same sorting problem); load the STL with
  trimesh (that loses the per-part colours); use a VTK offscreen render (needs OpenGL, and
  the user asked for matplotlib).

### 2. Lambert shading plus a small specular-like lift
Shaded colour = `base * (ambient + diffuse * |n·L|) + highlight * |n·L|^k`, clipped to
[0, 1]. L points from slightly above and to the left of the camera.

- *Why the additive term:* the housing is RGB ≈ 0.06. Purely multiplicative shading keeps
  every housing face at ≈ 0.02–0.06, so the body reads as a flat silhouette. A small
  additive grey highlight (0.22) on light-facing faces separates the top, front and side
  faces while the body still looks black. Gold faces stay clearly gold.

### 3. Camera, anti-aliasing and output
- View direction: elev 35.264°, azim 45° (true isometric from +X, +Y, +Z), the same as
  the existing `iso` SVG preview direction. It shows the plug opening, the shell top and
  the pins 2/4/6 side.
- Equal scale (`set_aspect("equal")`), model centred and spanning 85 % of the tighter
  image side, axes off, white background.
- **Supersampling:** the collection is drawn at 3× resolution with anti-aliasing off
  (anti-aliased triangle edges leak whatever was drawn behind them, so seams and hidden
  surfaces show through). Pillow then downsamples the buffer to 1200 × 900 with Lanczos
  for smooth silhouettes, and writes the PNG. Pillow is already a matplotlib dependency.
  Pillow writes no timestamp or software metadata, so repeated renders are byte-identical.

### 4. Module and CLI layout
- New module `src/pj3106m_model/render.py` with
  `render_iso(out_dir: Path) -> Path`. It builds the parts by calling
  `build_housing/shell/leads` and reads the colours from `params`, so the geometry and the
  colours have one source. It writes `out_dir / "PJ-3106M_iso.png"`.
- Rendering constants (view angles, light, figure size, DPI, tolerances, shading
  coefficients) are module-level named constants in `render.py`, not in `params.py`.
  `params.py` stays datasheet dimensions and part colours only.
- `build.py` gains `--render [DIR]` (`nargs="?"`, default constant
  `PROJECT_ROOT / "docs"`). It imports `render` lazily, so a plain build doesn't import
  matplotlib. `--render` works alongside `--out` and `--preview`.
  - *Alternative:* a separate `pj3106m-render` script entry. Rejected because the spec asks
    for one build command, and a flag keeps it discoverable next to `--preview`.
- `matplotlib>=3.8,<4` is added to `[project].dependencies`, and `uv lock` is re-run. The
  resolved versions shouldn't change, since matplotlib is already locked.

### 5. Tests (`tests/test_render.py`)
- Render once (module-scoped fixture) into `tmp_path_factory`. Load it with
  `matplotlib.image.imread`.
- Check: it's a valid PNG, at least 800 px wide; the outer 2-pixel border is all background
  (so nothing is cropped); the non-background pixel bounding box covers at least 50 % of the
  width or height; dark pixels (max channel < 0.35, low saturation) make up a meaningful
  fraction; gold pixels (R > G > B, R − B > 0.25) are present above a threshold.
- `main(["--out", tmp])` without `--render` writes no PNG into `tmp` (default build is
  unchanged), and `main(["--out", tmp, "--render", tmp2])` writes the PNG to `tmp2`.
- README check: the README contains a Markdown image reference to `docs/PJ-3106M_iso.png`,
  and that file exists in the repo.

## Risks / Trade-offs

- [The painter's algorithm isn't a z-buffer: surfaces closer together than about one
  triangle size can still sort wrongly] → Use 0.12 mm subdivision plus back-face culling,
  and check the committed image visually when the geometry changes.
- [Agg output can differ slightly between matplotlib/freetype versions] → The repo doesn't
  test PNG bytes. The README says to regenerate the image with the build and commit it
  along with `models/`.
- [Rendering adds time to `pytest`] → One module-scoped render plus one CLI render, about 10 s in total.
- [Binary file in git (about 100–300 KB)] → Acceptable for one image. It only changes when
  the geometry or colours change, because the metadata is stripped.

## Migration Plan

Purely additive. Generate `docs/PJ-3106M_iso.png` once with
`uv run pj3106m-build --render` and commit it with the code and README changes. To roll
back, revert the commit. The STEP/STL outputs are unaffected.
