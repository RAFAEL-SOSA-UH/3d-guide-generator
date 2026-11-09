---
tags: [ai, prompts]
---
# Prompts

Copy, paste and fill in what is between [brackets]. With this vault connected, the AI already has the guide rules in CLAUDE.md, so short prompts are enough.

## 1. Video to guide (without the vault connected)
```
I'm a beginner in [app and version]. Here is the transcript of a [length] tutorial.
Turn it into a guide for Obsidian.

Guide rules (goal: build more, watch less):
- Main section "Guide": what is done in the video, as imperative instructions,
  the way it works in my version. If part of the video is confusing or done by eye,
  write the direct way to the same result and give exact starting values.
- Phases: a new phase every time the workplace changes. "### Phase N - Name (where)".
- Sections inside each phase: "#### N.M What is achieved · Mode", with the time and phrase.
  Start complex sections with an "Objective" box. Steps as "- [ ] action (shortcut / menu)".
  Mark WATCH (and what to look at) only if a step cannot be followed from text.
- After: "Video map" table | # | Starts at | SKIP/READ/WATCH | What happens |,
  Tools table, Shortcuts table, and an empty "## My notes".
- Do not copy the transcript.

Transcript:
[paste here]
```

## 2. I'm stuck
```
I'm following [guide or video link] at [section / mm:ss].
It should do: [what]. What happens to me: [what].
[Screenshot attached.] I use [app version].
Tell me the most likely cause and how to fix it, step by step. Don't do it for me yet.
```

## 3. Explain the why
```
In the tutorial they do [action]. Why, and what would happen if I didn't?
Give me one example of when to use it and one of when not to.
```

## 4. Plan a model like building blocks
```
I want to model [object] in [low-poly / stylised] style for a game.
These are the techniques I already know: [paste the Technique map].
Give me a step-by-step recipe using mostly those, and at most 1 new technique to learn.
```

## 5. Quick review
```
Quiz me with 10 questions on these shortcuts and techniques: [paste note].
One question at a time, wait for my answer and correct me.
```

## 6. Review my model
```
This is my [object] model for a game (screenshots in wireframe and solid attached).
Review topology, polygon count, proportions and what I should improve first.
```
