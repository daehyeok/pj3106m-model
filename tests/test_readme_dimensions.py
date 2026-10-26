"""The README "Dimensions" table must match pj3106m_model.params.

Each row maps to one or more parameters (several numbers in one cell are
separated by "/" or "x"/"×") and to the source tag the README must show.
"""

import re
from pathlib import Path

import pytest

from pj3106m_model import params as p

README = Path(__file__).resolve().parents[1] / "README.md"

# Feature -> (values from params, expected Source column)
ROWS = {
    "Housing length": ([p.HOUSING_LENGTH], "datasheet"),
    "Housing width": ([p.HOUSING_WIDTH], "datasheet"),
    "Housing height (= overall height, flat top)": ([p.HOUSING_HEIGHT], "datasheet"),
    "Nose projection in front of the housing": ([p.NOSE_PROJECTION], "datasheet"),
    "Overall length": ([p.OVERALL_LENGTH], "datasheet"),
    "Plug axis height": ([p.AXIS_HEIGHT], "datasheet"),
    "Plug axis lateral offset": ([p.AXIS_X], "estimate"),
    "Plug bore diameter": ([p.BORE_DIAMETER], "datasheet"),
    "Nose width below the board": ([p.NOSE_BELOW_BOARD_WIDTH], "datasheet"),
    "Nose extent behind the front face (board cutout depth)": (
        [p.NOSE_INTO_HOUSING], "datasheet"),
    "Peg distance behind the front face": ([p.PEG_FROM_FRONT], "datasheet"),
    "Peg diameter (Ø1.2 +0/−0.1)": ([p.PEG_DIAMETER], "datasheet"),
    "Peg length below the board": ([p.PEG_LENGTH], "datasheet"),
    "Lead tip span": ([p.LEAD_TIP_SPAN], "datasheet"),
    "Lead width": ([p.LEAD_WIDTH], "datasheet"),
    "Lead thickness": ([p.LEAD_THICKNESS], "datasheet"),
    "Pins 1 / 4 behind the front face": ([p.PIN_FROM_FRONT[1]], "datasheet"),
    "Pin 3 behind the front face": ([p.PIN_FROM_FRONT[3]], "datasheet"),
    "Pin 2 behind the front face": ([p.PIN_FROM_FRONT[2]], "datasheet"),
    "Pin 6 behind the front face": ([p.PIN_FROM_FRONT[6]], "datasheet"),
    "Pin 5 behind the front face": ([p.PIN_FROM_FRONT[5]], "datasheet"),
    "Pad along the plug axis × across": ([p.PAD_ALONG_AXIS, p.PAD_ACROSS], "datasheet"),
    "Pad outer span": ([p.PAD_OUTER_SPAN], "datasheet"),
    "Peg hole diameter (PCB)": ([p.PCB_HOLE_DIAMETER], "datasheet"),
    "Nose board cutout width": ([p.NOSE_CUTOUT_WIDTH], "datasheet"),
    "Nose diameter": ([p.NOSE_DIAMETER], "estimate"),
    "Nose dip below the board": ([p.NOSE_DIP], "estimate"),
    "Nose-face recess diameter / depth": (
        [p.NOSE_RECESS_OUTER_DIAMETER, p.NOSE_RECESS_DEPTH], "estimate"),
    "Bore entry chamfer": ([p.BORE_CHAMFER], "estimate"),
    "Bore depth from the nose tip": ([p.BORE_DEPTH], "estimate"),
    "Flange thickness": ([p.FLANGE_THICKNESS], "estimate"),
    "Rim notch width top / bottom / depth": (
        [p.FLANGE_NOTCH_TOP_WIDTH, p.FLANGE_NOTCH_BOTTOM_WIDTH, p.FLANGE_NOTCH_DEPTH],
        "estimate"),
    "Shell rear edge behind the front face": ([p.SHELL_REAR_FROM_FRONT], "estimate"),
    "Shell sheet thickness": ([p.SHELL_THICKNESS], "estimate"),
    "Shell side wall bottom above the board": ([p.SHELL_SIDE_BOTTOM], "estimate"),
    "Shell V tongue rear width / apex gap": (
        [p.SHELL_V_REAR_WIDTH, p.SHELL_V_APEX_GAP], "estimate"),
    "Shell window length × height / centre height": (
        [p.SHELL_WINDOW_LENGTH, p.SHELL_WINDOW_HEIGHT, p.SHELL_WINDOW_Z], "estimate"),
    "Lead side tab height": ([p.LEAD_TAB_HEIGHT], "estimate"),
    "Lead fork diameter": ([p.LEAD_FORK_DIAMETER], "estimate"),
}


def readme_table() -> dict[str, tuple[str, str]]:
    text = README.read_text(encoding="utf-8")
    section = text.split("### Dimensions", 1)[1].split("\n## ", 1)[0]
    rows = {}
    for line in section.splitlines():
        cells = [c.strip() for c in line.split("|")]
        if len(cells) != 3 or cells[0] in ("Feature", "") or cells[0].startswith(":"):
            continue
        rows[cells[0]] = (cells[1], cells[2])
    return rows


def test_table_rows_match_mapping():
    table = readme_table()
    assert set(table) == set(ROWS), (
        f"README-only rows: {sorted(set(table) - set(ROWS))}; "
        f"missing from README: {sorted(set(ROWS) - set(table))}"
    )


@pytest.mark.parametrize("feature", sorted(ROWS))
def test_value_and_source(feature):
    table = readme_table()
    assert feature in table, f"README Dimensions table has no row {feature!r}"
    cell, source = table[feature]
    expected_values, expected_source = ROWS[feature]
    numbers = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", cell)]
    assert len(numbers) == len(expected_values), f"{feature}: cell {cell!r}"
    for got, want in zip(numbers, expected_values):
        assert abs(got - want) < 1e-6, f"{feature}: README {got}, params {want}"
    assert source == expected_source, f"{feature}: source {source!r}, expected {expected_source!r}"
