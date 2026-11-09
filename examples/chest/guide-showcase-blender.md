---
type: guide
engine: blender
mode: showcase
source: "examples/chest/chest_build_turntable.mp4"
url: 
app_version: "Blender 5.1"
generated_by: "Claude, from prompt.md made by guidegen.py (showcase mode)"
tags: [guide, example]
---
# Treasure chest in Blender (from a showcase video)

> **Result:** a low-poly treasure chest (box, rounded lid, two metal bands, lock) with three materials, ready to export to a game engine.
> **Difficulty and time:** beginner, about 40 minutes.
> **Time you really need to watch:** ~5 s, once, to compare the result (0:02-0:05).

The video shows the chest being assembled part by part (0:00-0:02) and then turning (0:02-0:05). The **order** comes from the video (`Source: deduced`); the **dimensions and techniques** are proposed (`Source: proposed`), estimated from the turntable: the box is about 5 : 3 wide to deep, and the lid is a half cylinder as wide as the box is deep.

## Guide

### Phase 0 - Prepare (Blender, Layout)
Source: proposed

- [ ] **File > New > General**
- [ ] Delete the default cube: click it, `X` > **Delete**
- [ ] `Ctrl+S` as `chest.blend`

### Phase 1 - Box and lid (Layout)
Phrase in the video (0:00): no narration; the box appears first, then the lid.

#### 1.1 Box · Object Mode
Source: deduced (first part to appear) · values proposed

> [!info] Objective
> All parts are placed with exact numbers in the `N` panel, so they fit together without moving anything by eye. The box sits on the floor: its centre is at half its height.

| Object | Dimensions X × Y × Z (m) | Location X, Y, Z (m) | Bevel |
|---|---|---|---|
| Body | 1.0 × 0.6 × 0.45 | 0, 0, 0.225 | 0.015, 2 segments |

- [ ] `Shift+A` > **Mesh > Cube**
- [ ] `F2`: name it `Body`
- [ ] `N` > **Item**: type the Dimensions and Location from the table
- [ ] `Ctrl+A` > **Scale** (so the bevel is the same on every edge)
- [ ] Properties > **Modifiers** (wrench) > **Add Modifier > Generate > Bevel**: Amount `0.015 m`, Segments `2`

#### 1.2 Lid · Object Mode and Edit Mode
Source: deduced (second part to appear) · values proposed

> [!info] Objective
> The lid is a cylinder lying along X, cut in half. Its radius (0.3 m) is half the depth of the box, so the curve starts exactly at the top front and back edges. Cutting with exact numbers in the Bisect panel avoids selecting vertices by hand.
> ```
>      ___
>    /     \     cylinder: radius 0.3, length 1.0, centre at Z 0.45
>   |   +   |    Bisect at Z 0.45, keep the top, fill the cut
>    \_____/  ← removed
> ```

- [ ] `Shift+A` > **Mesh > Cylinder**
- [ ] In the panel at the bottom left (`F9` if it closed): Vertices `32`, Radius `0.3 m`, Depth `1 m`, Location Z `0.45 m`, Rotation Y `90°`
- [ ] `F2`: name it `Lid`
- [ ] `Ctrl+A` > **Rotation**: the `N` panel now shows the lid's size along the world axes (X = length), which 2.1 relies on
- [ ] `Tab` (Edit Mode), `A` to select everything
- [ ] **Mesh > Bisect**, then click and drag a line across the cylinder in the 3D view (any line)
- [ ] In the Bisect panel: Plane Point X `0`, Y `0`, Z `0.45`; Plane Normal X `0`, Y `0`, Z `1`; tick **Fill** and **Clear Inner**
- [ ] `Tab` back to Object Mode
- [ ] Add a **Bevel** modifier: Amount `0.01 m`, Segments `2`

Checkpoint: `Numpad 1` (front). The dome sits on the box and its ends are flush with the sides. In the `N` panel the lid measures 1 × 0.6 × 0.3 m.

> [!warning] Not checked
> The Bisect panel values are in global coordinates. If the cut lands in the wrong place, check that the lid's Location Z is 0.45 and redo the Bisect.

### Phase 2 - Metal bands and lock (Layout)
Phrase in the video (0:01): the two bands appear, then the lock.

#### 2.1 Bands · Object Mode
Source: deduced (third part to appear) · values proposed

> [!info] Objective
> Each band is two pieces: a thin box around the body and a thin copy of the lid, both 1 cm bigger than what they wrap. The lid copy keeps its origin on the flat bottom, so changing its Dimensions keeps it sitting on the box.

| Object | Made from | Dimensions X × Y × Z (m) | Location X, Y, Z (m) |
|---|---|---|---|
| BandBody | New cube | 0.06 × 0.62 × 0.46 | −0.38, 0, 0.225 |
| BandLid | Copy of Lid (`Shift+D`, right click) | 0.06 × 0.62 × 0.31 | −0.38, 0, 0.45 |

- [ ] Make `BandBody`: `Shift+A` > **Mesh > Cube**, name it, type the values, `Ctrl+A` > **Scale**
- [ ] Make `BandLid`: select `Lid`, `Shift+D`, right click (stays in place), name it, type the values
- [ ] On `BandLid`, delete its Bevel modifier (`X` on the modifier header): the metal looks better with sharp edges
- [ ] Select both bands, `Shift+D`, then type `X` `0.76` `Enter`: the second pair lands at X = 0.38

#### 2.2 Lock · Object Mode
Source: deduced (last part to appear) · values proposed

| Object | Dimensions X × Y × Z (m) | Location X, Y, Z (m) | Bevel |
|---|---|---|---|
| Lock | 0.12 × 0.04 × 0.14 | 0, −0.32, 0.44 | 0.008, 2 segments |

- [ ] `Shift+A` > **Mesh > Cube**, name it `Lock`, type the values, `Ctrl+A` > **Scale**, add the Bevel

Checkpoint: `Numpad 1`. The lock covers the line between box and lid, in the middle.

### Phase 3 - Materials (Shading)
Phrase in the video (0:02): the colours are visible on the turntable.

#### 3.1 Wood, metal and gold · Object Mode
Source: proposed (colours taken from the video)

| Material | Base Color (R, G, B) | Metallic | Roughness | Objects |
|---|---|---|---|---|
| Wood | 0.30, 0.13, 0.05 | 0 | 0.7 | Body, Lid |
| Metal | 0.22, 0.22, 0.24 | 1 | 0.45 | the four band pieces |
| Gold | 0.85, 0.60, 0.18 | 1 | 0.3 | Lock |

- [ ] Select `Body` > Properties > **Material** > **New**, name it `Wood`, set the values
- [ ] Select `Lid` > Material > browse button (sphere icon) > `Wood`
- [ ] Same for `Metal` on one band, then browse it on the other three
- [ ] `Gold` on the lock
- [ ] `Z` > **Material Preview** to check

### Phase 4 - Clean-up and export (Layout)

#### 4.1 Compare and export · Object Mode
Source: proposed

- [ ] Watch 0:02-0:05 and compare from a similar angle (`Numpad 1`, then orbit)
- [ ] Select everything except the lid and its two bands, then `Body` last: `Ctrl+J` (one object for the base)
- [ ] Select `Lid` and its two bands, `Lid` last: `Ctrl+J`
- [ ] **File > Export > glTF 2.0** (Godot, web) or **FBX** (Unreal, Unity); modifiers are applied on export by default
- [ ] `Ctrl+S`

> [!tip] Alternative 001 · for 4.1
> To open the chest in a game, put the lid's origin on its hinge: select the joined lid, `Tab`, select one vertex of the back bottom edge, `Shift+S` > **Cursor to Selected**, `Tab`, right click > **Set Origin > Origin to 3D Cursor**. Now rotating the lid on X opens it.

## Video map
| # | Starts at | Type | What happens |
|---|---|---|---|
| 1 | 0:00 | READ | Box, then lid (1.1, 1.2) |
| 2 | 0:01 | READ | Bands, then lock (2.1, 2.2) |
| 3 | 0:02 | WATCH (optional) | Turntable: compare shape and colours |

## Tools
| Tool | Where in the guide | What for / why | Where it is |
|---|---|---|---|
| `N` panel (Dimensions, Location) | 1.1; 1.2; 2.1; 2.2 | Exact sizes instead of scaling by eye | 3D view, `N` > Item |
| Bevel modifier | 1.1; 1.2; 2.2 | Soft edges that catch the light | Properties > Modifiers > Generate |
| Bisect | 1.2 | Cut the cylinder in half with exact numbers | Edit Mode > Mesh > Bisect |
| Duplicate | 2.1 | Bands from the lid, second pair of bands | `Shift+D` |
| Materials | 3.1 | Wood, metal and gold | Properties > Material |
| Join | 4.1 | Fewer objects for the game engine | `Ctrl+J` |

## Shortcuts
| Shortcut | What it does | Mode | Where in the guide | Why there |
|---|---|---|---|---|
| `X` | Delete | Object | 0; 2.1 | Default cube; band's bevel |
| `Ctrl+S` | Save | Any | 0; 4.1 | Keep the file |
| `Shift+A` | Add object | Object | 1.1; 1.2; 2.1; 2.2 | Cube and cylinder |
| `F2` | Rename | Object | 1.1; 1.2; 2.1; 2.2 | Clear names for the game engine |
| `N` | Side panel | Object | 1.1 | Type dimensions and location |
| `Ctrl+A` | Apply scale / rotation | Object | 1.1; 1.2; 2.1; 2.2 | Even bevel; lid sizes along the world axes |
| `F9` | Last operation panel | Object | 1.2 | Cylinder settings |
| `Tab` | Object / Edit Mode | Both | 1.2 | Bisect works in Edit Mode |
| `A` | Select all | Edit | 1.2 | Cut the whole cylinder |
| `Numpad 1` | Front view | Both | 1.2; 2.2; 4.1 | Compare with the video |
| `Shift+D` | Duplicate | Object | 2.1 | Lid band, second pair |
| `Z` | Shading pie | Object | 3.1 | Material Preview |
| `Ctrl+J` | Join | Object | 4.1 | Base and lid as two objects |

## Resources
| File | Where in the guide | What for |
|---|---|---|
| `chest_build_turntable.mp4` | Video map | The source video |

## My notes
