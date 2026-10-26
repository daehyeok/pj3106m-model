"""All PJ-3106M model dimensions, in millimetres.

Source: the HAOYU/HOOYA PJ-31060 datasheet identified by the DATASHEET_*
constants below (revision A2, 2021-11-04; LCSC part C2939583). Source documents
are kept outside git; verify a local copy with
``uv run pj3106m-datasheet --datasheet PATH``. The PDF is a scanned drawing;
values marked "estimate" are not dimensioned on it and were measured from the
drawing (scale 1:1 render) or from the LCSC C2939583 product photos.

Coordinate frame (KiCad 3D model convention):
  * Z = 0 is the seating plane (PCB top surface), +Z up.
  * The plug opening faces +Y. Pins 2/4/6 are on +X, pins 1/3/5 on -X
    (the datasheet's "P.C.B LAYOUT TOP VIEW" rotated 90 degrees clockwise).
  * The origin is the centroid of the six-pad pattern (see PAD_CENTROID_FROM_FRONT).
"""

# --- Source document identity (files themselves are not in git) ------------
DATASHEET_VENDOR = "HAOYU (HONGKONG) LIMITED / HOOYA ELECTRONICS"
DATASHEET_MODEL = "PJ-31060新模"  # used in this project as PJ-3106M
DATASHEET_REVISION = "A2"
DATASHEET_DATE = "2021-11-04"
DATASHEET_SHA256 = "939615b14e90b455765f1b6e26bbef588cdcfba269b0a047174ec80916c501fb"
LCSC_PART = "C2939583"  # datasheet + product photos: https://www.lcsc.com/product-detail/C2939583.html

# --- Housing ---------------------------------------------------------------
HOUSING_LENGTH = 12.00  # side view, *i
HOUSING_WIDTH = 6.40  # front view, *f
HOUSING_HEIGHT = 4.00  # front view, *e

# --- Plug axis / nose ------------------------------------------------------
OVERALL_LENGTH = 14.00  # side view, *h (housing + nose)
NOSE_PROJECTION = OVERALL_LENGTH - HOUSING_LENGTH  # 2.00, nose in front of housing
AXIS_HEIGHT = 1.90  # front view: plug axis above seating plane
AXIS_FROM_PIN246_SIDE = 3.10  # front view: axis to the pin-2/4/6 housing side
# Lateral offset of the axis from the housing centreline, toward +X (pins 2/4/6).
AXIS_X = HOUSING_WIDTH / 2 - AXIS_FROM_PIN246_SIDE  # +0.10
NOSE_DIAMETER = 5.00  # estimate; matches the 3.20 board-cutout chord at Z=0
NOSE_INTO_HOUSING = 1.00  # estimate (0.95 side view / 1.20 PCB layout)
NOSE_FRONT_FILLET = 0.15  # estimate, cosmetic
BORE_DIAMETER = 3.60  # front view, +/-0.05
BORE_DEPTH = 11.00  # estimate, measured from the nose tip (blind)
# Nose face: an inner annulus is recessed so the outer rim reads as a raised
# ring without lengthening the part (photos, datasheet 3D view).
NOSE_RECESS_OUTER_DIAMETER = 4.20  # estimate (photo)
NOSE_RECESS_DEPTH = 0.20  # estimate (photo)
BORE_CHAMFER = 0.20  # estimate (photo), 45 deg at the bore entry

# --- Front flange (first section of the housing) ---------------------------
FLANGE_THICKNESS = 0.70  # side view (front section ahead of the shell)
FLANGE_NOTCH_WIDTH = 1.00  # estimate (photo), centred on the plug axis X
FLANGE_NOTCH_DEPTH = 0.40  # estimate (photo), from the top

# --- Gold front shell ------------------------------------------------------
# Covers top and both sides from FLANGE_THICKNESS to SHELL_REAR_FROM_FRONT
# behind the front face (side view; top view front block ~3.36).
SHELL_REAR_FROM_FRONT = 3.30  # side view
SHELL_THICKNESS = 0.15  # estimate; sits in a pocket so the envelope is unchanged
SHELL_SIDE_BOTTOM = 0.35  # estimate (photo); clears the lead feet
SHELL_V_REAR_WIDTH = 2.40  # top view V spring / photo, estimate
SHELL_V_APEX_GAP = 0.40  # estimate: V apex distance from the shell's front edge
SHELL_WINDOW_LENGTH = 1.20  # side view rounded window (along Y), estimate
SHELL_WINDOW_HEIGHT = 1.00  # side view rounded window (Z), estimate
SHELL_WINDOW_Z = 2.00  # estimate, window centre height
SHELL_FUSE_OVERLAP = 0.005  # internal: shell overlap into the pocket, fused STL path only

# --- Rear locating peg -----------------------------------------------------
PEG_FROM_FRONT = 10.55  # side view & PCB layout (PCB hole is 1.50)
PEG_DIAMETER = 1.15  # side view, 1.15 +/-0.05
PEG_LENGTH = 0.60  # estimate, below the seating plane

# --- Leads -----------------------------------------------------------------
# Lead centre distance from the housing front face, along the plug axis
# (component top view & PCB layout).
PIN_FROM_FRONT = {
    1: 2.80,
    2: 2.85,
    3: 5.45,
    4: 9.40,
    5: 10.50,
    6: 11.50,
}
PIN_SIDE = {1: -1, 3: -1, 5: -1, 2: +1, 4: +1, 6: +1}  # sign of X
LEAD_TIP_SPAN = 8.30  # front view, *g, +/-0.25
LEAD_WIDTH = 0.80  # estimate, along the plug axis
LEAD_THICKNESS = 0.25  # estimate
LEAD_TAB_HEIGHT = 1.50  # estimate, vertical tab up the housing side
LEAD_OVERLAP = 0.05  # internal: overlap into the housing, fused STL path only
LEAD_FORK_DIAMETER = 0.50  # photo (back) / datasheet lead outline, estimate

# --- Footprint reference ---------------------------------------------------
PAD_ALONG_AXIS = 1.50  # PCB layout, 6-2.00X1.50
# Pads run from 2.80 - 0.75 = 2.05 to 11.50 + 0.75 = 12.25 behind the front face.
PAD_CENTROID_FROM_FRONT = (
    min(PIN_FROM_FRONT.values()) - PAD_ALONG_AXIS / 2
    + max(PIN_FROM_FRONT.values()) + PAD_ALONG_AXIS / 2
) / 2  # 7.15
# Y of the housing front face in model space. Change this to move the origin.
FRONT_Y = PAD_CENTROID_FROM_FRONT

# --- Appearance ------------------------------------------------------------
HOUSING_COLOR = (0.06, 0.06, 0.07)  # matte near-black PPA (LCSC C2939583 photos)
LEAD_COLOR = (0.90, 0.72, 0.35)  # Au-plated leads (photos)
SHELL_COLOR = LEAD_COLOR  # gold front shell (photos)
