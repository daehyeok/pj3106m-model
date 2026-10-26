"""Coloured isometric README image: render checks, CLI flag, README embed."""

import re
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from pj3106m_model.build import main
from pj3106m_model.render import BACKGROUND, IMAGE_NAME, render_iso

PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_IMAGE = PROJECT_ROOT / "docs" / IMAGE_NAME
MIN_WIDTH = 800
BORDER = 2  # px that must be pure background (model not cropped)


@pytest.fixture(scope="module")
def image(tmp_path_factory) -> np.ndarray:
    path = render_iso(tmp_path_factory.mktemp("render"))
    with Image.open(path) as im:
        assert im.format == "PNG"
        return np.asarray(im.convert("RGB"), dtype=float) / 255.0


@pytest.fixture(scope="module")
def foreground(image) -> np.ndarray:
    return np.abs(image - np.asarray(BACKGROUND)).max(axis=2) > 0.02


def test_png_size(image):
    height, width, _ = image.shape
    assert width >= MIN_WIDTH, f"image is {width} px wide, need >= {MIN_WIDTH}"
    assert height > 0


def test_not_cropped(foreground):
    border = np.ones_like(foreground)
    border[BORDER:-BORDER, BORDER:-BORDER] = False
    assert not foreground[border].any(), "model touches the image edge (cropped)"


def test_model_fills_frame(foreground):
    rows = np.flatnonzero(foreground.any(axis=1))
    cols = np.flatnonzero(foreground.any(axis=0))
    h_frac = (rows[-1] - rows[0] + 1) / foreground.shape[0]
    w_frac = (cols[-1] - cols[0] + 1) / foreground.shape[1]
    assert max(h_frac, w_frac) >= 0.5, f"model spans only {h_frac:.0%} x {w_frac:.0%}"


def test_dark_housing_present(image, foreground):
    spread = image.max(axis=2) - image.min(axis=2)
    dark = (image.max(axis=2) < 0.35) & (spread < 0.08)
    frac = dark.sum() / foreground.sum()
    assert frac > 0.4, f"near-black housing covers only {frac:.0%} of the model"


def test_gold_present(image):
    r, g, b = image[..., 0], image[..., 1], image[..., 2]
    gold = (r > g) & (g > b) & (r - b > 0.25)
    frac = gold.mean()
    assert frac > 0.01, f"gold shell/leads cover only {frac:.2%} of the image"


def test_default_build_writes_no_image(tmp_path):
    main(["--out", str(tmp_path)])
    assert sorted(p.name for p in tmp_path.iterdir()) == [
        "PJ-3106M.step",
        "PJ-3106M.stl",
    ]


def test_render_flag_writes_image(tmp_path):
    out, img_dir = tmp_path / "models", tmp_path / "img"
    main(["--out", str(out), "--render", str(img_dir)])
    assert (img_dir / IMAGE_NAME).is_file()
    assert not (out / IMAGE_NAME).exists()


def test_readme_embeds_committed_image():
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    links = re.findall(r"!\[[^\]]+\]\(([^)\s]+)\)", readme)
    assert f"docs/{IMAGE_NAME}" in links, "README.md doesn't embed the iso image"
    assert COMMITTED_IMAGE.is_file(), f"{COMMITTED_IMAGE} is missing"
