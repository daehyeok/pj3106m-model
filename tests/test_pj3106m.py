"""Dimensional checks for the PJ-3106M model against the datasheet.

Expected values are hard-coded from the PJ-3106M (YBC01) drawing rev A (LCSC
C7428681; identity and SHA-256 in pj3106m_model.params; the file itself is not
in git) on purpose and are NOT imported from pj3106m_model.params, so a wrong
parameter is caught instead of being compared against itself.

Model frame: Z=0 seating plane, plug opening toward +Y, pins 2/4/5 on +X,
origin at the six-pad centroid. The housing front face is therefore at
Y = 7.125 (pads span 2.00..12.25 mm behind the front face).
"""

from pathlib import Path

import cadquery as cq
import pytest
import trimesh

from pj3106m_model.build import export
from pj3106m_model.model import build_fused, build_housing, build_leads, build_shell

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FRONT_Y = 7.125
AXIS_X = 0.0  # on the housing centreline (end view)
AXIS_Z = 1.85
TOL_SMALL = 0.1  # datasheet: up to 5 mm
TOL_LARGE = 0.2  # datasheet: above 5 mm

# Pin -> (lead centre distance behind front face, side sign of X), PCB layout.
PINS = {
    1: (2.75, -1),
    2: (9.40, +1),
    3: (5.50, -1),
    4: (2.75, +1),
    5: (11.50, +1),
    6: (10.50, -1),
}
PAD_ACROSS = 2.60
PAD_ALONG = 1.50
PAD_CENTRE_X = 3.10  # outer pad edges 8.80 apart, pads 2.60 across (PCB layout)

# Details (design.md D1; drawing views and LCSC C7428681 photos).
FLANGE_REAR_Y = FRONT_Y - 0.60  # flange 0.6 thick
SHELL_REAR_Y = FRONT_Y - 3.50  # gold shell 0.6..3.5 behind the front face
SHELL_MID_Y = (FLANGE_REAR_Y + SHELL_REAR_Y) / 2
NOSE_TIP_Y = FRONT_Y + 1.00
LEAD_TIP_X = 8.30 / 2


@pytest.fixture(scope="module")
def shell():
    return build_shell()


@pytest.fixture(scope="module")
def housing():
    return build_housing()


@pytest.fixture(scope="module")
def leads():
    return build_leads()


@pytest.fixture(scope="module")
def fused():
    return build_fused()


def assert_close(name, actual, expected, tol):
    assert abs(actual - expected) <= tol, (
        f"{name}: {actual:.3f} mm, expected {expected:.2f} +/- {tol} mm"
    )


def inside(solid, x, y, z):
    return solid.isInside(cq.Vector(x, y, z), 1e-4)


# --- Outline ---------------------------------------------------------------


def test_overall_bounding_box(fused):
    bb = fused.BoundingBox()
    assert_close("overall length (Y)", bb.ylen, 13.00, TOL_LARGE)
    assert_close("lead tip span (X)", bb.xlen, 8.30, 0.30)
    assert_close("top (Z max)", bb.zmax, 4.00, TOL_SMALL)
    assert_close("nose/peg bottom (Z min)", bb.zmin, -0.50, TOL_SMALL)
    assert_close("nose tip Y", bb.ymax, FRONT_Y + 1.00, TOL_SMALL)
    assert_close("housing rear Y", bb.ymin, FRONT_Y - 12.00, TOL_LARGE)


def test_housing_box(housing):
    # Probe away from the nose: flat top at 4.00, sides at +/-3.20.
    assert inside(housing, -2.5, 0, 3.95), "housing top below 4.00"
    assert not inside(housing, -2.5, 0, 4.05), "housing top above 4.00"
    assert inside(housing, 3.15, 0, 3.0), "housing narrower than 6.40"
    assert not inside(housing, 3.25, 0, 3.0), "housing wider than 6.40"
    assert inside(housing, -3.15, 0, 3.0), "housing narrower than 6.40"
    assert not inside(housing, -3.25, 0, 3.0), "housing wider than 6.40"
    assert inside(housing, -2.5, FRONT_Y - 0.05, 3.0), "housing front face misplaced"
    assert not inside(housing, -2.5, FRONT_Y + 0.05, 3.0), "housing front face misplaced"


# --- Nose / bore -----------------------------------------------------------


def test_plug_bore(housing):
    y = FRONT_Y + 0.5  # inside the nose
    assert not inside(housing, AXIS_X, y, AXIS_Z), "bore not open on the plug axis"
    # Bore radius 1.80 +/- 0.025 (diameter 3.60 +/- 0.05).
    assert not inside(housing, AXIS_X + 1.77, y, AXIS_Z), "bore smaller than 3.60"
    assert inside(housing, AXIS_X + 1.83, y, AXIS_Z), "bore larger than 3.60"
    assert not inside(housing, AXIS_X - 1.77, y, AXIS_Z), "bore off-centre (+X)"
    assert inside(housing, AXIS_X - 1.83, y, AXIS_Z), "bore off-centre (-X)"
    # The top of the bore is opened by the rim notch, so check from below.
    assert not inside(housing, AXIS_X, y, AXIS_Z - 1.77), "bore axis too high"
    assert inside(housing, AXIS_X, y, AXIS_Z - 1.83), "bore axis too low"
    # Bore is open at the nose tip.
    assert not inside(housing, AXIS_X, FRONT_Y + 0.99, AXIS_Z), "bore not open at tip"


def test_flat_top(fused):
    slab = cq.Solid.makeBox(40, 40, 10, cq.Vector(-20, -20, 4.05))
    vol = fused.intersect(slab).Volume()
    assert vol < 1e-9, f"{vol:.6f} mm^3 of the part is above 4.05"


def test_nose_rim_flush_with_top(housing):
    # Part of the housing in front of the front face = the nose.
    front = cq.Solid.makeBox(20, 5, 20, cq.Vector(-10, FRONT_Y + 0.01, -10))
    bb = housing.intersect(front).BoundingBox()
    assert_close("nose top", bb.zmax, 4.00, 0.05)
    assert inside(housing, AXIS_X + 2.2, FRONT_Y + 0.5, 3.0), "nose missing at the side"


def test_nose_below_board(housing):
    below = cq.Workplane("XY").box(20, 20, 5, centered=(True, True, False))
    below = below.translate((0, 0, -5)).val()
    # Keep only the front region (exclude the rear peg).
    front = cq.Workplane("XY").box(20, 10, 10).translate((0, FRONT_Y, 0)).val()
    part = housing.intersect(below).intersect(front)
    bb = part.BoundingBox()
    assert_close("nose lowest point", bb.zmin, -0.50, TOL_SMALL)
    assert bb.xlen <= 3.05, f"below-board nose width {bb.xlen:.3f} > 3.05"


def test_locating_peg(housing):
    y = FRONT_Y - 10.70
    assert inside(housing, AXIS_X, y, -0.3), "no peg 10.70 behind the front face"
    assert inside(housing, AXIS_X + 0.54, y, -0.3), "peg narrower than 1.10"
    assert not inside(housing, AXIS_X + 0.61, y, -0.3), "peg wider than 1.20"
    assert not inside(housing, AXIS_X, y - 0.8, -0.3), "peg misplaced along Y"
    assert not inside(housing, AXIS_X, y + 0.8, -0.3), "peg misplaced along Y"
    assert inside(housing, AXIS_X, y, -0.45), "peg shorter than 0.50"
    assert not inside(housing, AXIS_X, y, -0.55), "peg longer than 0.50"


# --- Leads -----------------------------------------------------------------


def test_six_leads(leads):
    assert sorted(leads) == [1, 2, 3, 4, 5, 6]


@pytest.mark.parametrize("pin", sorted(PINS))
def test_lead_on_pad(leads, pin):
    dist, side = PINS[pin]
    bb = leads[pin].BoundingBox()
    pad_y = FRONT_Y - dist
    pad_x = side * PAD_CENTRE_X
    assert_close(f"pin {pin} bottom Z", bb.zmin, 0.0, 1e-3)
    assert pad_y - PAD_ALONG / 2 <= bb.ymin and bb.ymax <= pad_y + PAD_ALONG / 2, (
        f"pin {pin} Y {bb.ymin:.2f}..{bb.ymax:.2f} outside pad "
        f"{pad_y - PAD_ALONG / 2:.2f}..{pad_y + PAD_ALONG / 2:.2f}"
    )
    # Only the part of the lead outside the housing has to land on the pad.
    x_outer = bb.xmax if side > 0 else -bb.xmin
    assert x_outer <= abs(pad_x) + PAD_ACROSS / 2, f"pin {pin} overhangs its pad"
    assert_close(f"pin {pin} tip |X|", x_outer, 8.30 / 2, 0.15)
    assert_close(f"pin {pin} width", bb.ylen, 1.00, 0.05)


@pytest.mark.parametrize("pin", sorted(PINS))
def test_pin_side(leads, pin):
    _, side = PINS[pin]
    centre_x = leads[pin].Center().x
    assert centre_x * side > 0, f"pin {pin} is on the wrong side (X={centre_x:.2f})"


@pytest.mark.parametrize("pin", sorted(PINS))
def test_lead_fork(leads, pin):
    dist, side = PINS[pin]
    y = FRONT_Y - dist
    lead = leads[pin]
    assert not inside(lead, side * (LEAD_TIP_X - 0.1), y, 0.1), (
        f"pin {pin} has no fork notch at its tip"
    )
    assert inside(lead, side * (LEAD_TIP_X - 0.1), y + 0.33, 0.1), (
        f"pin {pin} fork too wide (no material beside the notch)"
    )


# --- Tier A details --------------------------------------------------------


def test_shell_envelope(shell):
    assert shell.isValid()
    bb = shell.BoundingBox()
    assert bb.xmax <= 3.20 + 1e-6 and bb.xmin >= -3.20 - 1e-6, (
        f"shell outside the 6.40 width: X {bb.xmin:.3f}..{bb.xmax:.3f}"
    )
    assert bb.zmax <= 4.00 + 1e-6, f"shell above the 4.00 top: {bb.zmax:.3f}"
    assert_close("shell rear edge Y", bb.ymin, SHELL_REAR_Y, TOL_SMALL)
    assert_close("shell front edge Y", bb.ymax, FLANGE_REAR_Y, TOL_SMALL)


def test_shell_covers_top_and_sides(shell):
    assert inside(shell, -2.0, SHELL_MID_Y, 3.93), "no shell on the top"
    assert inside(shell, 3.12, SHELL_MID_Y, 3.0), "no shell on the +X side"
    assert inside(shell, -3.12, SHELL_MID_Y, 3.0), "no shell on the -X side"


def test_shell_side_walls_reach_board(shell):
    assert shell.BoundingBox().zmin <= 0.15, "shell side walls end above 0.15"
    for side in (+1, -1):
        assert inside(shell, side * 3.12, SHELL_MID_Y, 0.14), (
            f"shell side wall (X sign {side}) does not reach 0.15 above the board"
        )
    assert shell.BoundingBox().zmin >= 0.0, "shell side walls go below the board"


def test_shell_v_tongue(shell, housing):
    y = SHELL_REAR_Y + 0.35
    assert not inside(shell, AXIS_X, y, 3.93), "no V opening in the shell top"
    assert inside(housing, AXIS_X, y, 3.70), "no black housing under the V opening"


@pytest.mark.parametrize("side", [+1, -1])
def test_shell_side_window(shell, housing, side):
    assert not inside(shell, side * 3.12, SHELL_MID_Y, 2.0), (
        f"no window in the shell side (X sign {side})"
    )
    assert inside(housing, side * 2.95, SHELL_MID_Y, 2.0), (
        f"no housing behind the shell window (X sign {side})"
    )


def test_flange_notch(housing):
    y = (FLANGE_REAR_Y + FRONT_Y) / 2
    assert not inside(housing, AXIS_X, y, 3.80), "no notch in the flange top"
    assert inside(housing, -2.5, y, 3.80), "flange missing beside the notch"
    assert inside(housing, 2.5, y, 3.80), "flange missing beside the notch"


def test_nose_ring_and_chamfer(housing):
    y_face = NOSE_TIP_Y - 0.05
    assert not inside(housing, AXIS_X + 1.95, y_face, AXIS_Z), "no nose-face recess"
    assert inside(housing, AXIS_X + 2.30, y_face, AXIS_Z), "no raised outer nose ring"
    # Chamfer at the bore entry (bottom of the 0.2 recess).
    assert not inside(housing, AXIS_X + 1.85, NOSE_TIP_Y - 0.25, AXIS_Z), (
        "no chamfer at the bore entry"
    )
    # Bore still 3.60 +/- 0.05 at 1 mm depth.
    y = NOSE_TIP_Y - 1.0
    assert not inside(housing, AXIS_X + 1.77, y, AXIS_Z), "bore smaller than 3.60"
    assert inside(housing, AXIS_X + 1.83, y, AXIS_Z), "bore larger than 3.60"


def test_solids_do_not_overlap(housing, shell, leads):
    pairs = [("housing", housing, "shell", shell)]
    pairs += [("housing", housing, f"pin {p}", s) for p, s in leads.items()]
    pairs += [("shell", shell, f"pin {p}", s) for p, s in leads.items()]
    for name_a, a, name_b, b in pairs:
        vol = a.intersect(b).Volume()
        assert vol < 1e-6, f"{name_a} and {name_b} overlap by {vol:.6f} mm^3"


# --- Exports ---------------------------------------------------------------


@pytest.fixture(scope="module")
def exported(tmp_path_factory):
    return export(tmp_path_factory.mktemp("models"))


def test_fused_is_single_valid_solid(fused):
    assert fused.isValid()


def test_step_export(exported):
    step, _ = exported
    assert step.stat().st_size > 0
    solids = cq.importers.importStep(str(step)).solids().vals()
    assert len(solids) == 8, f"STEP has {len(solids)} solids, expected 8"


def test_stl_export(exported):
    _, stl = exported
    mesh = trimesh.load(str(stl))
    assert len(mesh.faces) > 0
    assert mesh.is_watertight, "STL is not watertight"
    (xmin, ymin, zmin), (xmax, ymax, zmax) = mesh.bounds
    assert_close("STL length (Y)", ymax - ymin, 13.00, TOL_LARGE)
    assert_close("STL width (X)", xmax - xmin, 8.30, 0.30)
    assert_close("STL Z min", zmin, -0.50, TOL_SMALL)
    assert_close("STL Z max", zmax, 4.00, TOL_SMALL)


def test_committed_outputs_are_current(exported):
    step, stl = exported
    committed_step = PROJECT_ROOT / "models" / "PJ-3106M.step"
    committed_stl = PROJECT_ROOT / "models" / "PJ-3106M.stl"
    assert committed_step.exists() and committed_stl.exists(), (
        "models/ outputs missing: run `uv run pj3106m-build`"
    )
    fresh = cq.importers.importStep(str(step))
    old = cq.importers.importStep(str(committed_step))
    assert len(old.solids().vals()) == len(fresh.solids().vals())
    fb, ob = fresh.val().BoundingBox(), old.val().BoundingBox()
    for attr in ("xmin", "xmax", "ymin", "ymax", "zmin", "zmax"):
        assert abs(getattr(fb, attr) - getattr(ob, attr)) < 1e-3, (
            f"committed STEP is stale ({attr}): run `uv run pj3106m-build`"
        )
    fresh_mesh = trimesh.load(str(stl))
    old_mesh = trimesh.load(str(committed_stl))
    assert abs(fresh_mesh.volume - old_mesh.volume) < 1e-3, (
        "committed STL is stale: run `uv run pj3106m-build`"
    )
