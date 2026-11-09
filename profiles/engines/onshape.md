# Engine: Onshape

- **Kind**: parametric CAD in the browser. Units: millimetres (set in the document properties). Note: documents on the free plan are public; say so in Phase 0.
- **Phases**: a Part Studio for the parts, an Assembly if parts move or must be positioned with mates. **Sections** by feature in the Feature list: one sketch + the feature that uses it.
- **Workflow per part**: Sketch on Top, Front or Right plane (or a face) → draw → dimensions and constraints until the sketch is fully defined (black lines) → feature (Extrude, Revolve, Sweep, Loft, Fillet, Chamfer, Shell, Mirror, Pattern).
- **Name tools by their toolbar label**; shortcuts are shown in each tool's tooltip — mention them only when sure.
- **Design intent**: key dimensions as Variables (`#name`) defined with the Variable feature at the top of the Feature list.
- **Reference**: insert the image into a sketch and scale it to a known dimension.
- **Checkpoints**: no red features in the Feature list; the named view matches the reference.
- **Export**: right-click the part > Export (STEP, STL, OBJ...).
- **Can the guide be tested automatically?** Hard: Onshape has a web API and FeatureScript, but it needs your account and API keys.
