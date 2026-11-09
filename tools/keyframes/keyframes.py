#!/usr/bin/env python3
"""
keyframes.py

Turns a video tutorial into key frames + an aligned transcript, ready to read
in Obsidian or to hand to an AI.

What it does:
  1. Detects scene changes with ffmpeg (only keeps an image when something changes).
  2. Adds frames where the instructor says "like this", "right here", etc.
  3. Fills long gaps without changes with one frame every N seconds.
  4. Drops near-duplicate images (perceptual hash).
  5. (Optional) Reads on-screen text with OCR (Tesseract).
  6. Packs the frames into contact sheets labelled with their timestamp.
  7. Writes:
       index.md   -> every frame with what is said during that stretch (for Obsidian)
       for_ai.md  -> compact version: text + reference to the contact sheet panel
       data.json  -> everything in structured form
  8. Prints an estimate of how many tokens the output costs when sent to an AI.

No AI is used here: everything runs locally.

Requirements: Python 3.10+, ffmpeg and ffprobe on the PATH, Pillow.
Optional: Tesseract on the PATH for --ocr.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    sys.exit("Pillow is missing. Install it with:  pip install pillow")


KEYWORDS = [
    # English
    "like this", "like that", "right here", "over here", "here", "this one",
    "as you can see", "something like",
    # Spanish
    "así", "aquí", "como ven", "como pueden ver", "algo así", "esto de aquí",
]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def fmt_time(sec: float) -> str:
    sec = max(0, int(sec))
    h, rest = divmod(sec, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def fmt_name(sec: float) -> str:
    sec = max(0, int(sec))
    h, rest = divmod(sec, 3600)
    m, s = divmod(rest, 60)
    return f"{h:02d}h{m:02d}m{s:02d}s" if h else f"{m:02d}m{s:02d}s"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def require(program: str) -> None:
    if shutil.which(program) is None:
        sys.exit(f"Cannot find '{program}' on the PATH. Install it (see README.md) and try again.")


# --------------------------------------------------------------------------- #
# Token estimate (Claude vision)
# --------------------------------------------------------------------------- #

# Claude bills one visual token per 28x28 px patch. Images larger than the
# model's budget are scaled down first. Two tiers (see docs/token-estimates.md):
TIERS = {
    "standard": {"max_edge": 1568, "max_tokens": 1568},
    "high": {"max_edge": 2576, "max_tokens": 4784},
}


def image_tokens(width: int, height: int, tier: str = "standard") -> int:
    lim = TIERS[tier]
    w, h = float(width), float(height)

    def cost(a: float, b: float) -> int:
        return math.ceil(a / 28) * math.ceil(b / 28)

    scale = min(1.0, lim["max_edge"] / max(w, h))
    w, h = w * scale, h * scale
    while cost(w, h) > lim["max_tokens"]:
        w, h = w * 0.98, h * 0.98
    return cost(w, h)


def text_tokens(text: str) -> int:
    # Rough rule of thumb: ~4 characters per token for English prose.
    return math.ceil(len(text) / 4)


# --------------------------------------------------------------------------- #
# Transcript
# --------------------------------------------------------------------------- #

@dataclass
class Segment:
    start: float
    text: str


RE_TIME_ONLY = re.compile(r"^\s*(?:(\d+):)?(\d{1,2}):(\d{2})\s*$")
RE_TIME_AND_TEXT = re.compile(r"^\s*(?:(\d+):)?(\d{1,2}):(\d{2})\s+(.+)$")
RE_SRT = re.compile(
    r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})\s*-->\s*\d{1,2}:\d{2}:\d{2}[,.]\d{1,3}"
)


def _to_sec(h, m, s) -> float:
    return int(h or 0) * 3600 + int(m) * 60 + int(s)


def read_transcript(path: Path) -> tuple[list[Segment], list[Segment]]:
    """Returns (segments, chapters).

    Accepted formats:
      - SRT / VTT  (00:01:02,000 --> 00:01:05,000)
      - Copied from YouTube: one line with the timestamp ("1:34") and the text below it.
      - Lines like "1:34 text" are read as chapters.
    """
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    segments: list[Segment] = []
    chapters: list[Segment] = []

    if any(RE_SRT.search(l) for l in lines[:50]):
        current: Segment | None = None
        for l in lines:
            m = RE_SRT.search(l)
            if m:
                h, mi, s, ms = m.groups()
                current = Segment(_to_sec(h, mi, s) + int(ms) / 1000, "")
                segments.append(current)
            elif current is not None and l.strip() and not l.strip().isdigit() and l.strip() != "WEBVTT":
                current.text = (current.text + " " + re.sub(r"<[^>]+>", "", l.strip())).strip()
        return [s for s in segments if s.text], chapters

    current = None
    for l in lines:
        m = RE_TIME_ONLY.match(l)
        if m:
            current = Segment(_to_sec(*m.groups()), "")
            segments.append(current)
            continue
        m = RE_TIME_AND_TEXT.match(l)
        if m:
            h, mi, s, txt = m.groups()
            chapters.append(Segment(_to_sec(h, mi, s), txt.strip()))
            current = None
            continue
        if current is not None and l.strip() and not l.startswith("#") and l.strip() != "---":
            current.text = (current.text + " " + l.strip()).strip()
    return [s for s in segments if s.text], chapters


def keyword_times(segments: list[Segment], words: list[str]) -> list[float]:
    times = []
    for s in segments:
        t = s.text.lower()
        if any(re.search(r"\b" + re.escape(w) + r"\b", t) for w in words):
            times.append(s.start + 1.5)  # a bit after it is said
    return times


# --------------------------------------------------------------------------- #
# Video
# --------------------------------------------------------------------------- #

def duration(video: Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(video)])
    try:
        return float(r.stdout.strip())
    except ValueError:
        sys.exit(f"Could not read the video duration:\n{r.stderr}")


def detect_scenes(video: Path, threshold: float) -> list[float]:
    """Times where the picture changes more than 'threshold' (0-1)."""
    vf = f"scale=320:-2,select='gt(scene,{threshold})',showinfo"
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video),
             "-vf", vf, "-an", "-f", "null", "-"])
    return [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)]


def extract_frame(video: Path, t: float, dest: Path, width: int) -> bool:
    r = run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
             "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1",
             "-vf", f"scale='min({width},iw)':-2", "-q:v", "3", str(dest)])
    return r.returncode == 0 and dest.exists()


# --------------------------------------------------------------------------- #
# Images
# --------------------------------------------------------------------------- #

def dhash(path: Path, size: int = 8) -> int:
    with Image.open(path) as im:
        g = im.convert("L").resize((size + 1, size), Image.LANCZOS)
        px = list(g.tobytes())
    bits = 0
    for row in range(size):
        for col in range(size):
            i = row * (size + 1) + col
            bits = (bits << 1) | (px[i] > px[i + 1])
    return bits


def distance(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def ocr(path: Path, lang: str, min_conf: float = 75) -> str:
    """Readable on-screen text. Only words Tesseract recognises with high confidence,
    so frames without text do not fill the output with noise."""
    r = run(["tesseract", str(path), "stdout", "-l", lang, "--psm", "11", "tsv"])
    words = []
    for row in r.stdout.splitlines()[1:]:
        col = row.split("\t")
        if len(col) < 12:
            continue
        try:
            conf = float(col[10])
        except ValueError:
            continue
        w = col[11].strip()
        if conf >= min_conf and len(w) >= 2 and re.fullmatch(r"[\w.,:%()+\-/'#]+", w) \
                and re.search(r"[A-Za-z0-9]", w):
            words.append(w)
    return " ".join(words)[:400]


def font(size: int):
    for name in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def contact_sheets(frames: list["Frame"], folder: Path, per_sheet: int, columns: int,
                   cell_width: int) -> list[tuple[int, int]]:
    """Writes the sheets and returns their sizes."""
    folder.mkdir(parents=True, exist_ok=True)
    f = font(max(16, cell_width // 22))
    sizes = []
    for n in range(0, len(frames), per_sheet):
        group = frames[n:n + per_sheet]
        cells = []
        for fr in group:
            with Image.open(fr.path) as im:
                im = im.convert("RGB")
                h = int(im.height * cell_width / im.width)
                cells.append(im.resize((cell_width, h), Image.LANCZOS))
        cell_height = max(c.height for c in cells)
        rows = (len(cells) + columns - 1) // columns
        sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), "black")
        d = ImageDraw.Draw(sheet)
        sheet_no = n // per_sheet + 1
        for i, (c, fr) in enumerate(zip(cells, group)):
            x, y = (i % columns) * cell_width, (i // columns) * cell_height
            sheet.paste(c, (x, y))
            label = f" {i + 1} | {fmt_time(fr.time)} "
            box = d.textbbox((x + 6, y + 6), label, font=f)
            d.rectangle(box, fill="black")
            d.text((x + 6, y + 6), label, fill="yellow", font=f)
            fr.sheet, fr.panel = sheet_no, i + 1
        sheet.save(folder / f"sheet_{sheet_no:02d}.jpg", quality=85)
        sizes.append(sheet.size)
    return sizes


# --------------------------------------------------------------------------- #
# Main process
# --------------------------------------------------------------------------- #

@dataclass
class Frame:
    time: float
    reason: str
    path: Path | None = None
    text: str = ""
    ocr: str = ""
    chapter: str = ""
    sheet: int = 0
    panel: int = 0
    hash: int = field(default=0, repr=False)


def choose_times(dur: float, scenes: list[float], keys: list[float],
                 max_gap: float, min_gap: float) -> list[tuple[float, str]]:
    cand = [(min(0.5, dur * 0.02), "start")] + [(t, "scene") for t in scenes] + [(t, "keyword") for t in keys]
    cand = sorted((min(t, max(0.0, dur - 0.5)), m) for t, m in cand)

    # Fill long gaps
    filled: list[tuple[float, str]] = []
    prev = 0.0
    for t, m in cand + [(dur, "end")]:
        while t - prev > max_gap:
            prev += max_gap
            filled.append((prev, "filler"))
        if m != "end":
            filled.append((t, m))
        prev = t

    # Drop the ones too close together (priority: keyword > scene > filler)
    priority = {"keyword": 3, "start": 2, "scene": 2, "filler": 1}
    chosen: list[tuple[float, str]] = []
    for t, m in sorted(filled):
        if chosen and t - chosen[-1][0] < min_gap:
            if priority[m] > priority[chosen[-1][1]]:
                chosen[-1] = (t, m)
            continue
        chosen.append((t, m))
    return chosen


def main() -> None:
    p = argparse.ArgumentParser(
        description="Turns a video tutorial into key frames + an aligned transcript.")
    p.add_argument("video", type=Path, help="Video file (mp4, mkv, webm...)")
    p.add_argument("-t", "--transcript", type=Path,
                   help="Transcript: SRT, VTT or text copied from YouTube (timestamp on one line, text below)")
    p.add_argument("-o", "--output", type=Path,
                   help="Output folder (default: output/<video name> next to this script)")
    p.add_argument("--threshold", type=float, default=0.12,
                   help="Scene-change sensitivity, 0-1. Lower = more frames (default 0.12)")
    p.add_argument("--max-gap", type=float, default=20,
                   help="Maximum seconds without a frame (default 20)")
    p.add_argument("--min-gap", type=float, default=2,
                   help="Minimum seconds between frames (default 2)")
    p.add_argument("--similar", type=int, default=3,
                   help="Hash distance under which two frames count as equal; higher = drops more, -1 keeps all (default 3)")
    p.add_argument("--width", type=int, default=1280, help="Frame width in px (default 1280)")
    p.add_argument("--per-sheet", type=int, default=6, help="Frames per contact sheet (default 6)")
    p.add_argument("--columns", type=int, default=3, help="Columns per contact sheet (default 3)")
    p.add_argument("--ocr", action="store_true", help="Read on-screen text with Tesseract")
    p.add_argument("--ocr-lang", default="eng", help="Tesseract language (default eng)")
    p.add_argument("--keywords", nargs="*", help="Your own keywords (replace the defaults)")
    a = p.parse_args()

    require("ffmpeg")
    require("ffprobe")
    if a.ocr:
        require("tesseract")
    if not a.video.exists():
        sys.exit(f"Video not found: {a.video}")

    out = a.output or Path(__file__).resolve().parent / "output" / a.video.stem
    frames_dir = out / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("*.jpg"):  # a re-run starts clean
        old.unlink()

    segments, chapters = ([], [])
    if a.transcript:
        segments, chapters = read_transcript(a.transcript)
        print(f"Transcript: {len(segments)} segments, {len(chapters)} chapters")
        if not segments:
            print("WARNING: no timed lines found in the transcript; frames will have no text.")

    dur = duration(a.video)
    print(f"Duration: {fmt_time(dur)}. Detecting scene changes...")
    scenes = detect_scenes(a.video, a.threshold)
    keys = keyword_times(segments, a.keywords or KEYWORDS)
    times = choose_times(dur, scenes, keys, a.max_gap, a.min_gap)
    print(f"{len(scenes)} scene changes, {len(keys)} keyword moments -> {len(times)} candidates")

    frames: list[Frame] = []
    for i, (t, reason) in enumerate(times, 1):
        dest = frames_dir / f"{i:04d}_{fmt_name(t)}.jpg"
        if not extract_frame(a.video, t, dest, a.width):
            continue
        fr = Frame(t, reason, dest)
        fr.hash = dhash(dest)
        if a.similar >= 0 and frames and reason != "keyword" and distance(fr.hash, frames[-1].hash) <= a.similar:
            dest.unlink(missing_ok=True)
            continue
        frames.append(fr)
        print(f"\r  frames kept: {len(frames)}", end="", flush=True)
    print()

    # Renumber so the names are consecutive
    for n, fr in enumerate(frames, 1):
        new = frames_dir / f"{n:04d}_{fmt_name(fr.time)}.jpg"
        if fr.path != new:
            fr.path.rename(new)
            fr.path = new

    # Text of each stretch (from this frame to the next one)
    for i, fr in enumerate(frames):
        end = frames[i + 1].time if i + 1 < len(frames) else dur + 1
        fr.text = " ".join(s.text for s in segments if fr.time - 1.5 <= s.start < end - 1.5).strip()
        chs = [c.text for c in chapters if c.start <= fr.time]
        fr.chapter = chs[-1] if chs else ""

    if a.ocr:
        print("Reading on-screen text (OCR)...")
        for fr in frames:
            fr.ocr = ocr(fr.path, a.ocr_lang)

    print("Building contact sheets...")
    sheets_dir = out / "sheets"
    if sheets_dir.exists():
        for old in sheets_dir.glob("*.jpg"):
            old.unlink()
    sheet_sizes = contact_sheets(frames, sheets_dir, a.per_sheet, a.columns, cell_width=640)

    write_outputs(a.video, out, dur, frames, segments)
    print(f"\nDone: {len(frames)} frames, {len(sheet_sizes)} sheets.")
    print(f"Folder: {out}")
    print_estimate(out, frames, sheet_sizes)


def print_estimate(out: Path, frames: list[Frame], sheet_sizes: list[tuple[int, int]]) -> None:
    with Image.open(frames[0].path) as im:
        fw, fh = im.size
    text = text_tokens((out / "for_ai.md").read_text(encoding="utf-8"))
    print("\nEstimated tokens if you send this to Claude (input only, approximate):")
    print(f"  for_ai.md (text)            ~{text:,}")
    for tier in TIERS:
        s = sum(image_tokens(w, h, tier) for w, h in sheet_sizes)
        f = len(frames) * image_tokens(fw, fh, tier)
        print(f"  [{tier} tier] all sheets   ~{s:,}   |  all frames ({fw}x{fh}) ~{f:,}")
    print("  Tip: send for_ai.md + sheets for the whole video, and full frames only for the parts you need.")


def write_outputs(video: Path, out: Path, dur: float, frames: list[Frame],
                  segments: list[Segment]) -> None:
    # index.md: to read in Obsidian
    l = [f"# {video.stem}", "",
         f"Duration: {fmt_time(dur)}. Frames: {len(frames)}.", "",
         "Each section is one frame with what is said from that moment to the next frame.", ""]
    prev_ch = None
    for fr in frames:
        if fr.chapter and fr.chapter != prev_ch:
            l += [f"## {fr.chapter}", ""]
            prev_ch = fr.chapter
        l.append(f"### {fmt_time(fr.time)}  ({fr.reason})")
        l.append(f"![]({fr.path.relative_to(out).as_posix()})")
        if fr.text:
            l.append(f"> {fr.text}")
        if fr.ocr:
            l.append(f"On-screen text: `{fr.ocr}`")
        l.append("")
    (out / "index.md").write_text("\n".join(l), encoding="utf-8")

    # for_ai.md: compact, points to the contact sheets
    l = [f"# {video.stem} - key frames and transcript", "",
         f"Duration {fmt_time(dur)}. The images are in contact sheets (folder `sheets/`), "
         "each panel numbered with its timestamp. Format: [time] sheet N, panel M: what is said in that stretch.", ""]
    for fr in frames:
        line = f"[{fmt_time(fr.time)}] sheet {fr.sheet}, panel {fr.panel}"
        if fr.reason == "keyword":
            line += " (visual moment)"
        line += f": {fr.text or '(no text)'}"
        if fr.ocr:
            line += f" | screen: {fr.ocr}"
        l.append(line)
    (out / "for_ai.md").write_text("\n".join(l), encoding="utf-8")

    data = {
        "video": video.name, "duration": dur,
        "frames": [{**{k: v for k, v in asdict(fr).items() if k not in ("hash", "path")},
                    "file": fr.path.relative_to(out).as_posix(),
                    "timestamp": fmt_time(fr.time)} for fr in frames],
    }
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
