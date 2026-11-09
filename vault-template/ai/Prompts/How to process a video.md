---
tags: [ai, workflow]
---
# How to process a video

## 1. Get the transcript
- **YouTube**: under the video > "...more" > **Show transcript**. Select all of it and copy (with timestamps). Copy the chapter list from the description too.
- **Udemy and other platforms**: the **Transcript** button in the player. These usually have no timestamps; the guide then uses exact phrases to find each stretch.

## 2. Save it
One file per video in `ai/Sources/<course>/` (see `ai/Sources/README.md`). Course files and your `.blend` files go to `resources/`.

## 3. (Optional) Key frames
If you have the video file and are allowed to use it (see docs/copyright.md in the repo): put the video and the transcript (same name, `.txt`) together and drag the video onto `process.bat`. The output is in the tool's `output/<video>/`.

## 4. Ask for the guide
With this vault connected to the AI:

```
Make the guide for "[video]" from ai/Sources/[course]/[file] following CLAUDE.md.
[Use the frames in <keyframes output path>/[video].]
My working file is resources/[...]/[file].blend.
```

For a whole course section:

```
Process section "[Section 1]" of the course "[name]" in ai/Sources, following CLAUDE.md:
one guide per video and a section index. Create or update the techniques and shortcuts.
```

The guide lands in `guides/<course>/` (or `guides/YouTube/`). From then on it is yours: edit it and write your thoughts in **My notes**.

## 5. Watch the video with the guide next to it
Each guide splits the video into stretches:
- **SKIP**: do not watch.
- **READ**: follow the checklist; video at 2x or not at all.
- **WATCH**: watch the video; the guide says what to look at.

The AI classifies from what the instructor says and, with key frames, from what is on screen. If a READ stretch turns out to need watching, write it in your notes and ask for a fix.

## 6. Stuck?
```
I'm stuck at section [N.M] of [guide]. [What happens.]
Check my file and tell me what is wrong. Don't change anything yet.
```
Then, if needed: "rewrite that section from where my file is", or, only if you decide so, "do that section for me".

## Advice
One section at a time. Processing a whole course at once is fast, but you learn by practising, and each guide should take into account what you already know.
