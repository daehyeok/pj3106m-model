"""CadQuery geometry for the PJ-3106M jack. Dimensions come from params.py."""

import cadquery as cq

from pj3106m_model import params as p

_BIG = 50.0  # size of "everything" boxes used for cuts


def _y_from_front(distance: float) -> float:
    """Model-space Y of a point `distance` mm behind the housing front face."""
    return p.FRONT_Y - distance


def _box(x0, x1, y0, y1, z0, z1) -> cq.Workplane:
    """Axis-aligned box from min/max corners."""
    return cq.Workplane("XY").box(
        x1 - x0, y1 - y0, z1 - z0, centered=False
    ).translate((x0, y0, z0))


def _cylinder_along_y(diameter: float, y0: float, y1: float) -> cq.Workplane:
    """Cylinder on the plug axis from Y=y0 to Y=y1 (y1 > y0)."""
    return (
        cq.Workplane("XZ", origin=(p.AXIS_X, y0, p.AXIS_HEIGHT))
        .circle(diameter / 2)
        # The XZ workplane normal is -Y, so extrude a negative distance to go +Y.
        .extrude(-(y1 - y0))
    )


def _shell_zone() -> tuple[float, float]:
    """Y range (rear, front) covered by the gold front shell."""
    return _y_from_front(p.SHELL_REAR_FROM_FRONT), _y_from_front(p.FLANGE_THICKNESS)


def build_housing() -> cq.Solid:
    """Housing body + nose + peg, with bore, flange notch and shell pocket."""
    half_w = p.HOUSING_WIDTH / 2
    body = _box(
        -half_w, half_w,
        _y_from_front(p.HOUSING_LENGTH), p.FRONT_Y,
        0, p.HOUSING_HEIGHT,
    )

    nose_tip_y = p.FRONT_Y + p.NOSE_PROJECTION
    nose = _cylinder_along_y(
        p.NOSE_DIAMETER, _y_from_front(p.NOSE_INTO_HOUSING), nose_tip_y
    )
    nose = nose.faces(">Y").edges().fillet(p.NOSE_FRONT_FILLET)
    # Flat rim at the housing top, flat underside below the board, and the
    # below-board part trimmed to the datasheet end-view width (fits the 3.2
    # board cutout).
    half_below = p.NOSE_BELOW_BOARD_WIDTH / 2
    nose = (
        nose.cut(_box(-_BIG, _BIG, -_BIG, _BIG, p.HOUSING_HEIGHT, _BIG))
        .cut(_box(-_BIG, _BIG, -_BIG, _BIG, -_BIG, -p.NOSE_DIP))
        .cut(_box(p.AXIS_X + half_below, _BIG, -_BIG, _BIG, -_BIG, 0))
        .cut(_box(-_BIG, p.AXIS_X - half_below, -_BIG, _BIG, -_BIG, 0))
    )

    peg = (
        cq.Workplane("XY", origin=(p.AXIS_X, _y_from_front(p.PEG_FROM_FRONT), 0))
        .circle(p.PEG_DIAMETER / 2)
        .extrude(-p.PEG_LENGTH)
    )

    housing = body.union(nose).union(peg)

    # Plug bore, nose-face annulus recess (leaves a raised outer ring), and a
    # 45-degree chamfer where the bore meets the recess floor.
    bore = _cylinder_along_y(
        p.BORE_DIAMETER, nose_tip_y - p.BORE_DEPTH, nose_tip_y + 0.1
    )
    recess_floor_y = nose_tip_y - p.NOSE_RECESS_DEPTH
    recess = _cylinder_along_y(
        p.NOSE_RECESS_OUTER_DIAMETER, recess_floor_y, nose_tip_y + 0.1
    )
    chamfer = cq.Workplane("XY").add(
        cq.Solid.makeCone(
            p.BORE_DIAMETER / 2,
            p.BORE_DIAMETER / 2 + p.BORE_CHAMFER,
            p.BORE_CHAMFER,
            cq.Vector(p.AXIS_X, recess_floor_y - p.BORE_CHAMFER, p.AXIS_HEIGHT),
            cq.Vector(0, 1, 0),
        )
    )
    housing = housing.cut(bore).cut(recess).cut(chamfer)

    # Trapezoid notch in the top of the front flange and the flat nose rim
    # (datasheet front view), running from the flange rear through the nose tip.
    flange_rear_y = _y_from_front(p.FLANGE_THICKNESS)
    top_half = p.FLANGE_NOTCH_TOP_WIDTH / 2
    bottom_half = p.FLANGE_NOTCH_BOTTOM_WIDTH / 2
    notch_bottom_z = p.HOUSING_HEIGHT - p.FLANGE_NOTCH_DEPTH
    notch_len = nose_tip_y + 0.1 - flange_rear_y
    notch = (
        cq.Workplane("XZ", origin=(0, flange_rear_y, 0))
        .polyline(
            [
                (p.AXIS_X - bottom_half, notch_bottom_z),
                (p.AXIS_X + bottom_half, notch_bottom_z),
                (p.AXIS_X + top_half, p.HOUSING_HEIGHT + 0.1),
                (p.AXIS_X - top_half, p.HOUSING_HEIGHT + 0.1),
            ]
        )
        .close()
        # The XZ workplane normal is -Y, so extrude a negative distance to go +Y.
        .extrude(-notch_len)
    )
    housing = housing.cut(notch)

    # Pocket for the gold shell: top (also trims the nose above the shell)
    # and both sides above SHELL_SIDE_BOTTOM.
    y0, y1 = _shell_zone()
    t = p.SHELL_THICKNESS
    top_pocket = _box(-_BIG, _BIG, y0, y1, p.HOUSING_HEIGHT - t, _BIG)
    side_pocket_pos = _box(half_w - t, _BIG, y0, y1, p.SHELL_SIDE_BOTTOM, _BIG)
    side_pocket_neg = _box(-_BIG, -(half_w - t), y0, y1, p.SHELL_SIDE_BOTTOM, _BIG)
    housing = housing.cut(top_pocket).cut(side_pocket_pos).cut(side_pocket_neg)
    return housing.val()


def build_shell(overlap: float = 0.0) -> cq.Solid:
    """Gold U-profile shell over the front section, with V tongue and windows.

    `overlap` thickens the shell inward into the housing pocket (fused STL path
    only) so the boolean fuse doesn't depend on exactly coincident faces.
    """
    half_w = p.HOUSING_WIDTH / 2
    t = p.SHELL_THICKNESS
    inner_t = t + overlap
    top_z = p.HOUSING_HEIGHT
    y0, y1 = _shell_zone()

    top = _box(-half_w, half_w, y0, y1, top_z - inner_t, top_z)
    side_pos = _box(half_w - inner_t, half_w, y0, y1, p.SHELL_SIDE_BOTTOM, top_z - t)
    side_neg = _box(-half_w, -(half_w - inner_t), y0, y1, p.SHELL_SIDE_BOTTOM, top_z - t)
    shell = top.union(side_pos).union(side_neg)

    # V-shaped tongue: wide at the rear edge, apex toward the front.
    apex_y = y1 - p.SHELL_V_APEX_GAP
    v_cut = (
        cq.Workplane("XY", origin=(0, 0, top_z - t - 0.05))
        .polyline(
            [
                (p.AXIS_X - p.SHELL_V_REAR_WIDTH / 2, y0 - 0.01),
                (p.AXIS_X + p.SHELL_V_REAR_WIDTH / 2, y0 - 0.01),
                (p.AXIS_X, apex_y),
            ]
        )
        .close()
        .extrude(t + 0.1)
    )
    shell = shell.cut(v_cut)

    # Rectangular window in each side wall.
    wy = (y0 + y1) / 2
    for sign in (1, -1):
        window = _box(
            -_BIG, _BIG,
            wy - p.SHELL_WINDOW_LENGTH / 2, wy + p.SHELL_WINDOW_LENGTH / 2,
            p.SHELL_WINDOW_Z - p.SHELL_WINDOW_HEIGHT / 2,
            p.SHELL_WINDOW_Z + p.SHELL_WINDOW_HEIGHT / 2,
        )
        side = side_pos if sign > 0 else side_neg
        shell = shell.cut(window.intersect(side))
    return shell.val()


def build_leads(overlap: float = 0.0) -> dict[int, cq.Solid]:
    """Six SMD leads: a forked foot on the seating plane + a side tab.

    `overlap` extends each lead into the housing (fused STL path only); the
    STEP assembly uses 0 so the solids don't intersect.
    Leads under the gold shell get no side tab (it would hit the shell wall).
    """
    half_width = p.HOUSING_WIDTH / 2
    tip = p.LEAD_TIP_SPAN / 2
    shell_y0, shell_y1 = _shell_zone()
    leads = {}
    for pin, dist in sorted(p.PIN_FROM_FRONT.items()):
        side = p.PIN_SIDE[pin]
        y_c = _y_from_front(dist)
        x0 = half_width - overlap
        lead = _box(
            x0, tip,
            y_c - p.LEAD_WIDTH / 2, y_c + p.LEAD_WIDTH / 2,
            0, p.LEAD_THICKNESS,
        )
        under_shell = (y_c + p.LEAD_WIDTH / 2 > shell_y0) and (
            y_c - p.LEAD_WIDTH / 2 < shell_y1
        )
        if not under_shell:
            tab = _box(
                x0, half_width + p.LEAD_THICKNESS,
                y_c - p.LEAD_WIDTH / 2, y_c + p.LEAD_WIDTH / 2,
                0, p.LEAD_TAB_HEIGHT,
            )
            lead = lead.union(tab)
        fork = (
            cq.Workplane("XY", origin=(tip, y_c, -0.05))
            .circle(p.LEAD_FORK_DIAMETER / 2)
            .extrude(p.LEAD_THICKNESS + 0.1)
        )
        lead = lead.cut(fork)
        if side < 0:
            lead = lead.mirror("YZ")
        leads[pin] = lead.val()
    return leads


def build_assembly() -> cq.Assembly:
    """Coloured assembly for STEP export (black housing, gold shell + leads)."""
    assy = cq.Assembly(name="PJ-3106M")
    assy.add(build_housing(), name="housing", color=cq.Color(*p.HOUSING_COLOR))
    assy.add(build_shell(), name="shell", color=cq.Color(*p.SHELL_COLOR))
    for pin, lead in build_leads().items():
        assy.add(lead, name=f"pin{pin}", color=cq.Color(*p.LEAD_COLOR))
    return assy


def build_fused() -> cq.Solid:
    """Housing, shell and leads fused into one solid (for a watertight STL)."""
    shape = cq.Workplane("XY").add(build_housing())
    shape = shape.union(cq.Workplane("XY").add(build_shell(overlap=p.SHELL_FUSE_OVERLAP)))
    for lead in build_leads(overlap=p.LEAD_OVERLAP).values():
        shape = shape.union(cq.Workplane("XY").add(lead))
    solids = shape.solids().vals()
    if len(solids) != 1:
        raise RuntimeError(f"fused model has {len(solids)} solids, expected 1")
    return solids[0]
