"""Build CLI: writes models/PJ-3106M.step and models/PJ-3106M.stl.

With --render, also writes the README image docs/PJ-3106M_iso.png.
"""

import argparse
from pathlib import Path

import cadquery as cq

from pj3106m_model.model import build_assembly, build_fused

PROJECT_ROOT = Path(__file__).resolve().parents[2]
NAME = "PJ-3106M"
STL_TOLERANCE = 0.01  # mm, linear deflection
STL_ANGULAR_TOLERANCE = 0.1  # rad

PREVIEW_VIEWS = {
    "front": (0, 1, 0),  # looking into the plug opening
    "top": (0, 0, 1),
    "side": (1, 0, 0),
    "iso": (1, 1, 1),
}


def export(out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    step_path = out_dir / f"{NAME}.step"
    stl_path = out_dir / f"{NAME}.stl"
    build_assembly().export(str(step_path))
    cq.exporters.export(
        build_fused(),
        str(stl_path),
        tolerance=STL_TOLERANCE,
        angularTolerance=STL_ANGULAR_TOLERANCE,
    )
    return step_path, stl_path


def export_previews(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    fused = build_fused()
    paths = []
    for view, direction in PREVIEW_VIEWS.items():
        path = out_dir / f"{NAME}_{view}.svg"
        cq.exporters.export(
            fused,
            str(path),
            opt={
                "projectionDir": direction,
                "showHidden": False,
                "width": 600,
                "height": 450,
            },
        )
        paths.append(path)
    return paths


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", type=Path, default=PROJECT_ROOT / "models", help="output directory"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="also write SVG projections to build/",
    )
    parser.add_argument(
        "--render",
        type=Path,
        nargs="?",
        const=PROJECT_ROOT / "docs",
        default=None,
        metavar="DIR",
        help="also write the coloured isometric PNG (default DIR: docs/)",
    )
    args = parser.parse_args(argv)
    for path in export(args.out):
        print(f"wrote {path}")
    if args.preview:
        for path in export_previews(PROJECT_ROOT / "build"):
            print(f"wrote {path}")
    if args.render is not None:
        # Lazy import: a plain build doesn't need matplotlib.
        from pj3106m_model.render import render_iso

        print(f"wrote {render_iso(args.render)}")


if __name__ == "__main__":
    main()
