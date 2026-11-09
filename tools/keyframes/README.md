# keyframes

Turns a video tutorial into **key frames + an aligned transcript**, ready to read in Obsidian or to hand to an AI. Runs locally; no AI involved.

Instead of every frame (a 25-minute video at 30 fps has ~45,000), it keeps only the ones that matter:

1. **Scene changes**: when the picture really changes (a menu opens, the mode changes, an object appears).
2. **Visual moments**: when the instructor says "like this", "right here", "as you can see"... (needs the transcript). Spanish phrases are included too; add your own with `--keywords`.
3. **Fillers**: if nothing changes for more than 20 s, one frame now and then.
4. **No duplicates**: near-identical images are dropped.
5. **On-screen text (optional)**: with OCR it reads menus, the status bar, values in side panels.

At the end it prints an **estimate of the tokens** the output costs when sent to Claude (see [docs/token-estimates.md](../../docs/token-estimates.md)).

## Folder

```
keyframes/
  keyframes.py       the program
  install.bat        creates the .venv environment and installs dependencies (once, Windows)
  process.bat        drag a video onto it (Windows)
  requirements.txt   Python dependencies (only Pillow)
  videos/            put your videos and transcripts here (ignored by git)
  output/<video>/    result for each video (ignored by git)
```

Each output contains:

```
output/<video>/
  frames/0001_00m00s.jpg ...   full frames (up to 1280 px wide)
  sheets/sheet_01.jpg ...      contact sheets: 6 frames per image, numbered, with timestamp
  index.md                     every frame with what is said in that stretch (read it in Obsidian)
  for_ai.md                    compact version: [time] sheet N, panel M: text
  data.json                    everything in structured form
```

## Install (Windows, once)

1. **Python 3.10 or newer**: https://www.python.org/downloads/ (tick "Add python.exe to PATH").
2. **ffmpeg**, in PowerShell or Terminal:
   ```
   winget install Gyan.FFmpeg
   ```
3. **Optional, to read on-screen text**: Tesseract.
   ```
   winget install UB-Mannheim.TesseractOCR
   ```
   If it is not found afterwards, add `C:\Program Files\Tesseract-OCR` to the PATH.
4. **Double-click `install.bat`**: creates `.venv` and installs Pillow inside it. Nothing is installed in your global Python.

Close and reopen the terminal after installing ffmpeg or Tesseract so they are found.

On macOS / Linux: install `ffmpeg` (and optionally `tesseract`) with your package manager, then `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.

## Use

**Quick way (Windows):** put the video in `videos/` and drag it onto `process.bat`. If a file with the same name and extension `.srt`, `.vtt`, `.txt` or `.md` is next to the video, it is used as the transcript. The result goes to `output/<video name>/`.

**From a terminal** (in this folder):

```
.venv\Scripts\activate
python keyframes.py "videos\Slime.mp4" -t "videos\Slime.txt"
python keyframes.py "videos\Slime.mp4" -t "videos\Slime.srt" --ocr
python keyframes.py "videos\Slime.mp4" --threshold 0.08
```

### Transcript

Accepted:
- **SRT / VTT** subtitles.
- **Text copied from YouTube** ("...more" > *Show transcript*, select all, copy): the timestamp on one line and the text below. Lines with `timestamp text` on the same line are read as chapters, so you can paste the video's chapter list at the top.

Without a transcript it still works, but it cannot find the visual moments or align the text. If the transcript is not next to the video when you process it, the output says "(no text)": process it again.

### Options

| Option | What for | Default |
|---|---|---|
| `--threshold` | Scene-change sensitivity. Lower = more frames. Blender changes are small: try `0.08` if you get too few | `0.12` |
| `--max-gap` | Maximum seconds without a frame | `20` |
| `--min-gap` | Minimum seconds between frames | `2` |
| `--similar` | How similar two images must be to drop one. Higher = drops more, `-1` keeps all | `3` |
| `--width` | Frame width | `1280` |
| `--per-sheet` / `--columns` | Contact sheet layout | `6` / `3` |
| `--ocr` | Read on-screen text | off |
| `--ocr-lang` | Tesseract language | `eng` |
| `--keywords` | Your own keywords for visual moments | English + Spanish |

## Giving it to an AI

- **Whole video**: `for_ai.md` + the images in `sheets/`. A 25-minute video is usually 20-40 sheets.
- **One part** (for example where you got stuck): find the time in `index.md` and send that full frame from `frames/` with its text. More detail, fewer images.
- **With the vault**: ask *"make the guide using the frames in output/<video>"*. The AI reads `for_ai.md` and the sheets, and copies only the important frames (the parts you need to watch) into the vault's `guides/Attachments/`.

## Notes

- Scene detection scans the whole video: a 25-minute 1080p video takes 1-3 minutes depending on the computer.
- Re-running on the same video replaces the previous frames and sheets.
- Read [docs/copyright.md](../../docs/copyright.md) before downloading any video.
