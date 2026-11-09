# Engine: Blender

- **Kind**: mesh modelling, artistic. Units: metres. Default version: Blender 5.1 (say so if a step differs in older versions).
- **Phases** by workspace: Layout, Modeling, Sculpting, UV Editing, Shading, Animation. **Sections** by mode: Object Mode, Edit Mode, Sculpt Mode, Pose Mode, Weight Paint.
- **Reference**: Add > Image > Reference (or Background), aligned to the view it was taken from (`Numpad 1/3/7`).
- **Values**: replace "by eye" with numbers typed in the `N` panel (Item tab) or the operator panel (`F9`); several parts → a table (location, scale, dimensions, segments).
- **Shortcuts depend on where the mouse is** (3D view, Dope Sheet, Graph Editor): say where. Example: `I` over the 3D view inserts a keyframe; over the Dope Sheet it opens a different menu.
- **Animation**: keys as a table per frame; name each action; for game engines, one action per NLA strip, loops whose last frame equals the first.
- **Checkpoints**: a numpad view to compare with the reference; Material Preview or Rendered (`Z`) when colour matters.
- **Clean-up and export**: apply transforms (`Ctrl+A`), check normals, origin at the base, name the object, export FBX (Unreal, Unity) or glTF (Godot, web).
- **Can the guide be tested automatically?** Yes: Python (`bpy`) through a live connection (MCP add-on) or `blender --background --python`.
