# jack-3d-model Specification

## Purpose

Provides a simplified, datasheet-accurate 3D model of the PJ-3106M 3.5 mm 4-pole SMD phone
jack, exported as STEP and STL for the KiCad footprint 3D viewer and mechanical fit checks.

## Requirements

### Requirement: Datasheet-derived outline dimensions
The model SHALL match the outline dimensions in the HAOYU/HOOYA "PJ-3106M (YBC01)" drawing,
revision A (vector PDF; SHA-256
`88db1b26c288bbaa0537e7a184d20efc260de7c7e152d95f0d4d86067e96ea4f`; datasheet and product photos
from LCSC part C7428681). It SHALL stay within the drawing's general tolerance (±0.1 mm up to 5 mm,
±0.2 mm above 5 mm) unless the drawing gives a specific tolerance. The dimensions are:

- housing length 12.0 ± 0.3 mm
- nose projection 1.0 mm in front of the housing, so the overall length is 13.0 mm
- housing width 6.4 mm
- height 4.0 mm above the seating plane, with nothing higher, nose included
- plug bore Ø3.6 ± 0.05 mm
- plug axis 1.85 mm above the seating plane, on the housing centreline
- lead tip span 8.3 ± 0.3 mm

#### Scenario: Overall bounding box
- **WHEN** the exported model is measured
- **THEN** its extent along the plug axis is 13.00 ± 0.2 mm, its extent across the leads is
  8.30 ± 0.3 mm, and its highest point is 4.00 ± 0.1 mm above the seating plane

#### Scenario: Flat top
- **WHEN** the model is sliced at 4.05 mm above the seating plane
- **THEN** no solid (housing, nose, shell or lead) is present at that height

#### Scenario: Plug bore
- **WHEN** the front face of the nose is inspected
- **THEN** it has an open circular bore of Ø3.60 ± 0.05 mm centred on the plug axis, which
  is 1.85 ± 0.1 mm above the seating plane and within 0.05 mm of the housing centreline

#### Scenario: Datasheet identified without a local file
- **WHEN** someone reads the repository in a fresh clone that has no datasheet file
- **THEN** they can identify and obtain the exact source drawing from the recorded vendor,
  model, revision, SHA-256 and LCSC part number

### Requirement: Simplified but recognisable features
The model SHALL include these features:

- the housing body
- the round front nose: about Ø5.0 mm, projecting 1.00 mm in front of the housing, with
  its top cut flat at the housing top (4.00 mm) and its underside cut flat about 0.50 mm
  below the seating plane
- the plug bore
- the rear locating peg: Ø1.2 +0/−0.1 mm (so Ø1.10–1.20), on the plug axis 10.7 mm behind the housing front face,
  projecting 0.5 mm below the seating plane
- six SMD leads

The part of the nose below the seating plane SHALL be no wider than 3.0 mm, so that it fits
the datasheet's 3.2 mm board cutout.

The model SHALL also include these visible details from the drawing and the product photos:

- a front flange behind the nose, with a notch at its top
- a gold metal shell over the top and both sides of the front housing section, with a
  V-shaped tongue on top and a window in each side; its side walls SHALL reach down to
  within 0.15 mm of the seating plane
- a raised ring on the nose face
- a chamfer at the plug bore entry
- a forked (notched) tip on every lead

These details SHALL stay inside the outline envelope. The model SHALL NOT include internal
contacts, springs, top windows, text markings, or underside channels.

#### Scenario: Nose below the board
- **WHEN** the model is viewed from the front
- **THEN** the nose's lowest point is 0.50 ± 0.1 mm below the seating plane, and the part
  of the nose below the seating plane is no wider than 3.05 mm

#### Scenario: Nose rim flush with the housing top
- **WHEN** the nose is inspected from the side
- **THEN** its top is a flat face at 4.00 ± 0.05 mm above the seating plane, flush with the
  housing top, and the nose does not rise above it anywhere

#### Scenario: Locating peg
- **WHEN** the model is viewed from below
- **THEN** a single cylindrical peg of Ø1.10–1.20 mm projects 0.50 ± 0.1 mm below the
  seating plane, on the plug axis, 10.70 ± 0.2 mm behind the housing front face

#### Scenario: Front shell
- **WHEN** the model is inspected 0.6–3.5 mm behind the housing front face
- **THEN** a separate shell solid covers the top and both sides of the housing there,
  with a V-shaped opening in its top and a window in each side; its outer faces are no
  more than 3.20 mm from the centreline and 4.00 mm above the seating plane; and its side
  walls end no more than 0.15 mm above the seating plane

#### Scenario: Shell and leads do not collide
- **WHEN** the shell and the leads under it (pins 1 and 4) are checked for intersection
- **THEN** their common volume is zero

#### Scenario: Front flange and nose detail
- **WHEN** the front of the model is inspected
- **THEN** a flange spans the housing cross-section directly behind the nose with a notch
  at its top, the nose face has a raised ring, and the bore entry is chamfered while the
  bore stays Ø3.60 ± 0.05 mm behind the chamfer

#### Scenario: Forked lead tips
- **WHEN** a lead is viewed from above
- **THEN** its outer end has a semicircular notch, and the lead still lies entirely within
  its 1.50 × 2.60 mm pad

#### Scenario: Envelope unchanged
- **WHEN** the detailed model is measured
- **THEN** its bounding box matches the "Datasheet-derived outline dimensions" requirement,
  so the details add nothing outside the outline envelope

### Requirement: Lead positions match the datasheet PCB layout
The model SHALL have six leads, each 1.0 mm wide along the plug axis and 0.2 mm thick. Their
centres, measured along the plug axis from the housing front face, SHALL be:

- +X side: pin 4 at 2.75 mm, pin 2 at 9.4 mm, pin 5 at 11.5 mm
- −X side: pin 1 at 2.75 mm, pin 3 at 5.5 mm, pin 6 at 10.5 mm

The tolerances are the drawing's: ±0.2 mm on 9.4, ±0.3 mm on 10.5 and 11.5, and the
general tolerance elsewhere. Lead tips SHALL span 8.3 ± 0.3 mm across the body, and lead
bottoms SHALL lie on the seating plane.

#### Scenario: Leads land on the pads
- **WHEN** the model is overlaid on a footprint with six pads, each 1.50 mm along the
  plug axis by 2.60 mm across it, with outer pad edges 8.80 mm apart, at the datasheet
  PCB-layout positions
- **THEN** every lead's footprint on the seating plane lies inside its pad

#### Scenario: Pin side orientation
- **WHEN** the model is viewed from the top with the plug opening pointing toward +Y
- **THEN** pins 2, 4 and 5 are on the +X side and pins 1, 3 and 6 are on the −X side,
  matching the datasheet's component top view and PCB layout

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
