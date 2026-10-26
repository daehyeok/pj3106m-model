## Purpose

Provides a coloured isometric image of the PJ-3106M model, generated from the same geometry
as the STEP/STL outputs and committed to the repository, so readers can see the part
without opening a CAD tool.

## ADDED Requirements

### Requirement: Coloured isometric render
The project SHALL generate a raster PNG image of the full model (housing, front shell and
all six leads) viewed from an isometric direction from the front, above and the +X side,
so that the plug opening, the top of the gold shell and the +X leads (pins 2, 4, 6) are
visible. Each part SHALL be filled with the colour it has in the STEP output: matte
near-black housing (about RGB 0.06, 0.06, 0.07) and gold shell and leads (about RGB 0.90,
0.72, 0.35). Faces SHALL be shaded by orientation so the part reads as a solid, not a flat
silhouette. The model SHALL be drawn with equal scale on all three axes (no distortion),
on a plain light background with no axes, ticks or grid.

#### Scenario: Colours are present
- **WHEN** the generated image is inspected
- **THEN** it contains a large region of near-black pixels (housing) and a clearly visible
  region of gold-hued pixels (shell and leads), and the background is a uniform light
  colour

#### Scenario: Whole part in frame
- **WHEN** the generated image is inspected
- **THEN** the model isn't cropped at any image edge and fills most of the frame

### Requirement: Render command
Running the documented build command with a render option SHALL write the image to
`docs/PJ-3106M_iso.png` (or to a caller-given output directory) and exit with status 0.
The image SHALL be at least 800 pixels wide. Running the build without the render option
SHALL still write only the STEP and STL outputs, as before.

#### Scenario: Regenerate the image
- **WHEN** a developer runs the documented render command from the project root
- **THEN** `docs/PJ-3106M_iso.png` is written as a valid PNG of at least 800 pixels wide
  and the command exits with status 0

#### Scenario: Default build unchanged
- **WHEN** a developer runs the build command without the render option
- **THEN** only `models/PJ-3106M.step` and `models/PJ-3106M.stl` are written and no image
  is created or modified

### Requirement: Image committed and shown in the README
The generated image SHALL be committed at `docs/PJ-3106M_iso.png` and embedded in
`README.md` near the top, before the "Source documents" section, with alt text that names
the part, using a relative path so it renders on the repository host and in local
Markdown viewers.

#### Scenario: README shows the model
- **WHEN** someone views `README.md` on the repository host in a fresh clone
- **THEN** the coloured isometric image of the jack is displayed near the top of the page

#### Scenario: Image link resolves
- **WHEN** the image path referenced in `README.md` is resolved relative to the README
- **THEN** it points to an existing, committed PNG file
