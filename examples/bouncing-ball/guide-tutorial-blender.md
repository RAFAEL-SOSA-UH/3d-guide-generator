---
type: guide
engine: blender
mode: tutorial
video: Bouncing ball loop (fictional example)
duration: "06:00"
url: 
source: "ai/Sources/YouTube/Bouncing ball loop.md"
file_checked: "resources/YouTube/Ball/ball.blend (live, 2026-01-10 18:20)"
app_version: "Blender 5.1"
tags: [guide, example]
---
# YT - Bouncing ball loop (example)

> This guide follows a **fictional** video and only shows the format. It is not taken from any real tutorial.

> **Result:** a ball that bounces in place forever, squashing when it lands.
> **Time you really need to watch:** ~1 min (section 2.3, to compare the result).

## Guide

### Phase 0 - Fix previous
Source: proposed (from checking your file)

I checked your file: the sphere and its material are fine. Before continuing:

- [ ] The ball's scale is `2, 2, 2` (from scaling it in Object Mode). Animation will look fine, but export will not: `Ctrl+A` > **Scale**
- [ ] The video assumes the origin is at the bottom of the ball; yours is in the centre. Edit Mode, select the lowest vertex, `Shift+S` > **Cursor to Selected**; Object Mode, right click > **Set Origin** > **Origin to 3D Cursor**
- [ ] `Ctrl+S`

### Phase 1 - Bounce (Blender, Animation)
Phrase in the video (1:10): "let's make it bounce". Ball selected, Object Mode, frame 0.

> [!warning] This phase does not follow the video's order
> In the video (1:10-4:30) the keys are placed by eye, then moved in the Graph Editor and partly deleted. Here they are set once from a table with exact values, then only the landing keys change handle type. Same result. Open the video at 4:30 only to compare.

#### 1.1 Keys from a table · Object Mode
Phrase (1:25): "first key on the ground".
Source: video (order changed, values made exact)

> [!info] Objective
> A 20-frame loop that starts and ends squashed on the ground, so the landing of one bounce is the push-off of the next. In the `N` panel, **Location Z** is the height and **Scale** X/Y/Z is the shape.
> ```
> height 3 |        * 10
>          |      /    \
>        0 *--* 2        * 20
> ```

For each row: go to the frame, type the values in `N` > **Item**, mouse over the 3D view, `I`.

| Frame | Pose | Location Z | Scale X and Y | Scale Z |
|---|---|---|---|---|
| 0 | Squashed on the ground | `0` | `1.3` | `0.7` |
| 2 | Stretched, leaves the ground | `0` | `0.85` | `1.2` |
| 10 | Top | `3` | `1` | `1` |
| 20 | Same as 0 | `0` | `1.3` | `0.7` |

- [ ] Frame 0
- [ ] Frame 2
- [ ] Frame 10
- [ ] Frame 20

#### 1.2 Fast at the bottom, slow at the top · Dope Sheet
Phrase (3:40): "it needs to snap off the ground".
Source: video
- [ ] `Alt` + click a key on frame 0, `Shift+Alt` + click one on frame 2 and one on frame 20
- [ ] `V` > **Vector**
- [ ] Timeline **End**: `19` (frame 20 equals frame 0), `Space`

> [!warning] In the video (2:05)
> Pressing `I` shows a menu in the video. Since Blender 4.1, `I` over the 3D view inserts the key directly; the menu is on `K`.

## Video map
| # | Starts at | Type | What happens |
|---|---|---|---|
| 1 | 0:00 "welcome back" | SKIP | Intro |
| 2 | 1:10 "let's make it bounce" | READ | Keys (table in 1.1) |
| 3 | 3:40 "it needs to snap off the ground" | READ | Vector handles |
| 4 | 4:30 "and here's the result" | WATCH (optional) | Compare with yours |
| 5 | 5:20 "see you next time" | SKIP | Outro |

## Tools
| Tool | Where in the guide | What for / why | Where it is |
|---|---|---|---|
| Keyframes | 1.1 | Store height and shape at each frame | `I` over the 3D view |
| Vector handles | 1.2 | Sharp take-off and landing | Dope Sheet, `V` |

## Shortcuts
| Shortcut | What it does | Mode | Where in the guide | Why there |
|---|---|---|---|---|
| `Ctrl+A` | Apply transforms | Object | 0 | Scale back to 1 before animating |
| `N` | Side panel | Object | 1.1 | Type exact values |
| `I` | Insert keyframe | Object | 1.1 | One key per table row |
| `Alt` + click | Select all keys on a frame | Dope Sheet | 1.2 | Change all channels of that frame |
| `V` | Handle type | Dope Sheet | 1.2 | Vector at the ground |

## My notes
