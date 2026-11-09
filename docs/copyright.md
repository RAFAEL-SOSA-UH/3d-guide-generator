# Copyright and terms of use

*Not legal advice. Rules differ by country and by platform; read the terms of the sites you use.*

## Watching is not the same as owning a copy

A free tutorial on YouTube lets you **watch it on YouTube**. It does not, by itself, give you the right to download the video file or to share copies of it.

- **YouTube**: its terms do not allow downloading videos unless YouTube offers a download button or the creator gives permission. Tools like `yt-dlp` exist, but using them on someone else's video goes against those terms. The transcript you copy from the YouTube page and your own screenshots for personal study are a much lighter use.
- **Udemy and other paid courses**: the videos are protected and their terms forbid downloading them (except offline viewing inside their own app). Use the course transcript, the lesson PDFs and your own screenshots (`Win+Shift+S` on Windows) for the moments you need.
- **Your own videos, or videos with an open licence** (for example Creative Commons): no problem.

## What is fine to keep

On your own computer, for your own study:
- the transcript you copied, the frames and contact sheets, and the guide the AI writes from them;
- your notes, your `.blend` files and the models you build following a tutorial (check if the tutorial ships assets with their own licence, like textures or HDRIs).

## What not to publish

- Models that copy someone else's design or a known character, even if you built them yourself from an image. Fine for practice on your computer, not for your game or a public repo.

- Transcripts, frames, contact sheets or recordings of other people's tutorials.
- Guides that reproduce someone else's tutorial (especially a paid course) step by step. They can replace the original, which hurts the creator.

This is why the repo's `.gitignore` excludes `videos/`, `output/`, and the vault's `ai/Sources/`, `guides/` and `resources/` contents, and why the examples in `examples/` use original material.

## Good practice

- Always link to the original video in the guide's frontmatter (`url:`).
- If a guide helped you, support the creator: like, comment, buy the course.
- If you want to share your guides, ask the creator first, or share only your own notes and the techniques you learned (not the step-by-step).
