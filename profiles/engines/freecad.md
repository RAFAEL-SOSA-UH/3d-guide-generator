# Engine: FreeCAD

- **Kind**: parametric CAD. Units: millimetres. Default version: FreeCAD 1.0 or newer.
- **Phases** by workbench: Part Design (most parts), Sketcher, Part (simple solids and booleans), TechDraw (drawings). **Sections** by feature: one sketch + the feature that uses it.
- **Workflow per part**: Part Design > Create body → Create sketch on a plane (XY, XZ, YZ) or a face → draw → constrain → feature (Pad, Pocket, Revolution, Groove, Fillet, Chamfer, Mirrored, Linear/Polar Pattern).
- **Constraints**: give every sketch its constraints explicitly (coincident, horizontal, vertical, symmetric, distance, radius) until the Sketcher says *Fully constrained*. Dimensions in a table per sketch.
- **Design intent** goes in the Objective: which dimension drives the others. Key dimensions can live in a Spreadsheet and be referenced by name.
- **Reference**: Image workbench > Create image plane, scaled to a known dimension.
- **Views**: `0` isometric, `1` front, `2` top, `3` right; `V, F` fit all.
- **Checkpoints**: the model tree has no errors (no red marks), the expected view matches the reference.
- **Export**: STEP for CAD, STL or 3MF for 3D printing, OBJ/glTF for game engines (via the Mesh workbench or File > Export).
- **Can the guide be tested automatically?** Yes: FreeCAD's Python API, also headless with `FreeCADCmd`.
