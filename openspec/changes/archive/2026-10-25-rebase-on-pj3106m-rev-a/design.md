## Context

See proposal.md (Why) for the motivation. The current state:

- **Geometry and parameters.** All geometry is built in `src/pj3106m_model/model.py` from
  named constants in `src/pj3106m_model/params.py`. Each constant is commented with its
  source. The housing, the nose and the peg are one solid. The gold U-shell sits in a
  0.15 mm pocket, so the 6.40 × 4.00 envelope is unchanged. Each lead is a forked foot plus
  an optional side tab.
- **Nose.** The nose is a plain Ø5.0 cylinder on the axis at Z 1.90. Its top therefore
  reaches 4.40 and its bottom −0.60. Only the shell's top pocket trims it, and only inside
  the shell zone.
- **Tests.** `tests/test_pj3106m.py` hard-codes the expected values so a wrong parameter
  can't pass by being compared with itself. It also checks that the STEP has 8 solids, the
  STL is watertight and the committed outputs aren't stale.

The new source is the local copy of `PJ-3106M.pdf`. It is the datasheet that the LCSC C7428681
(HOOYA PJ-3106M) page serves: the SHA-256 was checked against
`datasheet.lcsc.com/.../0a871354539e12460c0b28cf68bdf9b3.pdf`. The old rev A2 scan
(SHA `9396…`) is the C2939583 (PJ-31060) datasheet, so every rev A2 value and every photo
estimate from that listing is suspect. All values are re-derived below. The matching
photos are `20230720_HOOYA-PJ-3106M_C7428681_{front,back,blank}.jpg` (copied into `local/`,
which is gitignored). It is a vector drawing of PJ-3106M (YBC01), rev A,
created 2019-09-10, SHA-256 `88db1b26…6ea4f`. The file stays outside git. The values below
were read from the drawing, rasterised at 1200 dpi. Each view was calibrated on a dimension
printed on that view:

- front view: the 4.0 height
- side view: the 12.0 housing length
- top view: the 11.5 pin-5 position
- end view: the 6.4 width
- right view: the 4.0 height

## Goals / Non-Goals

**Goals:**

- Every value printed on the rev A drawing is used as printed and tagged `datasheet`.
  Everything else is measured off the drawing (or taken from the photos where the drawing
  is silent) and tagged `estimate`.
- The nose rim is flush with the housing top, so the part's highest point is 4.00. The
  below-board part of the nose fits the 3.2 mm board cutout.
- The README dimension table and `params.py` can't drift apart: a test checks one against
  the other.

**Non-Goals:**

- Making a KiCad footprint file. The README pad table is still the only footprint
  guidance.
- Modelling the gold ground-spring tongue that drops into the flange notch, the top
  windows, or the asymmetric pin-4 pad offset that the PCB layout hints at but doesn't
  dimension (and that isn't drawn to scale).
- Keeping backward compatibility with the rev A2 numbering or origin.

## Decisions

### D1. Parameter values

"ds" means the value is printed on the rev A drawing. "est" means it was measured off the
drawing or judged from the photos.

| Parameter | Old | New | Source (rev A view) |
|---|---|---|---|
| HOUSING_LENGTH | 12.00 | 12.00 | ds, side view 12±0.3 |
| HOUSING_WIDTH / HEIGHT | 6.40 / 4.00 | 6.40 / 4.00 | ds, end view 6.4, front view 4 (*j) |
| NOSE_PROJECTION | 2.00 | **1.00** | ds, side view "1" (overall length 13.0, derived) |
| AXIS_HEIGHT | 1.90 | **1.85** | ds, front view 1,85 |
| AXIS_X | +0.10 | **0.00** | est, see D2 |
| BORE_DIAMETER | 3.60 | 3.60 | ds, front view Ø3.6±0.05 (*i) |
| NOSE_DIAMETER | 5.00 | 5.00 | est, front view outer circle measures 5.05 |
| NOSE_INTO_HOUSING | 1.00 | **1.10** | ds, PCB layout: board cutout starts 1.1 behind the edge |
| NOSE_DIP (new) | (0.60 implied) | **0.50** | est, front view 0.53, side view 0.48 |
| NOSE_BELOW_BOARD_WIDTH (new) | none | **3.00** | ds, end view "3" |
| NOSE_RECESS_OUTER_DIAMETER | 4.20 | **4.00** | est, front view inner ring circle about 4.05 |
| NOSE_RECESS_DEPTH, BORE_CHAMFER | 0.20, 0.20 | unchanged | est (photo) |
| BORE_DEPTH | 11.00 | 11.00 | est, from the nose tip |
| FLANGE_THICKNESS | 0.70 | **0.60** | est, top view 0.63, right view 0.60 |
| FLANGE_NOTCH | 1.0 wide × 0.4 deep, rectangular | **trapezoid: 2.7 wide at top, 2.0 at bottom, 0.7 deep** | est, front view |
| SHELL_REAR_FROM_FRONT | 3.30 | **3.50** | est, side 3.6, right 3.5, top 3.45 |
| SHELL_THICKNESS | 0.15 | 0.15 | est |
| SHELL_SIDE_BOTTOM | 0.35 | **0.10** | est, photos (D4) |
| SHELL_WINDOW L × H, Z centre | 1.20 × 1.00, 2.00 | **1.60 × 1.30, 2.10** | est, right view |
| SHELL_V_REAR_WIDTH / APEX_GAP | 2.40 / 0.40 | unchanged | est (photo) |
| PEG_FROM_FRONT | 10.55 | **10.70** | ds, side view 10.7 (*a), PCB layout 10.7 |
| PEG_DIAMETER | 1.15 | **1.15** | ds, Ø1.2 +0/−0.10, centre of the band |
| PEG_LENGTH | 0.60 | **0.50** | ds, right view 0,5 |
| PIN_FROM_FRONT | 1:2.80 2:2.85 3:5.45 4:9.40 5:10.50 6:11.50 | **1:2.75 2:9.40 3:5.50 4:2.75 5:11.50 6:10.50** | ds, top view and PCB layout |
| PIN_SIDE | +X: 2/4/6 | **+X: 2/4/5; −X: 1/3/6** | ds, top view (D3) |
| LEAD_TIP_SPAN | 8.30 | 8.30 | ds, 8,3±0.30 (*b) |
| LEAD_WIDTH | 0.80 | **1.00** | ds, top view "6-1" |
| LEAD_THICKNESS | 0.25 | **0.20** | ds, end view "0,2thk" |
| LEAD_TAB_HEIGHT, LEAD_FORK_DIAMETER | 1.50, 0.50 | unchanged | est |
| PAD (along axis × across) | 1.50 × 2.00 | **1.50 × 2.60**, outer span 8.80 | ds, PCB layout 6-1.5*2.6, 8.8 |
| PCB_HOLE_DIAMETER, NOSE_CUTOUT_WIDTH (new, README only) | 1.50, 3.20 | **1.60, 3.20** | ds, PCB layout |

The pads run from 2.75 − 0.75 = 2.00 to 11.50 + 0.75 = 12.25 behind the front face, so the
pad centroid is 7.125 behind it. That gives `FRONT_Y` = 7.125. The pad centres are at
X = ±(8.80/2 − 2.60/2) = ±3.10. Each lead foot runs from X = 3.20 to 4.15, which is inside
its pad's 1.80–4.40.

Alternative considered: keep the rev A2 values wherever they are within tolerance of
rev A, for example 2.80 against 2.75. Rejected, because the README table would then cite a
document that isn't the source.

### D2. Plug axis on the housing centreline

Rev A gives no dimension for a lateral offset. In the end view, the 3 mm nose chord and
the 6.4 width share one centre line. The front view looks about 0.2 mm off-centre, but
it's undimensioned and drafting skew is plausible. So AXIS_X = 0 (est), and the README
table records it that way. Rev A2's 3.10/3.30 split doesn't apply to this drawing.

### D3. Pin numbering and sides

The component top view shows pins 5, 2 and 4 on the left and 6, 3 and 1 on the right, with
the opening at the bottom. The PCB layout shows the same pins with the nose to the right.
Rotating either view so the opening faces +Y puts pins 2, 4 and 5 on +X and pins 1, 3 and
6 on −X. Pins 1 and 4, both at 2.75, sit under the shell zone, so they get no side tab, as
before.

### D4. Flat-top nose and trimmed underside

The Ø5.0 nose cylinder is built first, with its front-edge fillet, and then cut by:

- a half-space above Z = HOUSING_HEIGHT, which gives the flat rim the user pointed out in
  the front view (circles clipped by the 4.0 line);
- a half-space below Z = −NOSE_DIP;
- two blocks below Z = 0 at |X − AXIS_X| > NOSE_BELOW_BOARD_WIDTH/2.

Cutting the finished cylinder keeps the rest of the code as it is. The top cut runs the
full nose length, not just the shell zone. The flange notch is extended forward through
the nose tip, because the front view shows the trapezoid notch interrupting the rim. At
0.7 deep, the notch reaches Z 3.3, below the bore top (3.65), so it opens into the bore as
on the real part (the photo shows the ground tongue entering there).

The end view of the drawing still shows an arc above the housing top. It conflicts with
the front view. We follow the front view and the photos, which agree with the user's
reading.

The nose-face recess shrinks to Ø4.0. A Ø4.2 recess would leave only 0.05 of rim under
the 4.00 flat. At Ø4.0 its top is at 3.85, which leaves a 0.15 rim.

### D5. Shell side walls lowered to 0.10

The drawing's side views put the shell bottom about 0.5 mm up. In the photos the gold
wall runs almost to the board and merges visually with the pin 1 and pin 4 feet. The user
allowed the gold parts to be extended to an estimated length. We choose 0.10 mm: close to
the board, but not touching the seating plane, which leaves room for solder. The wall
occupies X 3.05–3.20 and the lead feet start at X = 3.20, so in the STEP assembly they
share at most a face and have no common volume. In the fused STL, `LEAD_OVERLAP` makes the
two overlap slightly, and the union absorbs it. The housing side pocket follows
SHELL_SIDE_BOTTOM automatically.

Alternative considered: 0.0, flush with the board. Rejected: a part that touches the
seating plane looks like a solder contact, and the shell isn't one.

### D6. README table, checked against params

The README gets a "Provenance" section and a "Dimensions" table (Feature | mm | Source),
in the same style as `skqyace010-model`. The provenance section covers:

- the source drawing identity;
- the estimate method: 1200 dpi raster, each view calibrated on one of its own printed
  dimensions;
- what the photos were used for: colours and appearance, plus the shell wall extent.

A new test, `tests/test_readme_dimensions.py`, parses the table. It maps each Feature row
to one or more `params` names with an explicit dict in the test, then asserts that the
numbers are equal (to 1e-6) and that the Source column matches a `datasheet`/`estimate`
tag dict, also kept in the test. This catches drift without making `params.py` generate
the README.

Alternative considered: generate the table from `params.py` at build time. Rejected: it
adds a build step and makes the README a generated file, which is more than this needs.

### D7. Test expectations stay hard-coded

`tests/test_pj3106m.py` keeps its independent constants, now set to the new values. The
changes:

- FRONT_Y 7.125, AXIS 0 / 1.85, the new PINS and pad size;
- Z max 4.00, Z min −0.50, length 13.00;
- the probe positions move, because the nose is now 1.0 long;
- new checks: nothing above 4.05, below-board width ≤ 3.05, shell wall bottom ≤ 0.15.

## Risks / Trade-offs

- [Footprints drawn from the old README pad table no longer match] → Call this out as
  BREAKING in the proposal and the commit message, and put the new pad table in the README.
- [Shell walls at 0.10 contradict the drawing's ≈0.5] → Tag the value `estimate (photos)`
  in the table. Changing it is a one-parameter edit.
- [Estimates are measured off a drawing that isn't to scale (the PCB layout clearly isn't)]
  → Measure only the mechanical views, calibrate each view on its own printed dimension,
  and never take a value from the PCB layout by measuring it.
- [The flat-top cut could split the nose solid or leave slivers near the notch and shell
  pocket] → The existing `isValid()` test, the 8-solid STEP check and the watertight STL
  check cover this.
- [Peg nominal: Ø1.2 printed against 1.15 modelled] → The drawing tolerance is +0/−0.10,
  so 1.15 is the centre of the band. The README lists it as "Ø1.2 +0/−0.1 → 1.15".

## Migration Plan

1. Update `params.py`, `model.py`, the tests and the README together in one commit, then
   regenerate `models/` and `docs/PJ-3106M_iso.png` with `uv run pj3106m-build --render`.
2. Consumers update their footprints from the new README pad table.
3. To roll back, revert the commit. The old outputs are in git history.

### D8. Photo cross-check (C7428681)

The real PJ-3106M photos confirm several choices:

- The nose is short (about 1 mm) and its rim is flush with the housing top.
- A square flange sits behind the nose, with a notch above the bore. Two black housing ribs
  run back from the notch corners into slots in the shell top, and they read as the "V" in
  the drawing's front view.
- The gold shell side walls run almost to the board (D5).

They disagree with the drawing in one place. The photos show a smaller side window, lower
and further back. The drawing wins, so the window keeps its right-view values. The V cut
stays a simple V, as a stand-in for the ribs and slots.
