# Engine: Fusion 360

- **Kind**: parametric CAD (Autodesk). Units: millimetres. The interface changes between updates: name tools by their toolbar label and mark doubtful menu paths.
- **Phases** by workspace (Design, Render, Manufacture). **Sections** by feature in the timeline: one sketch + the feature that uses it.
- **Workflow per part**: create a Component first (keeps the timeline clean) → Create Sketch on a plane or face → draw → Sketch Dimension and constraints until the sketch lines turn black (fully defined) → feature (Extrude, Revolve, Sweep, Loft, Fillet, Chamfer, Shell, Mirror, Pattern).
- **Common shortcuts**: `L` line, `C` circle, `R` rectangle, `D` sketch dimension, `E` extrude, `F` fillet, `Q` press pull, `M` move. Write the toolbar location too.
- **Design intent**: key dimensions as user parameters (Modify > Change Parameters) referenced by name; say which dimension drives the others in the Objective.
- **Reference**: Insert > Canvas on the matching plane, calibrated to a known dimension.
- **Checkpoints**: the timeline has no warnings, the view (ViewCube) matches the reference.
- **Export**: File > Export (STEP, F3D), STL/3MF for printing, FBX/OBJ for game engines.
- **Can the guide be tested automatically?** Partly: scripts and add-ins (Python API) run inside Fusion.
