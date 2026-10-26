## MODIFIED Requirements

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
