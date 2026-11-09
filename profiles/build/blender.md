# Build: Blender script

Write ONE Python script for Blender that builds the model exactly as the guide above describes, so the result can be compared with the reference.

- Start from an empty scene: `bpy.ops.wm.read_factory_settings(use_empty=True)`.
- Output folder: `out = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else sys.argv[-1]`.
- Follow the guide's phases in order, one function per phase, with the guide's names and values (dimensions, locations, modifiers, materials). Where the guide says "by eye", use its starting values.
- Use `bpy.data` and `bmesh` where possible; if you use operators, make sure they work in background mode (no viewport).
- Add a camera that matches the reference view (for an image: the same angle; for a video: the clearest view of the finished object), a sun light and a light-grey world, and frame the whole model.
- Render with Cycles on the CPU, 32 samples, denoising on, 960 x 720, to `os.path.join(out, "render.png")`.
- Save `os.path.join(out, "model.blend")`.
- Print `BUILD OK` at the end.

Reply with the script only, in one ```python block.
