# Rules for the AI in this vault

Read this file before doing anything in the vault. The person using it is **learning**: the guides exist so they can build things themselves. Do the work for them only when they ask.

## Settings (edit these)

- Language of the guides: **English**
- Main app and version: **Blender 5.1** (update when you upgrade)
- Keyframes tool output folder: `<path to tools/keyframes/output>`
- Live connection to the app (MCP): **yes / no**

## Zones

- `guides/`: finished guides, one folder per course (same name as in `resources/Courses/`) and `guides/YouTube/` for single videos. **The AI creates new guides here, but once created they belong to the person**: they edit them and add their own notes. The AI does not modify, move or delete an existing note in `guides/` unless asked, and never overwrites an existing file. The person's notes in `guides/` can be read to adapt the next guides.
- `ai/`: the AI's working area.
- `resources/`: course files (including the person's `.blend` files, stored per course) and a reusable library. The AI may read, link or open them, but must not modify, move or delete them without permission.

## Inside ai/

- `Sources/<course>/`: raw transcripts pasted by the person. Read, do not modify.
- `_templates/`: format of the guides (`Video guide.md`, `Section guide.md`) and of the reference notes.
- `Techniques/`, `Recipes/`, `Problems/`, `Shortcuts/`: reference notes the AI maintains, using the templates in `_templates/`.
- Before creating a technique note, check if it exists. If it does, add the new link under "Seen in" instead of duplicating it.
- Keep `Techniques/Technique map.md` and `Shortcuts/Essential shortcuts.md` up to date.
- `Prompts/`: prompts and `How to process a video.md`.

## If there are frames of the video

- If the keyframes tool has an output for the video, use `for_ai.md` and the images in `sheets/` to write the guide: confirm what is selected, which menu opens and what each step looks like, instead of guessing from the transcript.
- Copy only the important frames into the vault: for the WATCH steps, copy the useful frame from `frames/` to `guides/Attachments/` (name `<guide> - <time>.jpg`) and embed it under the step with `![[name.jpg]]`.

## Goal of the guides

Maximise time building and minimise time watching or rewinding. The guide is "what to do", with the "why" only where it is needed to understand (Objective boxes).

### Classify the video

Split the video into continuous stretches that cover all of it:
- **SKIP**: intros, outros, self-promotion, long explanations, repeating what was already said, instructor mistakes that are undone later.
- **READ**: actions that text describes exactly: shortcuts, menus, numeric values, toggles.
- **WATCH**: movement or the visual result matters: moving "by eye", sculpting, painting, hard-to-describe selections, comparing the silhouette, or when the instructor says "like this", "about here", "as you can see". **When in doubt, WATCH.**

### Before each guide: check the person's file

- Check their working file (in `resources/`): through the live connection if it is active (**read only**, change nothing), or by reading the saved file.
- Compare it with what should exist at the end of the previous guides: objects, collections, materials and nodes, colour spaces, UVs, render engine, lights, world, animations.
- Write `file_checked:` in the frontmatter with the path and the save date.

### Phase 0 - Fix previous

- The guide starts with `### Phase 0 - Fix previous`: one line with what is fine and a checklist of what to do before the video: mistakes or missing steps from previous guides, and things the video assumes without explaining.
- Each item says what is wrong, which guide it comes from and how to fix it step by step. Ends with `Ctrl+S`.
- If there is nothing to fix, the phase says so in one line.

### The way that works today, not the video's

- Steps are written the way they work in the person's version of the app, not the way the video does them. With the live connection, check doubtful shortcuts, menus and options (keymap, operator and property names) before writing them.
- If the video is outdated (shortcut that no longer exists, menu moved, option renamed) or skips steps without explaining them, the guide's step is the correct and complete one, and at the end of the section there is a note: `> [!warning] In the video (time)` with what the video does and what changed.
- If there is an easier or more current way, add it as a numbered alternative, without replacing the video's step.
- If the person shares comments from the video, use them to find where people get stuck and solve it in the guide.
- What cannot be checked (for example menus of another program), say so in a note instead of stating it as fact.
- If the person already ticked steps in a guide and asks for changes, keep their ticks.

### If part of the video is unclear

- The guide must be followable without the video. If the instructor does something by eye, skips steps, makes a mistake and fixes it later, or goes in circles (setting keys, fixing them, deleting them, moving them), the guide does not copy that path: it writes the direct way to the same result.
- The order of the video may change: explain or do something earlier even if the video does it later, merge steps the video spreads out, or skip corrections that only fix the instructor's own mistake. The end result must be the same as in the video.
- When the video gives values "by eye" (how much to squash, how high, at which frame), the guide gives **exact starting values**, in a table if there are several (for example frame, position and scale of each key), and says they can be adjusted.
- Start the section or phase with `> [!info] Objective`: what we are after, with a drawing if it helps, and the facts needed to understand the steps (for example which axis of the bone is height).
- Mark those sections with `> [!warning] This phase does not follow the video's order` at the top, explaining in one or two sentences what the video does and what the guide changes, and keep the video's time so the result can be compared.
- If the person says they got stuck: check their file (live if possible, read only), say what is right and what fails, and rewrite that part starting from the real state of their file, with a fix section at the start if needed.
- When rewriting part of a guide the person already started, keep the previous version below in a folded callout `> [!note]- Previous version...` with their ticks as they were.

### If the person asks the AI to do a part

- Save a copy of their file first (for example `<name>_before_<section>.blend` next to it) and say where it is.
- Do only the part they asked for, then verify it (evaluate the result, take a screenshot) and save.
- Add a `> [!success] Done by the AI (date)` note at the top of that section saying what was done and anything they must remember later. Keep the manual steps below as reference.
- Learning is the goal: point out where to look to understand what was done.

### The "Guide" section (the main part)

- Reproduces **what is done in the video** as imperative instructions, the way it works today, in the video's order unless another order is clearer (see "If part of the video is unclear"). No challenges or extra exercises.
- **Phases**: a new phase every time the workplace changes: outside the app (web, installer, another program) or a workspace (Layout, Modeling, UV Editing, Shading, Animation, or an editor in another program). Title `### Phase N - Name (where)` and below it the video's phrase where it starts and the starting state.
- **Sections**: inside each phase, one set of steps per thing achieved. Title `#### N.M What is achieved · Mode or editor` (for example `#### 2.3 Eyes without n-gons · Edit Mode`). A phase can have one section. Under the title: `Phrase (time): "..."`, and if the section has an alternative, `(see alternative 00N)`.
- **Objective**: if the section is complex or it is not obvious why it is done, start with `> [!info] Objective` explaining what is achieved and why, before the steps. A drawing in a code block if it helps. A whole phase can have its own "Objective of the whole phase".
- Steps: `- [ ] action (shortcut / menu)`. Include the undos (`Ctrl+Z`) and view changes the instructor makes.
- **WATCH** (with what to look at) only when a step really cannot be followed from text. If there are frames, the image goes under the step.
- **Alternatives** numbered across the guide: `> [!tip] Alternative 00N · for N.M`, right after the section they refer to.
- `> [!warning] In the video (time)` notes go at the end of their section.

### After "Guide"

- Video map (table of SKIP/READ/WATCH stretches with their starting phrase and time), Tools, Shortcuts, Resources and an empty `## My notes`.
- **Tools**: `| Tool | Where in the guide | What for / why | Where it is |`, with section numbers (`1.3; 2.5`).
- **Shortcuts**: `| Shortcut | What it does | Mode | Where in the guide | Why there |`. One shortcut per row, in order of appearance. If the video uses a shortcut that no longer works, say so in "What it does".
- **Resources**: look for the course files before writing the guide and use their exact names in the steps. Table `| File | Where in the guide | What for |`. Use the lesson's PDF, if there is one, to confirm steps the transcript leaves unclear.
- If the transcript is machine-generated or machine-translated, add a folded callout at the top with the misrecognised words and what they mean. Transcripts without timestamps (some course platforms): identify each stretch with an exact quoted phrase so it can be found in the transcript panel.
- No separate Challenge, Practice or Context sections (the why goes in the Objective boxes).

## Style

- Guide language from Settings; app version from Settings; for beginners, no filler, no emojis.
- Links with [[note name]]. Note names must be unique in the whole vault: video guides are named `<course short name> S1-02 - <title>` for courses and `YT - <title>` for single videos.
- Do not copy whole transcripts into the guides: summarise and turn them into steps.
- Use the person's notes in `guides/` to adapt the next guides.
