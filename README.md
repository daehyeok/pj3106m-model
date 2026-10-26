# PJ-3106M 3D model

A simplified 3D model of the **PJ-3106M** 3.5 mm 4-pole SMD phone jack, for the KiCad
footprint 3D viewer. It is generated with [CadQuery](https://cadquery.readthedocs.io/) from
the vendor datasheet (HAOYU/HOOYA "PJ-31060新模", rev A2). See
[Source documents](#source-documents).

Outputs (committed, so you don't need Python just to use the model):

| File | Use |
|---|---|
| [`models/PJ-3106M.step`](models/PJ-3106M.step) | KiCad 3D model: 8 coloured solids (black housing, gold front shell, 6 gold leads) |
| [`models/PJ-3106M.stl`](models/PJ-3106M.stl) | Single watertight mesh (mm) |

The model is simplified but recognisable. Features:

- **Housing** (matte near-black) with a square front flange (notched at the top), the
  round nose with a raised outer ring, the Ø3.60 plug bore with a chamfered entry, and the
  rear locating peg.
- **Gold front shell** over the top and sides of the front section, with a V-shaped
  tongue on top and a window in each side. It sits in a pocket, so the 6.40 × 4.00
  envelope is unchanged.
- **Six gold SMD leads** with forked tips. The two leads under the shell (pins 1, 2) have
  no side tab.

Out of scope: internal contacts and springs, top windows, the embossed marking, and the
underside channels. Shapes and colours follow the datasheet and the LCSC C2939583 product
photos. Every dimension is a named parameter in
[`src/pj3106m_model/params.py`](src/pj3106m_model/params.py), with a comment citing the
datasheet view or photo it comes from, or marking it as an estimate.

## Source documents

The datasheet and product photos are **not stored in git**. The model, tests and build
don't need them. They're identified by:

| | |
|---|---|
| Vendor / model | HAOYU (HONGKONG) LIMITED / HOOYA ELECTRONICS, "PJ-31060新模" (used here as PJ-3106M) |
| Datasheet revision | A2, 2021-11-04 (scanned drawing, 1 page) |
| Datasheet SHA-256 | `939615b14e90b455765f1b6e26bbef588cdcfba269b0a047174ec80916c501fb` |
| Distributor | LCSC [C2939583](https://www.lcsc.com/product-detail/C2939583.html): datasheet PDF and product photos (`20230107_HOOYA-PJ-31060_C2939583_{front,back,blank}.jpg`) |

To check a downloaded copy anywhere on disk (the path isn't recorded anywhere):

```sh
uv run pj3106m-datasheet --datasheet ~/Downloads/PJ-31060.pdf
# or
export PJ3106M_DATASHEET=~/Downloads/PJ-31060.pdf
uv run pj3106m-datasheet
```

The command exits 0 on a match, 1 if the file is a different revision (it prints both
hashes; compare the rev A2 dimensions in `params.py` by hand), and 2 if no path is given
or the file is missing. If you keep copies inside the repo, put them in `local/`, which
is gitignored.

## Setup

1. Install [uv](https://docs.astral.sh/uv/):

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh   # or: pipx install uv / brew install uv
   ```

2. Create the environment. uv installs the pinned Python (3.12, from `.python-version`;
   CadQuery needs 3.10–3.12) and the locked dependencies from `uv.lock`:

   ```sh
   uv sync
   ```

   > **Network filesystem checkouts:** keep the large venv out of the workspace
   > and avoid hard-link warnings:
   >
   > ```sh
   > export UV_PROJECT_ENVIRONMENT="$HOME/.venvs/pj3106m"
   > export UV_LINK_MODE=copy
   > ```
   >
   > Set these before every `uv` command (e.g. in your shell rc or a direnv `.envrc`).

## Build and test

```sh
uv run pj3106m-build             # regenerate models/PJ-3106M.{step,stl}
uv run pj3106m-build --preview   # also write SVG projections to build/ (gitignored)
uv run pj3106m-build --out DIR   # write the outputs somewhere else
uv run pytest                    # dimensional checks against the datasheet
```

After changing any geometry, rebuild and commit `models/`. A test fails if the committed
outputs are stale.

## Coordinate frame

The model follows KiCad's 3D model convention, so it needs **no offset, rotation or
scaling** in KiCad:

- Units are mm. **Z = 0 is the seating plane** (PCB top surface) and +Z is up. The nose
  dips 0.60 mm and the peg about 0.60 mm below the board, as on the real part.
- **Origin = centroid of the six-pad pattern.** The housing front face is at Y = +7.15,
  the nose tip at Y = +9.15, the rear peg at (X 0.10, Y −3.40), and the plug axis at
  X = +0.10, Z = 1.90.
- The **plug opening faces +Y** (toward the top of the screen in the footprint editor).
  **Pins 2/4/6 are on +X, pins 1/3/5 on −X.**

Pad centres for a matching footprint (KiCad footprint coordinates, Y pointing down), all
pads 2.00 (X) × 1.50 (Y):

| Pin | X | Y |
|---|---|---|
| 1 | −3.45 | −4.35 |
| 3 | −3.45 | −1.70 |
| 5 | −3.45 | +3.35 |
| 2 | +3.45 | −4.30 |
| 4 | +3.45 | +2.25 |
| 6 | +3.45 | +4.35 |

Plus an NPTH Ø1.50 hole at (+0.10, +3.40). The nose needs a 3.20 mm wide board-edge cutout
(datasheet PCB layout).

To use a different footprint origin, change `FRONT_Y` (and `AXIS_X` for lateral offsets)
in `params.py` and rebuild.

## Using it in KiCad

In the footprint's **3D Models** tab, add the STEP file with offset (0, 0, 0), rotation
(0, 0, 0) and scale 1. For example, using a path variable that points at this repo:

```
${PJ3106M_DIR}/models/PJ-3106M.step
```

## Layout

```
pyproject.toml, .python-version, uv.lock   # reproducible uv environment
src/pj3106m_model/params.py                # every dimension (datasheet-sourced)
src/pj3106m_model/model.py                 # CadQuery geometry
src/pj3106m_model/build.py                 # pj3106m-build CLI
tests/test_pj3106m.py                      # datasheet dimensional tests
models/                                    # committed STEP/STL outputs
openspec/                                  # OpenSpec specs and changes
```

## License

[MIT](LICENSE). This covers the code and the generated models. It does not cover the
vendor datasheet or the product photos, which aren't in this repository.
