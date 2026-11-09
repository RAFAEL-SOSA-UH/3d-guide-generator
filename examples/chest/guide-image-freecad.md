---
type: guide
engine: freecad
mode: image
source: "examples/chest/chest.png"
url: 
app_version: "FreeCAD 1.0"
generated_by: "Claude, from prompt.md made by guidegen.py (image mode)"
tags: [guide, example]
---
# Treasure chest in FreeCAD (from an image)

> **This is one possible way to build it.** The source is a single image, so the order, the dimensions and the hidden back are proposed, not copied.
> **Result:** a solid treasure chest (box, rounded lid, two metal bands, lock) ready to export as STEP or STL.
> **Difficulty and time:** beginner, about 45 minutes.

## Parts map

![[parts_map.jpg]]

| # | Part | Base sketch | Feature | Attached to | Difficulty |
|---|---|---|---|---|---|
| 1 | Box | Centred rectangle on XY | Pad 450 mm | (root) | Easy |
| 2 | Lid | Half circle on YZ | Pad symmetric 1000 mm | Box | Easy |
| 3 | Bands | Chest outline + 10 mm, on YZ | Pad symmetric 60 mm + Mirrored | Box and lid | Medium |
| 4 | Lock | Rectangle on XZ | Pad 320 mm | Box | Easy |

**Scale**: a chest you can open in a game is about knee height; I used 1000 × 600 mm for the box and 450 mm to the lid line, which matches the proportions in the image (about 5 : 3 : 2.5). **Hidden sides**: the back and the bottom are not visible; they are made flat.

## Guide

### Phase 0 - Prepare (FreeCAD, Part Design)
Source: proposed

- [ ] **File > New**
- [ ] **Edit > Preferences > General > Units**: Unit system **Standard (mm, kg, s, degree)**
- [ ] Switch to the **Part Design** workbench (workbench list in the toolbar)
- [ ] **Part Design > Create body**
- [ ] Optional reference: **Image** workbench > **Create image plane** with `chest.png`, on the XZ plane; scale it so the box is about 1000 mm wide. Hide it when it gets in the way (`Space` with it selected)
- [ ] `Ctrl+S` as `chest.FCStd`

### Phase 1 - Box (Part Design)

#### 1.1 Base of the box · Sketcher
Source: proposed

> [!info] Objective
> The box is a rectangle extruded upwards. Centring it on the origin keeps every later part symmetric, so the bands and the lock can be placed with simple numbers.

- [ ] **Create sketch** > **XY_Plane**
- [ ] **Sketch > Sketcher geometries > Create centered rectangle**: first click on the origin, second click anywhere
- [ ] Select a horizontal edge > **Constrain horizontal distance**: `1000 mm`
- [ ] Select a vertical edge > **Constrain vertical distance**: `600 mm`
- [ ] The task panel must say **Fully constrained**. **Close**

#### 1.2 Height · Part Design
Source: proposed

- [ ] Sketch selected > **Pad**: Length `450 mm` > **OK**

Checkpoint: `0` (isometric). A 1000 × 600 × 450 mm block.

### Phase 2 - Lid (Part Design)

#### 2.1 Half-round lid · Sketcher
Source: proposed

> [!info] Objective
> The lid is a half circle seen from the side, stretched along the whole length of the box. Its radius is half the depth of the box (300 mm), so it sits exactly on the top edges.
> ```
>         ___
>       /     \      radius 300, centre at height 450
>      |_______|     line closing the bottom, on the top of the box
> ```

- [ ] **Create sketch** > **YZ_Plane** (horizontal = Y, vertical = Z)
- [ ] **Create arc** (centre and end points): centre on the vertical axis above the box, ends to the left and right at the same height
- [ ] **Create line** joining the two ends of the arc (snap to each end point)
- [ ] Select the arc centre and the vertical axis > **Constrain point onto object**
- [ ] Select the arc centre > **Constrain vertical distance**: `450 mm` (from the origin)
- [ ] Select the arc > **Constrain radius**: `300 mm`
- [ ] Select the line > **Constrain horizontal**
- [ ] Select an end of the line and the arc centre > **Constrain horizontal** (puts the line through the centre)
- [ ] **Fully constrained** > **Close**

#### 2.2 Length · Part Design
Source: proposed

- [ ] **Pad**: Length `1000 mm`, tick **Symmetric to plane** > **OK**

Checkpoint: `1` (front) shows the dome on top of the box, flush with the front and back faces.

### Phase 3 - Metal bands (Part Design)

#### 3.1 Band outline · Sketcher
Source: proposed

> [!info] Objective
> A band wraps the chest 10 mm proud of its surface. The sketch is the chest's side outline made 10 mm bigger; the part that falls inside the chest merges with it, so only the outer 10 mm show.

| Dimension | Value |
|---|---|
| Width (Y) | 620 mm |
| Straight part (Z from the floor) | 450 mm |
| Arc radius | 310 mm, centre at 450 mm |
| Position | X = −380 mm, then mirrored |

- [ ] **Create sketch** > **YZ_Plane**
- [ ] In the sketch's **Attachment** (task panel or Property view > Attachment Offset), Position along the normal: `-380 mm`
- [ ] Draw a closed outline with **Create polyline**: along the floor, up the right side, an arc over the top (press `M` to switch the segment to arc), down the left side, back to the start
- [ ] Both side lines **Constrain vertical**, the floor line **Constrain horizontal** (the polyline may have added them already)
- [ ] One bottom corner and the horizontal axis > **Constrain point onto object**
- [ ] The two bottom corners and the vertical axis > **Constrain symmetric**
- [ ] Floor line **horizontal distance** `620 mm`, one side line **vertical distance** `450 mm`
- [ ] Arc centre and the vertical axis > **Constrain point onto object**; arc **radius** `310 mm`
- [ ] **Fully constrained** > **Close**

#### 3.2 Band and its twin · Part Design
Source: proposed

- [ ] **Pad**: Length `60 mm`, **Symmetric to plane** > **OK**
- [ ] With the Pad selected > **Mirrored**: Plane **YZ** (Base YZ plane) > **OK**

Checkpoint: `0`. Two bands at X = ±380 mm, 10 mm proud on the box and the lid.

> [!tip] Alternative 001 · for 3.1
> If the Sketcher says **Redundant constraints**, the one you just added is not needed: delete it from the Constraints list (shown in red). The radius 310 and the width 620 already force the arc to start at the top of the side lines.

### Phase 4 - Lock (Part Design)

#### 4.1 Lock plate · Sketcher and Pad
Source: proposed

> [!info] Objective
> The lock sits on the seam between box and lid, in the middle of the front. Padding from the centre plane to 20 mm past the front face is the simplest way: the part inside merges with the chest.

- [ ] **Create sketch** > **XZ_Plane**
- [ ] **Create centered rectangle**, centre on the vertical axis
- [ ] Width `120 mm`, height `140 mm`, centre at vertical distance `440 mm` from the origin
- [ ] **Close** > **Pad**: Length `320 mm` > **OK**
- [ ] If the lock grows towards the back, edit the Pad and tick **Reversed**

> [!warning] Not checked
> Which way a sketch on XZ_Plane pads by default depends on the plane's orientation; the Reversed box fixes it either way.

Checkpoint: `1`. The lock covers the line between box and lid.

### Phase 5 - Colours and export

#### 5.1 Colours (optional) · Part Design
Source: proposed

- [ ] Select faces > right click > **Appearance** (or **Set colors**): brown for the wood, grey for the bands, gold for the lock

#### 5.2 Export
Source: proposed

- [ ] Select the **Body** in the tree
- [ ] **File > Export**: STEP (`.step`) to keep it as CAD, STL (`.stl`) for 3D printing
- [ ] `Ctrl+S`

## Tools
| Tool | Where in the guide | What for / why | Where it is |
|---|---|---|---|
| Body | 0 | Container for all Part Design features | Part Design > Create body |
| Centered rectangle | 1.1; 4.1 | Rectangle centred on a point, keeps parts symmetric | Sketch > Sketcher geometries |
| Constraints (distance, radius, horizontal, symmetric, tangent, point on object) | 1.1; 2.1; 3.1; 4.1 | Exact dimensions instead of drawing by eye | Sketch > Sketcher constraints |
| Pad | 1.2; 2.2; 3.2; 4.1 | Turn a sketch into a solid | Part Design toolbar |
| Attachment offset | 3.1 | Move a sketch plane along its normal | Sketch properties > Attachment |
| Mirrored | 3.2 | Second band without drawing it again | Part Design > Apply a pattern |

## Shortcuts
| Shortcut | What it does | Mode | Where in the guide | Why there |
|---|---|---|---|---|
| `Ctrl+S` | Save | Any | 0; 5.2 | Keep the file |
| `Space` | Show / hide the selected object | Any | 0 | Hide the reference image |
| `0` | Isometric view | 3D view | 1.2; 3.2 | Check the shape |
| `1` | Front view | 3D view | 2.2; 4.1 | Compare with the image |
| `M` | Switch polyline segment mode | Sketcher (polyline) | 3.1 | Draw lines and the arc in one go |

## Resources
| File | Where in the guide | What for |
|---|---|---|
| `chest.png` | 0 | Reference image |
| `parts_map.jpg` | Parts map | Which part is which |

## My notes

```json
{"parts":[{"n":1,"name":"Box","box":[0.30,0.48,0.71,0.80]},{"n":2,"name":"Lid","box":[0.30,0.31,0.71,0.58]},{"n":3,"name":"Band","box":[0.31,0.31,0.42,0.69]},{"n":3,"name":"Band","box":[0.53,0.36,0.66,0.79]},{"n":4,"name":"Lock","box":[0.40,0.49,0.45,0.58]}]}
```
