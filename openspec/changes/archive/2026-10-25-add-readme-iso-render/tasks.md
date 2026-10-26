## 1. Dependency

- [x] 1.1 Add `matplotlib>=3.8,<4` to `[project].dependencies` in `pyproject.toml`, run `uv lock`, and check that `git diff uv.lock` only touches the root package's dependency list and that `uv sync --locked` succeeds

## 2. Renderer

- [x] 2.1 Create `src/pj3106m_model/render.py`: switch to the Agg backend, add named constants (view elev 35.264 / azim 45, ortho projection, light direction, ambient/diffuse/highlight coefficients, tessellation tolerances, figsize 8×6, dpi 150, background colour, output name `PJ-3106M_iso.png`), and add a helper that tessellates a CadQuery solid into a triangle array. Verify with `uv run python -c "from pj3106m_model import render"`
- [x] 2.2 Add per-triangle shading (Lambert with `abs(n·L)` plus the additive highlight, clipped to [0, 1]) using the part colours from `params.HOUSING_COLOR`, `SHELL_COLOR` and `LEAD_COLOR`. Verify that a quick check of a light-facing and a side-facing housing triangle gives visibly different but still dark colours
- [x] 2.3 Implement `render_iso(out_dir) -> Path`: build the housing, shell and six leads, back-face cull and subdivide the triangles (≤ 0.12 mm edges), project them orthographically and painter-sort them into one 2D `PolyCollection`, use equal scale with axes off, and render at 3× without anti-aliasing, then Lanczos-downsample with Pillow (no metadata). Verify by running it into `build/`: the file is 1200×900 and looks right when opened (black body, gold shell/leads, plug opening and pins 2/4/6 visible, not cropped)
- [x] 2.4 Adjust the zoom/margins and highlight strength until the part fills most of the frame and the housing faces can be told apart. Verify by rendering twice and checking that both runs give byte-identical PNGs (`cmp`)

## 3. Build CLI

- [x] 3.1 Add `--render [DIR]` (`nargs="?"`, default `PROJECT_ROOT / "docs"`) to `build.py` with a lazy `from pj3106m_model.render import render_iso`, and print `wrote <path>`. Verify that `uv run pj3106m-build --render` writes `docs/PJ-3106M_iso.png` and that `uv run pj3106m-build --help` lists the option
- [x] 3.2 Verify that `uv run pj3106m-build` (no flags) still writes only STEP/STL and leaves `docs/` untouched (`git status` shows no PNG change)

## 4. Tests

- [x] 4.1 Create `tests/test_render.py` with a module-scoped fixture that renders into a temp dir, plus image checks: it's a valid PNG at least 800 px wide, the 2-px border is all background, the content bounding box covers at least 50 % of the width or height, the dark-pixel fraction is above a threshold, and gold pixels (R > G > B, R − B > 0.25) are present. Verify that `uv run pytest tests/test_render.py` passes
- [x] 4.2 Add CLI tests: `main(["--out", tmp])` writes no PNG, and `main(["--out", tmp, "--render", tmp2])` writes `tmp2/PJ-3106M_iso.png`. Verify that they pass
- [x] 4.3 Add a README test: `README.md` contains a Markdown image linking `docs/PJ-3106M_iso.png`, and the file exists. Verify that it fails before section 5 and passes after it

## 5. Docs and committed image

- [x] 5.1 Generate the image with `uv run pj3106m-build --render` and add `docs/PJ-3106M_iso.png` to git. Verify that `git ls-files docs/` lists it
- [x] 5.2 Embed `![PJ-3106M 3D model, isometric view](docs/PJ-3106M_iso.png)` in `README.md` right after the intro paragraph, before "Source documents". Verify that it renders in a Markdown preview
- [x] 5.3 Update the README "Build and test" block with `uv run pj3106m-build --render   # regenerate docs/PJ-3106M_iso.png`, extend the "after changing any geometry" note to say to commit the image too, and add `src/pj3106m_model/render.py`, `docs/` and `tests/test_render.py` to "Layout". Verify by reading the README

## 6. Final verification

- [x] 6.1 Run `uv run pytest` (full suite, including `test_committed_outputs_are_current`) and `openspec validate add-readme-iso-render --strict`. Verify that both pass
