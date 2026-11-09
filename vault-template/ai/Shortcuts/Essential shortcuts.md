---
tags: [shortcuts]
app_version: Blender 4.x / 5.x
---
# Essential shortcuts (Blender, default keymap)

Almost every shortcut depends on **where the mouse is** (3D view, timeline, Graph Editor...) and on the **mode** (Object Mode, Edit Mode...).

No numpad on your laptop: `Edit > Preferences > Input > Emulate Numpad` (the top-row numbers work as numpad) or use the axis gizmo at the top right of the 3D view.

## The most important
| Shortcut | What it does |
|---|---|
| `F3` | Search any command by name |
| `F9` | Reopen the settings of the last operation |
| `Ctrl+Z` / `Ctrl+Shift+Z` | Undo / redo |
| `Shift+R` | Repeat last action |
| `Tab` | Switch Object Mode / Edit Mode |
| `Ctrl+Tab` | Mode pie menu (Pose Mode with an armature) |
| `N` | Side panel (exact position, rotation, scale) |
| `T` | Toolbar |
| `Ctrl+Space` | Maximise the editor under the mouse |

## Navigation
| Shortcut | What it does |
|---|---|
| Middle mouse + drag | Orbit |
| `Shift` + middle mouse | Pan |
| Wheel / `Ctrl` + middle mouse | Zoom |
| `Numpad .` | Frame selected |
| `Home` | Frame all |
| `Numpad 1 / 3 / 7` | Front / right / top view |
| `Ctrl + Numpad 1/3/7` | Back / left / bottom view |
| `Numpad 5` | Perspective / orthographic |
| `Numpad 0` | Camera view |
| `Numpad /` | Local view (isolate) |
| `` ` `` (key next to 1) | View pie menu |

## Selection
| Shortcut | What it does |
|---|---|
| Left click | Select |
| `Shift` + click | Add / remove from selection |
| `A` / `Alt+A` | Select all / none |
| `Ctrl+I` | Invert selection |
| `B` | Box select |
| `C` | Circle select (wheel = size, `Esc` to exit) |
| `L` (mouse over) / `Ctrl+L` | Select linked piece |
| `Alt` + click | Select loop |
| `Ctrl+Alt` + click | Select ring |
| `Ctrl+Numpad +` / `-` | Grow / shrink selection |

## Transform (Object and Edit Mode)
| Shortcut | What it does |
|---|---|
| `G` / `R` / `S` | Move / rotate / scale |
| ...then `X`, `Y` or `Z` | Lock to an axis |
| ...then `Shift+X/Y/Z` | All axes except that one |
| ...then type a number | Exact value (e.g. `R Z 90 Enter`) |
| `Ctrl` while moving | Toggle snapping temporarily |
| `Shift` while moving | Precise movement |
| `Alt+G / Alt+R / Alt+S` | Reset location / rotation / scale |
| `Shift+Tab` | Toggle snapping |
| `.` (period) | Pivot point pie menu |

## Object Mode
| Shortcut | What it does |
|---|---|
| `Shift+A` | Add object |
| `X` / `Delete` | Delete |
| `Shift+D` | Duplicate |
| `Alt+D` | Linked duplicate |
| `Ctrl+J` | Join objects |
| `Ctrl+A` | Apply transforms (or apply the modifier under the mouse) |
| `Ctrl+P` | Parent |
| `F2` | Rename active object |
| `M` | Move to collection |
| `H` / `Alt+H` / `Shift+H` | Hide / unhide all / hide others |
| `Shift+S` | Snap menu (cursor to selection, etc.) |
| `Ctrl+1 ... Ctrl+5` | Add Subdivision Surface at that level |
| `Z` | Shading pie (solid, material, rendered, wireframe) |
| `Alt+Z` | X-ray |

## Edit Mode (modelling)
| Shortcut | What it does |
|---|---|
| `1` / `2` / `3` | Vertex / edge / face mode |
| `E` | Extrude |
| `I` (twice = individual) | Inset |
| `Ctrl+B` | Bevel (wheel = more segments) |
| `Ctrl+R` | Loop cut |
| `K` | Knife |
| `F` | Fill face / connect two vertices with an edge |
| `J` | Connect vertices |
| `M` | Merge vertices |
| `G G` | Slide vertex / edge along the mesh |
| `Alt+S` | Shrink / fatten along normals |
| `P` | Separate into another object |
| `V` / `Y` | Rip / split |
| `Shift+N` | Recalculate normals |
| `U` | UV unwrap menu |
| `O` | Proportional editing (wheel = radius) |
| `Ctrl+V / Ctrl+E / Ctrl+F` | Vertex / edge / face menus |

## Animation
| Shortcut | What it does |
|---|---|
| `I` (mouse over the 3D view) | Insert keyframe for location, rotation and scale. Over the Dope Sheet it opens a menu that only re-keys existing channels |
| `I` (mouse over a field in the `N` panel) | Insert keyframe for that property only |
| `K` | Keying set menu |
| `Alt+I` | Delete keyframe at the current frame |
| `Space` | Play / pause |
| Left / right arrow | Previous / next frame |
| `Shift+Left arrow` | Go to the first frame |
| `Alt` + click (Dope Sheet) | Select all keys on that frame |
| `T` (Dope Sheet / Graph Editor) | Interpolation (constant, linear, bezier) |
| `V` (Dope Sheet / Graph Editor) | Handle type (Vector = sharp change) |
| `Ctrl+Tab` (Dope Sheet) | Switch to the Graph Editor |
| `Ctrl+Alt+P` (Graph Editor) | Set preview range to the selected keys |
| `Tab` (NLA, on a strip) | Edit that strip's action |
| `Ctrl+P > With Automatic Weights` | Bind a mesh to an armature |
