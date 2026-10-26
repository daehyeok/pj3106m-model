"""Coloured isometric PNG render of the PJ-3106M model, drawn with matplotlib.

Each part (housing, front shell, six leads) is tessellated separately and filled
with its STEP colour from params.py, with simple flat shading. All triangles
are projected orthographically and drawn far-to-near (painter's algorithm)
as one PolyCollection, so the parts occlude each other correctly.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.collections import PolyCollection  # noqa: E402
from PIL import Image  # noqa: E402  (matplotlib dependency)

from pj3106m_model import params as p  # noqa: E402
from pj3106m_model.model import build_housing, build_leads, build_shell  # noqa: E402

IMAGE_NAME = "PJ-3106M_iso.png"

# True isometric view from +X, +Y, +Z: plug opening, shell top and pins 2/4/6.
VIEW_ELEV = 35.264  # deg
VIEW_AZIM = 45.0  # deg

FIGSIZE = (8, 6)  # inches
DPI = 150  # -> 1200 x 900 px
BACKGROUND = (1.0, 1.0, 1.0)
FILL = 0.85  # fraction of the image the model spans (tighter axis)

TESS_TOLERANCE = 0.02  # mm, linear deflection
TESS_ANGULAR_TOLERANCE = 0.2  # rad
MAX_EDGE = 0.12  # mm; subdivide so painter's-algorithm depth sorting holds
BACKFACE_EPS = 1e-6  # drop triangles facing away from the camera

# Light from slightly above and left of the camera (model coordinates).
LIGHT_DIR = (0.35, 1.0, 1.25)
AMBIENT = 0.45
DIFFUSE = 0.55
HIGHLIGHT = 0.22  # additive grey lift so the black housing faces stay readable
HIGHLIGHT_POWER = 3.0
# Draw at SUPERSAMPLE x size without anti-aliasing (no seams between
# triangles), then downsample for smooth silhouettes.
SUPERSAMPLE = 3


def _subdivide(tris: np.ndarray, max_edge: float) -> np.ndarray:
    """Split triangles at the midpoint of their longest edge until every edge is
    at most `max_edge`. The renderer sorts polygons by mean depth (painter's
    algorithm), which only works when the triangles are small and similar."""
    done = []
    while len(tris):
        edges = np.stack(
            [
                np.linalg.norm(tris[:, 1] - tris[:, 0], axis=1),
                np.linalg.norm(tris[:, 2] - tris[:, 1], axis=1),
                np.linalg.norm(tris[:, 0] - tris[:, 2], axis=1),
            ],
            axis=1,
        )
        small = edges.max(axis=1) <= max_edge
        done.append(tris[small])
        big = tris[~small]
        # Rotate vertices so the longest edge is (v0, v1), then split it.
        k = edges[~small].argmax(axis=1)
        idx = (np.arange(3)[None, :] + k[:, None]) % 3
        big = np.take_along_axis(big, idx[:, :, None], axis=1)
        mid = (big[:, 0] + big[:, 1]) / 2
        tris = np.concatenate(
            [
                np.stack([big[:, 0], mid, big[:, 2]], axis=1),
                np.stack([mid, big[:, 1], big[:, 2]], axis=1),
            ]
        )
    return np.concatenate(done)


def _view_vector() -> np.ndarray:
    """Unit vector from the model toward the camera."""
    elev, azim = np.radians(VIEW_ELEV), np.radians(VIEW_AZIM)
    return np.array(
        [np.cos(elev) * np.cos(azim), np.cos(elev) * np.sin(azim), np.sin(elev)]
    )


def _normals(tris: np.ndarray) -> np.ndarray:
    normals = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    return normals / np.where(lengths == 0, 1, lengths)


def _triangles(shape) -> np.ndarray:
    """Tessellate a CadQuery shape into an (N, 3, 3) array of camera-facing,
    subdivided triangles (outward winding, as CadQuery's tessellate gives)."""
    vertices, faces = shape.tessellate(TESS_TOLERANCE, TESS_ANGULAR_TOLERANCE)
    verts = np.array([v.toTuple() for v in vertices], dtype=float)
    tris = verts[np.array(faces, dtype=int)]
    tris = tris[_normals(tris) @ _view_vector() > BACKFACE_EPS]  # back-face cull
    return _subdivide(tris, MAX_EDGE)


def _shade(tris: np.ndarray, base_rgb) -> np.ndarray:
    """Per-triangle RGB: Lambert shading plus an additive highlight."""
    normals = _normals(tris)
    light = np.asarray(LIGHT_DIR, dtype=float)
    light = light / np.linalg.norm(light)
    # abs(): a reversed winding must not make a visible face black.
    lambert = np.abs(normals @ light)[:, None]
    base = np.asarray(base_rgb, dtype=float)[None, :]
    rgb = base * (AMBIENT + DIFFUSE * lambert) + HIGHLIGHT * lambert**HIGHLIGHT_POWER
    return np.clip(rgb, 0.0, 1.0)


def _parts() -> list[tuple[object, tuple[float, float, float]]]:
    parts = [
        (build_housing(), p.HOUSING_COLOR),
        (build_shell(), p.SHELL_COLOR),
    ]
    parts += [(lead, p.LEAD_COLOR) for lead in build_leads().values()]
    return parts


def render_iso(out_dir: Path) -> Path:
    """Render the coloured isometric view to `out_dir / IMAGE_NAME`."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / IMAGE_NAME

    all_tris, all_colors = [], []
    for shape, color in _parts():
        tris = _triangles(shape)
        all_tris.append(tris)
        all_colors.append(_shade(tris, color[:3]))
    tris = np.concatenate(all_tris)
    colors = np.concatenate(all_colors)

    # Orthographic projection onto the camera plane, then painter's algorithm:
    # draw triangles far-to-near by centroid depth.
    view = _view_vector()
    right = np.cross((0.0, 0.0, 1.0), view)
    right /= np.linalg.norm(right)
    up = np.cross(view, right)
    xy = np.stack([tris @ right, tris @ up], axis=-1)  # (N, 3, 2)
    order = np.argsort((tris @ view).mean(axis=1), kind="stable")
    xy, colors = xy[order], colors[order]

    fig = plt.figure(figsize=FIGSIZE, dpi=DPI * SUPERSAMPLE, facecolor=BACKGROUND)
    try:
        ax = fig.add_axes((0, 0, 1, 1), facecolor=BACKGROUND)
        ax.add_collection(
            PolyCollection(
                xy, facecolors=colors, edgecolors="none", antialiaseds=False
            )
        )
        # Equal scale, model centred, filling FILL of the tighter image side.
        pts = xy.reshape(-1, 2)
        lo, hi = pts.min(axis=0), pts.max(axis=0)
        center = (lo + hi) / 2
        aspect = FIGSIZE[0] / FIGSIZE[1]
        half_h = max((hi - lo)[1], (hi - lo)[0] / aspect) / 2 / FILL
        ax.set_xlim(center[0] - half_h * aspect, center[0] + half_h * aspect)
        ax.set_ylim(center[1] - half_h, center[1] + half_h)
        ax.set_aspect("equal")
        ax.set_axis_off()
        fig.canvas.draw()
        big = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())).convert("RGB")
    finally:
        plt.close(fig)
    size = (round(FIGSIZE[0] * DPI), round(FIGSIZE[1] * DPI))
    # Pillow writes no timestamp/software metadata, so the bytes are stable.
    big.resize(size, Image.Resampling.LANCZOS).save(path, optimize=True)
    return path
