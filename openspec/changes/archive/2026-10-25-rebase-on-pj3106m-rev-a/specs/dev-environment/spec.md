## MODIFIED Requirements

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

## ADDED Requirements

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
