# Learn mode vs. build mode

The same setup can be used in two ways. This project is meant for the first one.

## Learn mode (the point of this project)

You build the model. The AI:
- writes the guide so you spend your time in Blender, not scrubbing the video;
- explains *why* in short "Objective" boxes before the complex parts;
- replaces "move it a bit, like this" with exact values you can type, and says you can adjust them;
- checks your file when something looks wrong and tells you what is off;
- rewrites a confusing part of the guide starting from where *your* file is, not from where the video is.

You learn the tools, the shortcuts and the reasons, and after a few videos you need the AI less.

## Build mode

The AI does the steps for you through a live connection to the app (for example, creating keyframes, modifiers or materials with Python in Blender). It works best for things that can be described with numbers:

| Works well | Works poorly |
|---|---|
| Keyframes from a table, modifiers, materials, export settings, cleaning up files | Shapes made "by eye", sculpting, painting, picking the right vertices on an organic mesh |

## When to switch

Getting stuck is normal and is not a reason to give up on learning. A good order:

1. Try the section yourself with the guide.
2. If it does not work, ask the AI to **look at your file and explain** what is wrong.
3. If the explanation is not enough, ask it to **rewrite that section** from your current state.
4. Only if you still cannot, or the part is not what you want to learn right now, ask it to **do that section** for you. Then look at what it did (open the Graph Editor, the modifier stack...) and compare it with the guide.

Keep a copy of your file before the AI changes anything (the vault rules ask the AI to do this).

## A real example

While building the slime from a 25-minute tutorial, the jump animation part was hard to follow: the instructor set keys by eye with constant interpolation, fixed them in the Graph Editor, deleted some, duplicated others and finally shifted everything by one frame. The guide followed the video and was just as confusing.

What helped:
1. The AI read the `.blend` and found the actual problems (idle keys at frames -7 and 67, stray keys in the jump, the bone floating at 4.45 m).
2. It rewrote the section as **tables of exact values per frame**, in a different order from the video, with the bone axes explained first. That rule is now in `CLAUDE.md`: *if part of a video is unclear, the guide may change the order and give exact values, as long as the result is the same*.
3. At that point the learner asked the AI to build the four animations directly, and it did, with a backup first.

Step 3 was a choice, not the goal. The tables in the guide are still there to redo it by hand.
