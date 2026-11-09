# 3D Guide Generator

Turn a **video or an image** into a **step-by-step guide** for the 3D program you choose: **Blender, FreeCAD, Fusion 360, OpenSCAD or Onshape** (one per guide). A beginner can follow the guide without rewatching the video, and an AI can help when they get stuck.

> **This is a learning tool first.** The goal is that *you* build the model and understand how. The AI writes the guide, explains the confusing parts and helps you when you get stuck. It *can* do the work for you, but then you learn much less. See [Learn mode vs. build mode](docs/learn-vs-build.md).

## Three kinds of input

The less the input shows, the more the AI has to invent, and the guide says so: every section is marked `Source: video`, `Source: deduced` or `Source: proposed`.

| Input | What it shows | What the AI does | Freedom |
|---|---|---|---|
| Tutorial video (`--mode tutorial`) | Every step, explained | Reorders and clarifies, replaces "by eye" with exact values, flags what changed since the video | Low: the result is the video's |
| Video of the result (`--mode showcase`): turntable, timelapse, showcase | The finished object, maybe the process sped up | Reconstructs the order from what is visible, invents the steps in between | Medium |
| Image(s) (`--mode image`) | One or more views of the object | Splits it into parts, invents the whole process and the hidden sides | High: one possible way |

## Five programs

| `--engine` | Kind | Units | The guide is organised by | Can the AI test the guide? |
|---|---|---|---|---|
| `blender` | Mesh, artistic | m | Workspace and mode | Yes (Python, live connection) |
| `freecad` | Parametric CAD | mm | Workbench, sketch + feature | Yes (Python, also headless) |
| `fusion360` | Parametric CAD | mm | Timeline: sketch + feature | Partly (API inside Fusion) |
| `openscad` | CAD by code | mm | Code modules, added step by step | Yes (renders from the command line) |
| `onshape` | Parametric CAD in the browser | mm | Part Studio: sketch + feature | Hard (web API with your account) |

Each program has a profile in [`profiles/engines/`](profiles/engines/); the common rules are in [`profiles/rules.md`](profiles/rules.md) and each input mode in [`profiles/modes/`](profiles/modes/). Adding a program = adding one profile.

## Quick start

Requirements: Python 3.10+, `pip install -r requirements.txt`, and [ffmpeg](https://ffmpeg.org/) for videos.

```
python guidegen.py examples/chest/chest.png
```

Without `--engine`, the generator asks four questions in the terminal, each with a token estimate, and sums them up before doing anything:

```
1) Which AI?                                     input  output (guide, normal detail)
 > 1) Claude Opus 5.5              in ~  4k  out ~ 12k   direct
   2) Claude Sonnet 5.5            in ~  4k  out ~ 10k   direct
   3) Claude Haiku 5.5             in ~  4k  out ~  8k   direct
   4) OpenAI GPT-5.2-Codex         in ~  3k  out ~ 10k   copy & paste (rough estimate)
   5) Google Gemini                in ~  3k  out ~ 10k   copy & paste (rough estimate)
   6) Other AI (copy and paste)    in ~  4k  out ~ 10k   copy & paste (rough estimate)
2) How detailed?        Normal ~16k | High ~22k
3) Which program?       Blender | FreeCAD | Fusion 360 | OpenSCAD | Onshape
4) What should the AI do?
 > 1) Guide only                                         ~16k
   2) Guide + build it once             + 20k  = ~36k
   3) Guide + build and fix it (max 3 rounds) +21k/round, up to ~99k   [coming soon]

Summary: Claude Opus 5.5 · Blender · image · detail normal · guide + build once · ~36k tokens
Continue? [Y/n]
```

The same with options, no questions:

```
python guidegen.py examples/chest/chest.png --engine freecad                 # package only
python guidegen.py video.mp4 -t video.txt --engine blender --call            # tutorial video, ask Claude
python guidegen.py chest.png --engine blender --model claude-opus-5-5 --build  # guide + build once
python guidegen.py turntable.mp4 --engine openscad --mode showcase --detail high
```

### What the AI can do

| Task | What happens | Needs |
|---|---|---|
| Guide only | The AI writes the guide | Any AI (direct or copy & paste) |
| Guide + build it once | Then the AI writes a script that builds the model following its own guide; it runs on your computer and you get `build/render.png` and `build/compare.jpg` (reference next to the result) | A direct AI + Blender or OpenSCAD installed (`BLENDER_PATH` / `OPENSCAD_PATH` if not found, or `pip install bpy`) |
| Guide + build and fix it | The AI compares the result with the reference, fixes the guide and tries again, with a maximum of rounds and a stop when it stops improving | Coming soon |

Building is a check of the guide, not the goal: you still follow the guide yourself.

### Choosing the AI

The list and its numbers live in [`models.json`](models.json): add or edit a model there, no code changes. Each entry says how that provider counts image tokens, the usual length of a guide and of a build script, and whether `guidegen.py` can call it directly. **Direct calls are Claude only for now** (set `ANTHROPIC_API_KEY`); for any other AI you get the package and paste it into its chat. Entries marked "rough estimate" are approximations: check the provider's documentation.

At the end of a direct run the generator prints the tokens really used next to the estimate, and saves both in `manifest.json`.

### What you get

`output/<name>-<engine>/`:

| File | What it is |
|---|---|
| `images/` | The images to attach, in order, already resized to what the model reads |
| `prompt.md` | The whole request: rules + program + mode + template + source material |
| `manifest.json` | Choices, token estimate and, after a direct run, the tokens used |
| `guide.md` | The guide (direct AI) |
| `parts_map.jpg` | Image mode: the parts drawn and numbered on the image |
| `build/` | Build once: the script, `render.png`, `compare.jpg`, `build_log.txt` |

**Copy & paste**: attach the images and paste `prompt.md` into the AI's chat. In image mode, save the answer as `guide.md` and draw the parts map with `python guidegen.py --parts-from output/<...>/guide.md --image output/<...>/images/view_01.jpg`.

## What is in this repo

| Folder | What it is | Needs AI? |
|---|---|---|
| `guidegen.py` | The generator and its terminal wizard | Only for direct calls |
| [`models.json`](models.json) | The AI models and their token estimates | — |
| [`profiles/`](profiles/) | Rules, one profile per program, one per input mode, build instructions, the guide template | — |
| [`tools/keyframes/`](tools/keyframes/) | Video → key frames, contact sheets and a compact text file. Used by the generator; also works on its own | No |
| [`vault-template/`](vault-template/) | An Obsidian vault to keep and follow the guides, with rules for an AI assistant that works in it (set up for Blender) | The guides are written by the AI |
| [`examples/`](examples/) | One input and its guide for each kind of input, with original material | — |
| [`docs/`](docs/) | Token estimates, what needs AI, learn vs build, copyright | — |

## Cost

About **4-7k input tokens for one image**, **30-50k for a 25-minute video** (contact sheets + transcript), plus 8-18k output tokens for the guide; building it once adds about 20-25k. The wizard shows the estimate for your input and choices. Details and ways to cut it: [docs/token-estimates.md](docs/token-estimates.md).

## Copyright

Do **not** publish transcripts, frames or guides that reproduce someone else's tutorial step by step, or models that copy someone else's design. Keep them on your computer for your own study and link to the original. Read [docs/copyright.md](docs/copyright.md).

## Roadmap

- Build and fix: the AI follows its own guide in a separate file, compares the result with the reference (screenshots + a local silhouette score), fixes the guide and stops after a few rounds or when it stops improving.
- Build for FreeCAD (its Python API can run without a window).
- Direct calls to other AI providers.
- More programs (Maya, 3ds Max, SketchUp, Godot CSG...): one profile each.

## License

MIT for the code, profiles and templates. See [LICENSE](LICENSE). The videos and images you process belong to their authors.
