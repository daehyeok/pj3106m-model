# dev-environment Specification

## Purpose

Makes the project reproducible on any machine with a uv-managed, lock-pinned Python
environment, one command to regenerate the model, and automated dimensional checks.

## Requirements

### Requirement: Reproducible uv environment
The project SHALL declare its Python version and dependencies in files committed to the
repository (`pyproject.toml`, `.python-version`, `uv.lock`) so that `uv sync` on a fresh
clone creates an identical working environment without manual package installation. The
virtual environment directory itself SHALL NOT be committed.

#### Scenario: Fresh clone on another machine
- **WHEN** a developer with only `uv` installed clones the repo and runs `uv sync`
- **THEN** uv installs the pinned Python version (if missing) and every locked dependency,
  and the build and tests run without further setup

#### Scenario: Lock stays authoritative
- **WHEN** `uv sync --locked` is run
- **THEN** it succeeds without changing `uv.lock`

### Requirement: Single build command
The project SHALL provide one documented command, run through `uv run`, that regenerates
all model outputs from source.

#### Scenario: Build
- **WHEN** a developer runs the documented build command from the project root
- **THEN** `models/PJ-3106M.step` and `models/PJ-3106M.stl` are written, and the command
  exits with status 0

### Requirement: Dimensional test suite
The project SHALL provide automated tests, run with `uv run pytest`, that check the
generated geometry against the datasheet dimensions and coordinate-frame rules in the
`jack-3d-model` capability.

#### Scenario: Tests catch a dimension regression
- **WHEN** a parameter is changed so that a datasheet dimension falls outside its tolerance
- **THEN** `uv run pytest` fails and names the dimension that is out of tolerance

### Requirement: Developer documentation
The project SHALL include a README covering: installing uv, setting up the environment,
the build and test commands (including the command that regenerates the README image),
the model's coordinate frame and footprint origin, and how to reference the outputs from
a KiCad footprint. The README SHALL show the coloured isometric image of the model.

#### Scenario: New contributor setup
- **WHEN** a new contributor follows the README from a fresh clone
- **THEN** they can regenerate the outputs and run the tests without consulting anything
  else

#### Scenario: Regenerate the README image
- **WHEN** a contributor changes the geometry and follows the README's build instructions
- **THEN** the README tells them the command that regenerates the isometric image, and
  that the image must be committed along with `models/`

### Requirement: Source documents stay outside git
Vendor datasheets and product photos SHALL NOT be committed to the repository or required
by the build or tests. Committed files SHALL refer to them by identity (vendor, model,
revision, SHA-256, distributor part number), not by a local file path. The `/local/`
directory SHALL stay gitignored.

#### Scenario: Fresh clone without source documents
- **WHEN** a developer clones the repository without any datasheet or photo files and runs
  `uv sync`, the build command and `uv run pytest`
- **THEN** all of them succeed

#### Scenario: No local paths in committed files
- **WHEN** the committed files outside `openspec/changes/archive/` are searched for
  `local/` paths to datasheets or photos
- **THEN** none are found

### Requirement: Optional datasheet path parameter
The project SHALL provide a datasheet verification command. It SHALL take the datasheet's
location from either a `--datasheet PATH` option or the `PJ3106M_DATASHEET` environment
variable; if both are given, the option wins. It SHALL report whether the file matches the
recorded SHA-256 of the "PJ-3106M (YBC01)" rev A drawing that the model is built from. The
path SHALL NOT be written to any committed file.

#### Scenario: Matching datasheet
- **WHEN** the command is run with a path to the PJ-3106M rev A PDF (SHA-256
  `88db1b26c288bbaa0537e7a184d20efc260de7c7e152d95f0d4d86067e96ea4f`)
- **THEN** it reports a match and exits with status 0

#### Scenario: Wrong or missing file
- **WHEN** the command is run with a path to a different file (for example the older
  PJ-31060 rev A2 scan), a path that doesn't exist, or with neither the option nor the
  environment variable set
- **THEN** it prints what is wrong (checksum mismatch with both hashes, missing file, or
  no path given) and exits with a non-zero status

### Requirement: Dimension provenance in the README
The README SHALL have a provenance section that names:

- the source drawing
- how the estimated values were measured: the drawing resolution and the dimension used to
  calibrate the scale
- what the product photos were used for

The README SHALL also have a "Dimensions" table with the columns Feature, mm and Source.
It SHALL list every modelled dimension that sets visible geometry. Source SHALL be
`datasheet` for values dimensioned on the drawing and `estimate` for values measured off
the drawing or judged from the photos. Every value in the table SHALL equal the
corresponding named parameter in the model's dimension source, whose comment SHALL carry
the same datasheet/estimate classification.

#### Scenario: Reader checks where a number comes from
- **WHEN** a reader looks up a feature (for example the plug axis height or the shell side
  wall bottom) in the README "Dimensions" table
- **THEN** the table gives its value in mm and says whether it is from the datasheet or
  an estimate

#### Scenario: Table matches the parameters
- **WHEN** the test suite runs
- **THEN** it fails if a value listed in the README table differs from the parameter it
  documents
