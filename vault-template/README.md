# Vault template

An Obsidian vault set up for learning from video tutorials with an AI.

```
vault-template/
  CLAUDE.md        rules the AI reads first (edit the Settings block at the top)
  guides/          your guides: the AI creates them, then they are yours
  ai/              the AI's working area
    Sources/         raw transcripts
    _templates/      guide and note templates
    Techniques/      one note per technique + Technique map
    Shortcuts/       Essential shortcuts
    Problems/        common problems and their fixes
    Recipes/         "build X from these techniques" notes
    Prompts/         How to process a video, Prompts
  resources/       .blend files, course files, your reusable library
```

## Set up

1. Copy this folder wherever you like and open it in Obsidian (**Open folder as vault**).
2. Edit the **Settings** block at the top of `CLAUDE.md` (language, app version, keyframes output path).
3. Give your AI assistant access to the folder (for example, connect it as a folder in the Claude desktop app, or open it with Claude Code). Ask it to read `CLAUDE.md` first.
4. Optional: connect the AI to Blender through an MCP server so it can check your file while you work. Blender MCP servers usually run as an add-on inside Blender that you start from the side panel; the AI only reads unless you ask it to change something.

Then follow `ai/Prompts/How to process a video.md`.
