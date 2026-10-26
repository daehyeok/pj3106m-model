# jack-3d-model Specification

## Purpose

Provides a simplified, datasheet-accurate 3D model of the PJ-3106M 3.5 mm 4-pole SMD phone
jack, exported as STEP and STL for the KiCad footprint 3D viewer and mechanical fit checks.

## Requirements

### Requirement: Datasheet-derived outline dimensions
The model SHALL match the outline dimensions in the HAOYU/HOOYA PJ-31060 datasheet,
revision A2 (2021-11-04; PDF SHA-256
`939615b14e90b455765f1b6e26bbef588cdcfba269b0a047174ec80916c501fb`; LCSC part C2939583),
to within the datasheet's general tolerance (±0.1 mm up to 5 mm, ±0.2 mm above 5 mm):
housing length 12.00 mm, overall length including the front nose 14.00 mm, housing width
6.40 mm, housing height 4.00 mm above the seating plane, plug bore Ø3.60 mm, and plug axis
1.90 mm above the seating plane.

#### Scenario: Overall bounding box
- **WHEN** the exported model is measured
- **THEN** its extent along the plug axis is 14.00 ± 0.2 mm, its extent across the leads is
  8.30 ± 0.25 mm, the housing's flat top is 4.00 ± 0.1 mm above the seating plane, and the
  highest point (top of the nose) is 4.40 ± 0.1 mm above the seating plane

#### Scenario: Plug bore
- **WHEN** the front face of the nose is inspected
- **THEN** it has an open circular bore of Ø3.60 ± 0.05 mm centred on the plug axis, 1.90 ±
  0.1 mm above the seating plane

#### Scenario: Datasheet identified without a local file
- **WHEN** someone reads the repository in a fresh clone that has no datasheet file
- **THEN** they can identify and obtain the exact source datasheet from the recorded
  vendor, model, revision, SHA-256 and LCSC part number

### Requirement: Simplified but recognisable features
The model SHALL include the housing body, the round front nose (about Ø5.0 mm, projecting
2.00 mm in front of the housing and dipping about 0.60 mm below the seating plane), the
plug bore, the rear locating peg on the plug axis 10.55 mm behind the housing front face,
and six SMD leads. It SHALL also include these visible details from the product photos:
a square front flange behind the nose, a metal shell over the top and both sides of the
front housing section (with a V-shaped tongue on top and a rectangular window on each
side), a raised ring on the nose face, a chamfer at the plug bore entry, and a forked
(notched) tip on every lead. These details SHALL stay inside the existing outline
envelope. It SHALL NOT model internal contacts, springs, top windows, text markings, or
underside channels.

#### Scenario: Nose below the board
- **WHEN** the model is viewed from the front
- **THEN** the nose's lowest point is 0.60 ± 0.1 mm below the seating plane, and the part
  of the nose below the seating plane is no wider than 3.30 mm at the seating plane

#### Scenario: Locating peg
- **WHEN** the model is viewed from below
- **THEN** a single cylindrical peg (about Ø1.15 mm) projects below the seating plane on
  the plug axis, 10.55 ± 0.1 mm behind the housing front face

#### Scenario: Front shell
- **WHEN** the model is inspected 0.7–3.3 mm behind the housing front face
- **THEN** a separate shell solid covers the top and both sides of the housing there,
  with a V-shaped opening in its top and a rectangular window in each side, and its outer
  faces are no more than 3.20 mm from the centreline and 4.00 mm above the seating plane

#### Scenario: Front flange and nose detail
- **WHEN** the front of the model is inspected
- **THEN** a flange about 0.7 mm thick spans the housing cross-section directly behind the
  nose with a notch at its top, the nose face has a raised ring, and the bore entry is
  chamfered while the bore stays Ø3.60 ± 0.05 mm behind the chamfer

#### Scenario: Forked lead tips
- **WHEN** a lead is viewed from above
- **THEN** its outer end has a semicircular notch, and the lead still lies entirely within
  its 2.00 × 1.50 mm pad

#### Scenario: Envelope unchanged
- **WHEN** the detailed model is measured
- **THEN** its bounding box and outline dimensions match the "Datasheet-derived outline
  dimensions" requirement exactly as before the details were added

### Requirement: Lead positions match the datasheet PCB layout
The model SHALL have six leads whose centres, measured along the plug axis from the housing
front face, are 2.85, 9.40 and 11.50 mm for pins 2, 4 and 6 (one side) and 2.80, 5.45 and
10.50 mm for pins 1, 3 and 5 (the opposite side). Lead tips span 8.30 ± 0.25 mm across the
body, and lead bottoms lie on the seating plane.

#### Scenario: Leads land on the pads
- **WHEN** the model is overlaid on a footprint with six 2.00 × 1.50 mm pads at the
  datasheet PCB-layout positions
- **THEN** every lead's footprint on the seating plane lies inside its pad

#### Scenario: Pin side orientation
- **WHEN** the model is viewed from the top with the plug opening pointing toward +Y
- **THEN** pins 2, 4 and 6 are on the +X side and pins 1, 3 and 5 are on the −X side,
  matching the datasheet's PCB layout (top view)

### Requirement: KiCad-aligned coordinate frame
The exported model SHALL use millimetres, with Z = 0 at the seating plane (PCB top
surface) and +Z pointing away from the board. X/Y SHALL be placed relative to a documented
footprint origin so the model needs zero offset, zero rotation and unit scale when it is
attached to a footprint built on the same origin.

#### Scenario: Load in KiCad without adjustment
- **WHEN** the STEP file is attached to a footprint with offset (0, 0, 0), rotation
  (0, 0, 0) and scale 1
- **THEN** the leads sit on the matching pads and the housing rests on the board surface

### Requirement: STEP and STL outputs
Running the build SHALL write `models/PJ-3106M.step` and `models/PJ-3106M.stl`. The STEP
SHALL keep the housing, the front shell, and each lead as separately coloured solids:
matte near-black housing (about RGB 0.06, 0.06, 0.07) and gold shell and leads (about RGB
0.90, 0.72, 0.35), matched to the product photos. The STL SHALL be a single closed
(watertight) mesh in millimetres. Both files SHALL be committed so consumers don't have
to run the build.

#### Scenario: Regenerate outputs
- **WHEN** a developer runs the documented build command
- **THEN** both files are regenerated with no errors, and the STL is watertight and not
  empty

#### Scenario: STEP colours
- **WHEN** the STEP file is opened in KiCad's 3D viewer or a STEP viewer
- **THEN** the housing appears black and the front shell and leads appear gold

#### Scenario: STEP solid count
- **WHEN** the STEP file is re-imported
- **THEN** it contains exactly 8 solids: 1 housing, 1 front shell, and 6 leads

### Requirement: Single source of dimensions
Every dimension used by the model SHALL be a named parameter whose comment cites the
datasheet view it comes from, or says it is an estimate when the datasheet doesn't give it.

#### Scenario: Change a dimension
- **WHEN** a developer changes one named parameter (e.g. the housing length) and rebuilds
- **THEN** the exported geometry changes to match, with no other code edits needed
