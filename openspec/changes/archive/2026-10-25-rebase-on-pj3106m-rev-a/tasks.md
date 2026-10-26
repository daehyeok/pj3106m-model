## 1. Source identity

- [x] 1.1 In `src/pj3106m_model/params.py`, set the `DATASHEET_*` and `LCSC_PART` (C7428681) constants to PJ-3106M (YBC01), rev A, created 2019-09-10, SHA-256 `88db1b26c288bbaa0537e7a184d20efc260de7c7e152d95f0d4d86067e96ea4f`, vector drawing. Rewrite the module docstring to match. Verify: `uv run pj3106m-datasheet --datasheet <copy of PJ-3106M.pdf>` exits 0, and running it on any other file exits 1.
- [x] 1.2 Update `tests/test_datasheet.py` (`test_recorded_identity_is_rev_a2` becomes a rev A identity check) and any rev A2 wording in `src/pj3106m_model/datasheet.py`. Verify: `uv run pytest tests/test_datasheet.py` passes.

## 2. Parameters

- [x] 2.1 In `params.py`, apply every value in the design.md D1 table. Each comment says `datasheet (<view>)` or `estimate (<view/photo>)`. Add `NOSE_DIP`, `NOSE_BELOW_BOARD_WIDTH`, the trapezoid notch widths, `PAD_ACROSS = 2.60`, `PAD_OUTER_SPAN = 8.80`, `PCB_HOLE_DIAMETER = 1.60` and `NOSE_CUTOUT_WIDTH = 3.20`. Set the new `PIN_FROM_FRONT`/`PIN_SIDE` (+X: 2/4/5, −X: 1/3/6). Verify: `PAD_CENTROID_FROM_FRONT` evaluates to 7.125 and `AXIS_X` to 0.0 in a `uv run python -c` check.

## 3. Geometry

- [x] 3.1 In `build_housing`, after the nose fillet, cut the nose above Z = `HOUSING_HEIGHT` and below Z = −`NOSE_DIP`, and trim the part below Z = 0 to `NOSE_BELOW_BOARD_WIDTH` around `AXIS_X` (design D4). Verify: the housing bounding box has zmax 4.00 and zmin −0.50, and `isValid()` is true.
- [x] 3.2 Replace the rectangular flange notch with the trapezoid (2.7 wide at the top, 2.0 at the bottom, 0.7 deep), centred on `AXIS_X` and running from the flange rear through the nose tip. Verify visually in `uv run pj3106m-build --preview` (front SVG) that the notch interrupts the flat rim.
- [x] 3.3 Lower the shell side walls to `SHELL_SIDE_BOTTOM` = 0.10. The housing side pocket follows automatically. Then confirm that pins 1 and 4 (under the shell) still get no side tab and that no solid overlaps another. Verify: `test_solids_do_not_overlap` passes.
- [x] 3.4 Update the shell window size and height from the new parameters, and check that `build_leads` uses `LEAD_WIDTH` 1.0 and `LEAD_THICKNESS` 0.2. Verify: `uv run pj3106m-build` succeeds, and the STEP re-imports with 8 solids.

## 4. Dimensional tests

- [x] 4.1 Rewrite the constants in `tests/test_pj3106m.py`: FRONT_Y 7.125, AXIS_X 0, AXIS_Z 1.85, the new PINS, PAD_ACROSS 2.60, PAD_CENTRE_X 3.10, FLANGE 0.60, SHELL 0.6–3.5, NOSE_TIP_Y = FRONT_Y + 1.00, and LEAD_TIP span tolerance 0.3. Move the probes that assumed a 2 mm nose. Verify: the existing tests pass with the new values.
- [x] 4.2 Update the bounding-box expectations to length 13.00, Z max 4.00 and Z min −0.50 (both the fused-solid and STL tests). Set the peg to 10.70 behind the front face, Ø1.10–1.20, projecting 0.50, and the below-board nose width to ≤ 3.05. Verify: `uv run pytest tests/test_pj3106m.py` passes.
- [x] 4.3 Add tests for the new spec scenarios: nothing above Z = 4.05 (flat top), the nose top flush at 4.00 ± 0.05, the shell side wall bottom ≤ 0.15 at the shell mid-Y, and pins 2/4/5 on +X with 1/3/6 on −X. Verify: each new test fails when its parameter is temporarily reverted (for example NOSE flats removed, SHELL_SIDE_BOTTOM back to 0.35), then passes again when restored.

## 5. README

- [x] 5.1 Replace the "Source documents" identity table with the rev A identity, the SHA and LCSC C7428681 (datasheet + photos `20230720_HOOYA-PJ-3106M_C7428681_*`). Say that the earlier model wrongly used C2939583 (PJ-31060). Keep the `pj3106m-datasheet` usage text, but drop the rev A2 wording and `PJ-31060.pdf` example names. Verify: `uv run pytest tests/test_source_documents.py` passes, and `grep -n "A2\|31060新模" README.md` finds only the deliberate "replaces the older rev A2 scan" note, if any.
- [x] 5.2 Add a "Provenance" section (source drawing; estimates measured off the 1200 dpi raster with each view calibrated on its own printed dimension; photos used for colours/appearance and the shell wall extent) and a "Dimensions" table (Feature | mm | Source). It covers every row of the design D1 table that sets visible geometry, and the peg is listed as "Ø1.2 +0/−0.1 → 1.15". Verify: the table renders in a Markdown preview.
- [x] 5.3 Update the feature bullets, the coordinate-frame text (front face Y +7.125, nose tip +8.125, peg (0, −3.575), axis X 0 Z 1.85, nose and peg 0.50 below the board, top flat at 4.00) and the pad table. Pads are 1.50 (Y) × 2.60 (X): pin 1 (−3.10, −4.375), 3 (−3.10, −1.625), 6 (−3.10, +3.375), 4 (+3.10, −4.375), 2 (+3.10, +2.275), 5 (+3.10, +4.375). Add the NPTH Ø1.60 at (0, +3.575) and a 3.20 wide cutout reaching 1.10 behind the board edge. Verify: the README numbers match `params.py` by inspection and through task 5.4.
- [x] 5.4 Add `tests/test_readme_dimensions.py`. It parses the README "Dimensions" table, maps each Feature to its `params` names and its expected Source tag through explicit dicts in the test, and asserts equality. Verify: it passes, and it fails if one README value is edited.

## 6. Outputs and final check

- [x] 6.1 Run `uv run pj3106m-build --render` and commit `models/PJ-3106M.step`, `models/PJ-3106M.stl` and `docs/PJ-3106M_iso.png`. Verify: the new image shows the flat rim flush with the housing top and gold shell walls reaching the board, and `test_committed_outputs_are_current` passes.
- [x] 6.2 Run the full suite and the spec validation. Verify: `uv run pytest` is all green, `openspec validate rebase-on-pj3106m-rev-a --strict` passes, and `git status` shows no files under `local/` staged.
