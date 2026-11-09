# Examples

One example per kind of input. All the material is original (made for this repo), so it can be published.

| Example | Input | Mode | Program | Guide |
|---|---|---|---|---|
| Bouncing ball | A fictional tutorial video (not included) | `tutorial` | Blender | [guide-tutorial-blender.md](bouncing-ball/guide-tutorial-blender.md) |
| Treasure chest | [chest_build_turntable.mp4](chest/chest_build_turntable.mp4): the parts appear one by one, then it turns | `showcase` | Blender | [guide-showcase-blender.md](chest/guide-showcase-blender.md) |
| Treasure chest | [chest.png](chest/chest.png): one render | `image` | FreeCAD | [guide-image-freecad.md](chest/guide-image-freecad.md) + [parts_map.jpg](chest/parts_map.jpg) |

## How they were made

The chest was modelled and rendered in Blender 5.1 for this repo with [make_chest.py](chest/make_chest.py) (`chest.blend` is the result). Then:

```
python guidegen.py examples/chest/chest_build_turntable.mp4 --engine blender --mode showcase --title "Treasure chest"
python guidegen.py examples/chest/chest.png --engine freecad --title "Treasure chest"
```

Each `prompt.md` (with its images) was given to Claude, the same request `--call` sends, and the answers were saved as the guides. For the image guide, the parts map was drawn locally from the parts list at the end of the guide:

```
python guidegen.py --parts-from examples/chest/guide-image-freecad.md --image examples/chest/chest.png
```

## Tested or not

- **Blender guide**: its key steps (the cylinder, Bisect and the band sizes) were run with Blender's Python API. That test found a real mistake in the first draft: the lid's sizes in the `N` panel follow the object's rotated axes, so the guide now applies the rotation first. This is the kind of check the planned self-test mode will do automatically.
- **FreeCAD guide**: written from the image, not run in FreeCAD. If a step does not match your version, open an issue.
- **Bouncing ball**: a format example for tutorial mode; the video is fictional.
