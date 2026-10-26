"""All PJ-3106M model dimensions, in millimetres.

Source: the HAOYU/HOOYA "PJ-3106M (YBC01)" drawing identified by the
DATASHEET_* constants below (revision A, vector PDF; LCSC part C7428681,
which serves this exact PDF and the product photos). Source documents are kept outside git; verify a local copy with
``uv run pj3106m-datasheet --datasheet PATH``.

Every value is tagged "datasheet (<view>)" when it is printed on the drawing,
or "estimate" when it was measured off the drawing (rasterised at 1200 dpi,
each view calibrated on one of its own printed dimensions) or judged from the
LCSC C7428681 product photos.

Coordinate frame (KiCad 3D model convention):
  * Z = 0 is the seating plane (PCB top surface), +Z up.
  * The plug opening faces +Y. Pins 2/4/5 are on +X, pins 1/3/6 on -X
    (the datasheet's component top view rotated so the opening points up).
  * The origin is the centroid of the six-pad pattern (see PAD_CENTROID_FROM_FRONT).
"""

# --- Source document identity (files themselves are not in git) ------------
DATASHEET_VENDOR = "HAOYU (HONGKONG) LIMITED / HOOYA ELECTRONICS"
DATASHEET_MODEL = "PJ-3106M (YBC01)"
DATASHEET_REVISION = "A"
DATASHEET_DATE = "2019-09-10"  # PDF creation date; the drawing itself is undated
DATASHEET_SHA256 = "88db1b26c288bbaa0537e7a184d20efc260de7c7e152d95f0d4d86067e96ea4f"
LCSC_PART = "C7428681"  # datasheet + photos: https://www.lcsc.com/product-detail/C7428681.html

# --- Housing ---------------------------------------------------------------
HOUSING_LENGTH = 12.00  # datasheet (side view, 12 +/-0.3)
HOUSING_WIDTH = 6.40  # datasheet (end view, 6.4)
HOUSING_HEIGHT = 4.00  # datasheet (front view, 4, *j); also the flat top of the nose

# --- Plug axis / nose ------------------------------------------------------
NOSE_PROJECTION = 1.00  # datasheet (side view, 1): nose in front of the housing
OVERALL_LENGTH = HOUSING_LENGTH + NOSE_PROJECTION  # 13.00
AXIS_HEIGHT = 1.85  # datasheet (front view, 1.85): plug axis above seating plane
# Lateral offset of the axis from the housing centreline, toward +X.
AXIS_X = 0.00  # estimate: not dimensioned; end view shows the axis on the centreline
NOSE_DIAMETER = 5.00  # estimate (front view outer circle, 5.05)
NOSE_INTO_HOUSING = 1.10  # datasheet (PCB layout, 1.1: board cutout behind the edge)
NOSE_DIP = 0.50  # estimate (front view 0.53, side view 0.48): flat underside below Z=0
NOSE_BELOW_BOARD_WIDTH = 3.00  # datasheet (end view, 3): nose width below the board
NOSE_FRONT_FILLET = 0.15  # estimate, cosmetic
BORE_DIAMETER = 3.60  # datasheet (front view, 3.6 +/-0.05, *i)
BORE_DEPTH = 11.00  # estimate, measured from the nose tip (blind)
# Nose face: an inner annulus is recessed so the outer rim reads as a raised
# ring without lengthening the part (photos, front view rings).
NOSE_RECESS_OUTER_DIAMETER = 4.00  # estimate (front view inner ring, 4.05)
NOSE_RECESS_DEPTH = 0.20  # estimate (photo)
BORE_CHAMFER = 0.20  # estimate (photo), 45 deg at the bore entry

# --- Front flange (first section of the housing) ---------------------------
FLANGE_THICKNESS = 0.60  # estimate (top view 0.63, right view 0.60)
# Trapezoid notch in the top of the flange and the nose rim, centred on AXIS_X.
FLANGE_NOTCH_TOP_WIDTH = 2.70  # estimate (front view)
FLANGE_NOTCH_BOTTOM_WIDTH = 2.00  # estimate (front view)
FLANGE_NOTCH_DEPTH = 0.70  # estimate (front view), from the top

# --- Gold front shell ------------------------------------------------------
# Covers top and both sides from FLANGE_THICKNESS to SHELL_REAR_FROM_FRONT
# behind the front face.
SHELL_REAR_FROM_FRONT = 3.50  # estimate (side view 3.6, right view 3.5, top view 3.45)
SHELL_THICKNESS = 0.15  # estimate; sits in a pocket so the envelope is unchanged
SHELL_SIDE_BOTTOM = 0.10  # estimate (photos): side walls reach almost to the board
SHELL_V_REAR_WIDTH = 2.40  # estimate (photo)
SHELL_V_APEX_GAP = 0.40  # estimate (photo): V apex distance from the shell's front edge
SHELL_WINDOW_LENGTH = 1.60  # estimate (right view), along Y
SHELL_WINDOW_HEIGHT = 1.30  # estimate (right view), Z
SHELL_WINDOW_Z = 2.10  # estimate (right view), window centre height
SHELL_FUSE_OVERLAP = 0.005  # internal: shell overlap into the pocket, fused STL path only

# --- Rear locating peg -----------------------------------------------------
PEG_FROM_FRONT = 10.70  # datasheet (side view 10.7, *a; PCB layout 10.7)
PEG_DIAMETER = 1.15  # datasheet (side view, 1.2 +0/-0.10): centre of the band
PEG_LENGTH = 0.50  # datasheet (right view, 0.5), below the seating plane

# --- Leads -----------------------------------------------------------------
# Lead centre distance from the housing front face, along the plug axis
# (datasheet: component top view & PCB layout).
PIN_FROM_FRONT = {
    1: 2.75,
    2: 9.40,
    3: 5.50,
    4: 2.75,
    5: 11.50,
    6: 10.50,
}
PIN_SIDE = {1: -1, 3: -1, 6: -1, 2: +1, 4: +1, 5: +1}  # sign of X
LEAD_TIP_SPAN = 8.30  # datasheet (end view, 8.3 +/-0.30, *b)
LEAD_WIDTH = 1.00  # datasheet (top view, 6-1), along the plug axis
LEAD_THICKNESS = 0.20  # datasheet (end view, 0.2thk)
LEAD_TAB_HEIGHT = 1.50  # estimate, vertical tab up the housing side
LEAD_OVERLAP = 0.05  # internal: overlap into the housing, fused STL path only
LEAD_FORK_DIAMETER = 0.50  # estimate (top view / photo)

# --- Footprint reference ---------------------------------------------------
PAD_ALONG_AXIS = 1.50  # datasheet (PCB layout, 6-1.5*2.6)
PAD_ACROSS = 2.60  # datasheet (PCB layout, 6-1.5*2.6)
PAD_OUTER_SPAN = 8.80  # datasheet (PCB layout, 8.8): outer pad edge to outer pad edge
PAD_CENTRE_X = PAD_OUTER_SPAN / 2 - PAD_ACROSS / 2  # 3.10
PCB_HOLE_DIAMETER = 1.60  # datasheet (PCB layout, 1.6): NPTH for the peg
NOSE_CUTOUT_WIDTH = 3.20  # datasheet (PCB layout, 3.2): board-edge cutout for the nose
# Pads run from 2.75 - 0.75 = 2.00 to 11.50 + 0.75 = 12.25 behind the front face.
PAD_CENTROID_FROM_FRONT = (
    min(PIN_FROM_FRONT.values()) - PAD_ALONG_AXIS / 2
    + max(PIN_FROM_FRONT.values()) + PAD_ALONG_AXIS / 2
) / 2  # 7.125
# Y of the housing front face in model space. Change this to move the origin.
FRONT_Y = PAD_CENTROID_FROM_FRONT

# --- Appearance ------------------------------------------------------------
HOUSING_COLOR = (0.06, 0.06, 0.07)  # matte near-black PA9T (LCSC C7428681 photos)
LEAD_COLOR = (0.90, 0.72, 0.35)  # Au-plated leads (photos)
SHELL_COLOR = LEAD_COLOR  # gold front shell (photos)
