# Engine: OpenSCAD

- **Kind**: CAD by code (constructive solid geometry). Units: millimetres by convention.
- **Phases**: preparing the file (parameters at the top), then one phase per part as a `module`, then assembly and export. **Sections**: one code change each.
- **Steps are code**: each section adds or changes a small block of code, shown in a ```openscad block, followed by what to look at in the preview. Never dump the whole file at once; the final file goes at the end for checking.
- **Building blocks**: `cube`, `sphere`, `cylinder`, `polygon`; `translate`, `rotate`, `scale`, `mirror`; `union`, `difference`, `intersection`; `linear_extrude`, `rotate_extrude`; `hull`, `minkowski` for rounded shapes; `$fn` for smoothness.
- **Design intent**: named variables at the top (they also appear in the Customizer); the Objective says which variable drives what.
- **Checkpoints**: `F5` preview after every section; `F6` full render before export. `#` before an object highlights it while debugging.
- **Export**: `F6` then File > Export (STL, 3MF, OFF).
- **Can the guide be tested automatically?** Yes: `openscad -o out.png file.scad` renders an image from the command line.
