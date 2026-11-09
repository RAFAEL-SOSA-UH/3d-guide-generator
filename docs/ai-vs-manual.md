# What needs AI and what does not

The AI is useful in a few specific places. Everything else is ordinary software or your own work, and costs no tokens.

## Step by step

| Step | Who / what | AI needed? | Notes |
|---|---|---|---|
| Get the transcript | You (copy from YouTube / Udemy) | No | |
| Get the video file | You | No | Only if you are allowed to; see [copyright](copyright.md) |
| Extract key frames, contact sheets, `for_ai.md` | `keyframes.py` + ffmpeg | No | Runs locally |
| Resize images, assemble the prompt, estimate tokens | `guidegen.py` | No | Runs locally |
| Draw the numbered parts map (image mode) | `guidegen.py` | No | From the parts list the AI returns |
| Read on-screen text | Tesseract (`--ocr`) | No | Optional |
| Set up the vault, folders, templates | You, once | No | `vault-template/` |
| **Turn the video or image into a guide** | AI | **Yes** | The core. Video: what to skip / read / watch, reorders confusing parts, exact values, what changed since the video. Showcase video and image: splits into parts and invents the steps, marked as deduced or proposed |
| Check shortcuts and menus against your version | AI + live connection to your app | Recommended | Without it the AI guesses from the video |
| Follow the guide and build | **You** | No | This is where you learn |
| Write your own notes in the guide | You | No | The AI reads them to adapt the next guides |
| **Diagnose a problem in your file** | AI + live connection | **Yes, on demand** | "Something looks wrong at step 5.2" |
| Rewrite a part of the guide that did not make sense | AI | On demand | Starts from the real state of your file |
| Do a part for you | AI + live connection | Optional | Build mode; see [learn vs build](learn-vs-build.md) |
| Build the whole model once to check the guide (`--build`) | AI writes a script; Blender or OpenSCAD runs it locally | Optional | The render and the comparison image are made locally |
| Keep technique, shortcut and problem notes up to date | AI | Optional | You can also do it by hand |
| Engine side (Unreal, Godot...) | You, with the guide | Partly | The AI can write import or material scripts; visual node graphs (Blueprints, state machines) are usually done by hand |

## Rule of thumb

- **No AI**: anything mechanical (extracting, converting, organising) and anything that is *your practice* (building, ticking boxes, taking notes).
- **AI**: turning a messy video into clear instructions, and getting you unstuck.
- **AI only if you choose**: doing the work for you.

## Without any AI

The tool and the vault still work on their own: `index.md` from the keyframes tool is a readable "video as a document" (each frame with what is said), and the templates in `vault-template/ai/_templates/` let you write guides by hand.
