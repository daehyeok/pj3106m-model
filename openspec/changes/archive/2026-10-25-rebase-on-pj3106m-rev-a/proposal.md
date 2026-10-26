## Why

The model was built from the wrong part. Its scanned "PJ-31060新模" rev A2 drawing and its
photos come from LCSC C2939583 (HOOYA PJ-31060). The PJ-3106M is LCSC **C7428681**, and that
listing serves the vector drawing **PJ-3106M (YBC01), rev A**. Its SHA-256 matches
the local copy of `PJ-3106M.pdf`. It disagrees with the
model in several places that matter for a KiCad footprint:

- The plug axis is at 1.85, not 1.90.
- The nose projects 1.0 mm (overall length 13.0), not 2.0 (14.0).
- The pin numbering and positions are different.
- The peg is Ø1.2 at 10.7, not Ø1.15 at 10.55.
- The pads are 1.5 × 2.6, not 2.0 × 1.5.

Its front view also shows that the nose rim is cut flat at the housing top. The real part
has no 4.40 mm bump, and its highest point is 4.00 mm. The LCSC C7428681 photos show the
gold front shell reaching almost to the board.

We also want the README to say, for every dimension, whether it comes from the datasheet
or is an estimate, the way the sibling `skqyace010-model` repo does.

## What Changes

- **BREAKING** Switch the LCSC part from C2939583 to C7428681. Switch the source document
  to HAOYU/HOOYA "PJ-3106M (YBC01)" rev A, SHA-256
  `88db1b26c288bbaa0537e7a184d20efc260de7c7e152d95f0d4d86067e96ea4f`. This updates the
  recorded identity, the `pj3106m-datasheet` check, the code comments and the README.
- **BREAKING** Re-base every dimension that disagrees with the new drawing:
  - Plug axis Z 1.85, now on the housing centreline (X 0).
  - Nose projection 1.0, so the overall length is 13.0.
  - Peg Ø1.2 at 10.7 behind the front face, projecting 0.5 below the board.
  - Nose dip 0.5.
  - Lead width 1.0 and thickness 0.2.
  - New lead positions and pin numbering: pins 4/2/5 on +X at 2.75/9.4/11.5, pins 1/3/6
    on −X at 2.75/5.5/10.5.
  - Pads 1.5 × 2.6 with an 8.8 outer span, a Ø1.6 peg hole, and a 3.2 × 1.1 nose cutout.
  - Origin moves to the new six-pad centroid, so the front face is at Y = +7.125.
- **BREAKING** Cut the nose flat at Z = 4.00 (the housing top), so the whole part is
  4.00 mm high. Cut its underside flat at Z = −0.50 and trim the part below the board to
  3.0 mm wide, as in the end view, so it fits the 3.2 mm board cutout.
- Extend the gold front shell's side walls down to just above the seating plane (an
  estimate). Re-measure the shell, flange, notch, window and nose-ring estimates from the
  new vector drawing, and re-check the photo-based estimates against the C7428681 photos.
- Add a README "Dimensions" table (Feature | mm | Source = datasheet / estimate) and a
  provenance section that says how the estimates were measured. Update the pad table,
  coordinate-frame text and source-document identity.
- Regenerate `models/PJ-3106M.{step,stl}` and `docs/PJ-3106M_iso.png`, and update the
  tests to the new values.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `jack-3d-model`: changes the source datasheet identity, the outline dimensions (axis
  1.85, overall length 13.0, flat top at 4.00), the nose and peg features, the front shell
  side-wall extent, the lead positions, pin sides and pad size, and the coordinate-frame
  origin.
- `dev-environment`: the datasheet check now targets rev A of PJ-3106M, and the README must
  include a dimension provenance table.

## Impact

- Code: `src/pj3106m_model/params.py` (most values), `src/pj3106m_model/model.py` (nose
  flats, below-board trim, shell walls, notch shape), `src/pj3106m_model/datasheet.py`
  messages.
- Tests: `tests/test_pj3106m.py` (every expected value), `tests/test_datasheet.py`
  (revision check).
- Outputs: `models/PJ-3106M.step`, `models/PJ-3106M.stl` and `docs/PJ-3106M_iso.png`
  regenerated.
- Docs: `README.md`.
- Users: KiCad footprints built from the old README pad table (2.0 × 1.5 pads, old pin
  numbering, front face at Y = 7.15) no longer line up with the model. They must be redrawn
  from the new pad table.
