#!/usr/bin/env python3
"""
guidegen.py - turn a video or an image into a step-by-step guide for a 3D program.

Interactive (asks for the AI, the detail level, the program and the task, with a token
estimate for each choice):

    python guidegen.py
    python guidegen.py examples/chest/chest.png

With options (no questions):

    python guidegen.py INPUT [INPUT ...] --engine ENGINE [--mode MODE] [--model ID]
                       [--detail normal|high] [--call] [--build]

INPUT is a video (tutorial or showcase) or one or more images of the same object.
ENGINE is one of: blender, freecad, fusion360, openscad, onshape (one per guide).

Without --call it prepares a package you can paste into any AI chat:
    output/<name>-<engine>/
        images/          the images to attach, in order (resized to what the model reads)
        prompt.md        the whole request: rules + program + mode + template + source material
        manifest.json    what is in the package and the token estimate
With --call (Claude models, ANTHROPIC_API_KEY set) it writes guide.md, and in image mode
parts_map.jpg. With --build it then asks for a script that builds the model, runs it in
Blender or OpenSCAD on your computer and writes build/render.png and build/compare.jpg.

Nothing here needs AI except --call and --build. Videos are processed locally by
tools/keyframes/keyframes.py (ffmpeg). The AI models and their estimates are in models.json.
"""

from __future__ import annotations

import argparse
import base64
import glob
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    sys.exit("Pillow is missing. Install it with:  pip install pillow")

ROOT = Path(__file__).resolve().parent
PROFILES = ROOT / "profiles"
KEYFRAMES = ROOT / "tools" / "keyframes" / "keyframes.py"
MODELS_FILE = ROOT / "models.json"

ENGINES = {
    "blender": ("Blender", "5.1"),
    "freecad": ("FreeCAD", "1.0"),
    "fusion360": ("Fusion 360", "current"),
    "openscad": ("OpenSCAD", "2021.01 or newer"),
    "onshape": ("Onshape", "current"),
}
BUILDABLE = {"blender", "openscad"}  # programs the generator can run from the command line
MODES = ("tutorial", "showcase", "image")
TASKS = ("guide", "build", "iterate")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp"}
VIDEO_EXT = {".mp4", ".mkv", ".webm", ".mov", ".avi", ".m4v"}
TRANSCRIPT_EXT = (".srt", ".vtt", ".txt", ".md")

# Claude vision limits (see docs/token-estimates.md)
MAX_EDGE, MAX_IMAGE_TOKENS = 1568, 1568
RENDER_TOKENS = 1200   # a 960x720 render sent back for comparison
HIGH_DETAIL = 1.5      # output multiplier for --detail high
ITERATE_ROUNDS = 3     # maximum rounds shown for "build and fix"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def patch_tokens(w: float, h: float) -> int:
    return math.ceil(w / 28) * math.ceil(h / 28)


def fit_size(w: int, h: int) -> tuple[int, int]:
    """Largest size with the same aspect ratio that Claude reads without scaling it down."""
    s = min(1.0, MAX_EDGE / max(w, h))
    fw, fh = w * s, h * s
    while patch_tokens(fw, fh) > MAX_IMAGE_TOKENS:
        fw, fh = fw * 0.98, fh * 0.98
    return max(1, int(fw)), max(1, int(fh))


def image_tokens(rule: str, w: int, h: int) -> int:
    """Approximate input tokens of one image for each provider's counting rule."""
    if rule == "openai_tiles":
        s = min(1.0, 2048 / max(w, h))
        w, h = w * s, h * s
        s = min(1.0, 768 / min(w, h))
        w, h = w * s, h * s
        return 85 + 170 * math.ceil(w / 512) * math.ceil(h / 512)
    if rule == "gemini_tiles":
        if w <= 384 and h <= 384:
            return 258
        return 258 * math.ceil(w / 768) * math.ceil(h / 768)
    return patch_tokens(*fit_size(w, h))


def text_tokens(text: str) -> int:
    return math.ceil(len(text) / 3.5)  # a bit pessimistic: guides are not always English


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def k(n: float) -> str:
    return f"{n / 1000:.0f}k" if n >= 1000 else str(int(n))


def save_fitted(src: Path, dest: Path) -> tuple[int, int]:
    with Image.open(src) as im:
        im = im.convert("RGB")
        size = fit_size(*im.size)
        if size != im.size:
            im = im.resize(size, Image.LANCZOS)
        im.save(dest, quality=90)
        return im.size


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


def load_models() -> list[dict]:
    return json.loads(read(MODELS_FILE))["models"]


def find_transcript(video: Path) -> Path | None:
    for ext in TRANSCRIPT_EXT:
        cand = video.with_suffix(ext)
        if cand.exists():
            return cand
    return None


# --------------------------------------------------------------------------- #
# Source material
# --------------------------------------------------------------------------- #

def prepare_images(inputs: list[Path], pkg: Path) -> tuple[list[Path], str]:
    out = pkg / "images"
    out.mkdir(parents=True, exist_ok=True)
    images, lines = [], []
    for n, src in enumerate(inputs, 1):
        dest = out / f"view_{n:02d}.jpg"
        w, h = save_fitted(src, dest)
        images.append(dest)
        lines.append(f"- Image {n} (`{dest.name}`, {w}x{h} px): view {n} of the object.")
    text = ("The source is the attached image(s) of the object, in this order:\n" + "\n".join(lines)
            + "\nIf there is more than one image, they are different views of the same object.")
    return images, text


def video_duration(video: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(video)], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def prepare_video(video: Path, transcript: Path | None, pkg: Path, max_images: int,
                  threshold: float | None, mode: str, max_gap: float | None) -> tuple[list[Path], str]:
    frames = pkg / "keyframes"
    cmd = [sys.executable, str(KEYFRAMES), str(video), "-o", str(frames)]
    if transcript:
        cmd += ["-t", str(transcript)]
    if threshold is not None:
        cmd += ["--threshold", str(threshold)]
    if max_gap is None and mode == "showcase":
        # A showcase often changes slowly (a turntable, a timelapse): sample it evenly, ~24 frames.
        dur = video_duration(video)
        if dur:
            max_gap = max(0.5, dur / 24)
    if max_gap is not None:
        cmd += ["--max-gap", f"{max_gap:.2f}", "--min-gap", f"{min(2.0, max_gap / 2):.2f}"]
    if mode == "showcase":
        cmd += ["--similar", "-1"]  # keep every sample: small additions (a band, a lock) matter here
    print("Extracting key frames (local, no AI)...")
    r = subprocess.run(cmd, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("The keyframes tool failed (see the messages above).")

    sheets = sorted((frames / "sheets").glob("sheet_*.jpg"))
    if len(sheets) > max_images:
        step = len(sheets) / max_images
        sheets = [sheets[int(i * step)] for i in range(max_images)]
        print(f"Too many contact sheets: sending {max_images} evenly spread (raise --max-images to send more).")

    out = pkg / "images"
    out.mkdir(parents=True, exist_ok=True)
    images = []
    for s in sheets:
        dest = out / s.name
        save_fitted(s, dest)
        images.append(dest)

    for_ai = read(frames / "for_ai.md")
    text = ("The source is a video. The attached images are contact sheets of its key frames "
            "(6 panels each, numbered, with their timestamp), in this order: "
            + ", ".join(f"`{p.name}`" for p in images) + ".\n"
            "Below, each key frame with what is said during that stretch "
            "([time] sheet N, panel M: text):\n\n" + for_ai)
    return images, text


# --------------------------------------------------------------------------- #
# Prompts
# --------------------------------------------------------------------------- #

def build_prompt(engine: str, mode: str, lang: str, version: str, title: str,
                 url: str, detail: str, source_text: str) -> str:
    name = ENGINES[engine][0]
    detail_line = ("Detail: high. Add an Objective box to every section, an alternative where one exists, "
                   "and a checkpoint at the end of every phase."
                   if detail == "high" else
                   "Detail: normal. Objective boxes only where a section is not obvious.")
    settings = (
        "# Task\n\n"
        f"Write a step-by-step guide to build **{title}** in **{name}** (version: {version}).\n\n"
        f"- Program (engine): {name}\n"
        f"- Input mode: {mode}\n"
        f"- Language of the guide: {lang}\n"
        f"- Source URL: {url or 'not given'}\n"
        f"- {detail_line}\n\n"
        "Follow the rules, the engine profile and the mode profile below, and fill the template. "
        "Reply with the guide only, in Markdown, starting with its frontmatter.\n"
    )
    parts = [
        settings,
        read(PROFILES / "rules.md"),
        read(PROFILES / "engines" / f"{engine}.md"),
        read(PROFILES / "modes" / f"{mode}.md"),
        "# Template\n\n```markdown\n" + read(PROFILES / "guide-template.md") + "```\n",
        "# Source material\n\n" + source_text,
    ]
    return "\n\n---\n\n".join(parts) + "\n"


def build_request(engine: str, guide: str) -> str:
    return ("# The guide\n\n" + guide + "\n\n---\n\n" + read(PROFILES / "build" / f"{engine}.md")
            + "\nThe attached images are the reference the result will be compared with.\n")


# --------------------------------------------------------------------------- #
# Estimates
# --------------------------------------------------------------------------- #

def estimate(model: dict, prompt_text: int, image_sizes: list[tuple[int, int]],
             detail: str, engine: str | None = None) -> dict:
    mult = HIGH_DETAIL if detail == "high" else 1.0
    img = sum(image_tokens(model["image_rule"], w, h) for w, h in image_sizes)
    guide_in = prompt_text + img
    guide_out = int(model["guide_out"] * mult)
    build_profile = text_tokens(read(PROFILES / "build" / f"{engine}.md")) if engine in BUILDABLE else 600
    build_in = guide_out + build_profile + img
    build_out = int(model["build_out"] * mult)
    round_cost = build_in + RENDER_TOKENS + build_out
    return {"guide": guide_in + guide_out, "guide_in": guide_in, "guide_out": guide_out,
            "build": build_in + build_out, "round": round_cost}


def task_total(est: dict, task: str) -> int:
    if task == "guide":
        return est["guide"]
    if task == "build":
        return est["guide"] + est["build"]
    return est["guide"] + est["build"] + ITERATE_ROUNDS * est["round"]


# --------------------------------------------------------------------------- #
# Interactive wizard (plain numbered menus, works in any terminal)
# --------------------------------------------------------------------------- #

def ask(title: str, options: list[tuple[str, str | None]], default: int = 1) -> int:
    """options: (label, reason it is unavailable or None). Returns the 0-based index chosen."""
    print(f"\n{title}")
    for i, (label, off) in enumerate(options, 1):
        mark = ">" if i == default else " "
        print(f" {mark} {i}) {label}" + (f"   [not available: {off}]" if off else ""))
    while True:
        try:
            raw = input(f"Choose 1-{len(options)} [{default}]: ").strip()
        except EOFError:
            raw = ""
        if not raw:
            choice = default
        elif raw.isdigit() and 1 <= int(raw) <= len(options):
            choice = int(raw)
        else:
            print("  Type one of the numbers.")
            continue
        if options[choice - 1][1]:
            print(f"  Not available: {options[choice - 1][1]}")
            continue
        return choice - 1


def yes(question: str, default: bool = True) -> bool:
    try:
        raw = input(f"{question} [{'Y/n' if default else 'y/N'}]: ").strip().lower()
    except EOFError:
        raw = ""
    return default if not raw else raw.startswith("y")


def wizard(a: argparse.Namespace, models: list[dict], image_sizes: list[tuple[int, int]],
           texts: dict[str, int], mode: str) -> tuple[dict, str, str, str]:
    """Returns (model, detail, engine, task)."""
    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    ref_text = texts["blender"]

    def model_label(m: dict) -> str:
        e = estimate(m, ref_text, image_sizes, "normal")
        how = "direct" if m["direct"] else "copy & paste"
        if m["direct"] and not has_key:
            how = "direct (needs ANTHROPIC_API_KEY)"
        note = "" if m["verified"] else " (rough estimate)"
        return f"{m['name']:<28} in ~{k(e['guide_in']):>4}  out ~{k(e['guide_out']):>4}   {how}{note}"

    mi = ask("1) Which AI?                                     input  output (guide, normal detail)",
             [(model_label(m), None) for m in models])
    model = models[mi]

    e_n = estimate(model, ref_text, image_sizes, "normal")
    e_h = estimate(model, ref_text, image_sizes, "high")
    di = ask("2) How detailed?", [
        (f"Normal   guide ~{k(e_n['guide'])}", None),
        (f"High     guide ~{k(e_h['guide'])} (more explanations, alternatives and checkpoints)", None)])
    detail = ("normal", "high")[di]

    names = list(ENGINES)
    ei = ask("3) Which program?",
             [(f"{ENGINES[n][0]:<12} guide ~{k(estimate(model, texts[n], image_sizes, detail)['guide'])}", None)
              for n in names])
    engine = names[ei]

    est = estimate(model, texts[engine], image_sizes, detail, engine)
    can_build = None
    if engine not in BUILDABLE:
        can_build = f"{ENGINES[engine][0]} can't be scripted from here"
    elif not model["direct"]:
        can_build = "needs a direct AI (Claude + API key)"
    ti = ask("4) What should the AI do?", [
        (f"Guide only{'':<41}~{k(task_total(est, 'guide'))}", None),
        (f"Guide + build it once{'':<13}+{k(est['build']):>4}  = ~{k(task_total(est, 'build'))}", can_build),
        (f"Guide + build and fix it (max {ITERATE_ROUNDS} rounds) +{k(est['round'])}/round, up to "
         f"~{k(task_total(est, 'iterate'))}", "coming soon"),
    ])
    task = TASKS[ti]

    print(f"\nSummary: {model['name']} · {ENGINES[engine][0]} · {mode} · detail {detail} · "
          f"{('guide only', 'guide + build once', 'build and fix')[ti]} · ~{k(task_total(est, task))} tokens")
    if not yes("Continue?"):
        sys.exit("Cancelled.")
    return model, detail, engine, task


# --------------------------------------------------------------------------- #
# Claude API (optional)
# --------------------------------------------------------------------------- #

def call_claude(prompt: str, images: list[Path], model: str, max_tokens: int, dest: Path) -> tuple[str, int, int]:
    try:
        import anthropic
    except ImportError:
        sys.exit("--call needs the Anthropic SDK:  pip install anthropic")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("--call needs your API key in the ANTHROPIC_API_KEY environment variable.")

    content = []
    for p in images:
        content.append({"type": "text", "text": f"Image: {p.name}"})
        content.append({"type": "image", "source": {
            "type": "base64", "media_type": "image/jpeg",
            "data": base64.standard_b64encode(p.read_bytes()).decode()}})
    content.append({"type": "text", "text": prompt})

    client = anthropic.Anthropic()
    print(f"Asking {model} (this can take a few minutes)...")
    with dest.open("w", encoding="utf-8") as f, client.messages.stream(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "user", "content": content}]) as stream:
        for chunk in stream.text_stream:
            f.write(chunk)
            print(".", end="", flush=True)
        final = stream.get_final_message()
    print()
    u = final.usage
    print(f"Written: {dest}  ({u.input_tokens:,} input + {u.output_tokens:,} output tokens)")
    if final.stop_reason == "max_tokens":
        print("WARNING: the answer was cut off at --max-tokens; raise it and run again.")
    return read(dest), u.input_tokens, u.output_tokens


# --------------------------------------------------------------------------- #
# Build once (Blender or OpenSCAD on your computer)
# --------------------------------------------------------------------------- #

def code_block(text: str, langs: tuple[str, ...]) -> str | None:
    for lang in langs:
        m = re.findall(rf"```{lang}\s*\n(.*?)```", text, flags=re.S)
        if m:
            return max(m, key=len)
    return None


def find_program(env: str, names: list[str], windows_globs: list[str]) -> str | None:
    if os.environ.get(env):
        return os.environ[env]
    for n in names:
        if shutil.which(n):
            return shutil.which(n)
    for pattern in windows_globs:
        found = sorted(glob.glob(pattern))
        if found:
            return found[-1]
    return None


def run_blender(script: Path, out: Path) -> bool:
    exe = find_program("BLENDER_PATH", ["blender"],
                       [r"C:\Program Files\Blender Foundation\Blender*\blender.exe"])
    if exe:
        cmd = [exe, "--background", "--factory-startup", "--python", str(script), "--", str(out)]
    elif subprocess.run([sys.executable, "-c", "import bpy"], capture_output=True).returncode == 0:
        cmd = [sys.executable, str(script), "--", str(out)]  # Blender as a Python module (pip install bpy)
    else:
        print("Blender not found: set BLENDER_PATH to blender.exe, or pip install bpy.")
        return False
    print("Building in Blender (this can take a minute)...")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    (out / "build_log.txt").write_text(r.stdout + "\n" + r.stderr, encoding="utf-8")
    ok = "BUILD OK" in r.stdout and (out / "render.png").exists()
    if not ok:
        print(f"The script did not finish; see {out / 'build_log.txt'}")
    return ok


def run_openscad(scad: Path, out: Path) -> bool:
    exe = find_program("OPENSCAD_PATH", ["openscad"], [r"C:\Program Files\OpenSCAD*\openscad.exe"])
    if not exe:
        print("OpenSCAD not found: install it or set OPENSCAD_PATH to openscad.exe.")
        return False
    print("Building in OpenSCAD...")
    log = ""
    for args in (["-o", str(out / "model.stl")],
                 ["-o", str(out / "render.png"), "--imgsize=960,720", "--viewall", "--autocenter"]):
        r = subprocess.run([exe, *args, str(scad)], capture_output=True, text=True, timeout=1800)
        log += r.stdout + r.stderr
    (out / "build_log.txt").write_text(log, encoding="utf-8")
    ok = (out / "render.png").exists()
    if not ok:
        print(f"OpenSCAD did not render; see {out / 'build_log.txt'}")
    return ok


def compare_image(reference: Path, render: Path, dest: Path, label: str) -> None:
    with Image.open(reference) as a, Image.open(render) as b:
        a, b = a.convert("RGB"), b.convert("RGB")
        h = 540
        a = a.resize((int(a.width * h / a.height), h))
        b = b.resize((int(b.width * h / b.height), h))
        out = Image.new("RGB", (a.width + b.width + 12, h + 40), "white")
        out.paste(a, (0, 40))
        out.paste(b, (a.width + 12, 40))
        d = ImageDraw.Draw(out)
        f = font(22)
        d.text((8, 8), "Reference", fill="black", font=f)
        d.text((a.width + 20, 8), label, fill="black", font=f)
        out.save(dest, quality=90)
    print(f"Comparison: {dest}")


def build_once(engine: str, guide: str, images: list[Path], model: str, pkg: Path,
               max_tokens: int, model_name: str) -> tuple[int, int]:
    out = pkg / "build"
    out.mkdir(exist_ok=True)
    answer_file = out / "answer.md"
    text, tin, tout = call_claude(build_request(engine, guide), images, model, max_tokens, answer_file)
    if engine == "blender":
        code = code_block(text, ("python", "py"))
        if not code:
            print("No ```python block in the answer: nothing to build.")
            return tin, tout
        script = out / "model.py"
        script.write_text(code, encoding="utf-8")
        ok = run_blender(script, out)
    else:
        code = code_block(text, ("openscad", "scad"))
        if not code:
            print("No ```openscad block in the answer: nothing to build.")
            return tin, tout
        scad = out / "model.scad"
        scad.write_text(code, encoding="utf-8")
        ok = run_openscad(scad, out)
    if ok:
        compare_image(images[-1] if len(images) > 1 else images[0], out / "render.png",
                      out / "compare.jpg", f"Built by {model_name}")
    return tin, tout


# --------------------------------------------------------------------------- #
# Parts map (image mode, local)
# --------------------------------------------------------------------------- #

def parts_from_text(text: str) -> list[dict]:
    blocks = re.findall(r"```json\s*(\{.*?\})\s*```", text, flags=re.S)
    for b in reversed(blocks):
        try:
            data = json.loads(b)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and isinstance(data.get("parts"), list):
            return data["parts"]
    return []


def draw_parts_map(image: Path, parts: list[dict], dest: Path) -> None:
    colours = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4", "#42d4f4", "#f032e6", "#9a6324"]
    with Image.open(image) as im:
        im = im.convert("RGB")
        d = ImageDraw.Draw(im)
        w, h = im.size
        f = font(max(14, w // 45))
        placed: list[tuple] = []
        for i, p in enumerate(parts):
            try:
                x0, y0, x1, y1 = (float(v) for v in p["box"])
            except (KeyError, TypeError, ValueError):
                continue
            try:
                c = colours[(int(p.get("n", i + 1)) - 1) % len(colours)]  # same part number, same colour
            except (TypeError, ValueError):
                c = colours[i % len(colours)]
            box = [x0 * w, y0 * h, x1 * w, y1 * h]
            d.rectangle(box, outline=c, width=max(2, w // 300))
            label = f" {p.get('n', i + 1)} {p.get('name', '')} "
            x, y = box[0] + 4, box[1] + 4
            tb = d.textbbox((x, y), label, font=f)
            while any(not (tb[2] < o[0] or tb[0] > o[2] or tb[3] < o[1] or tb[1] > o[3]) for o in placed):
                y += tb[3] - tb[1] + 4  # move down until it does not cover another label
                tb = d.textbbox((x, y), label, font=f)
            placed.append(tb)
            d.rectangle(tb, fill=c)
            d.text((x, y), label, fill="white", font=f)
        im.save(dest, quality=90)
    print(f"Parts map: {dest}")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main() -> None:
    p = argparse.ArgumentParser(description="Turn a video or an image into a step-by-step guide for a 3D program. "
                                            "Run without --engine for the interactive wizard.")
    p.add_argument("inputs", nargs="*", type=Path, help="A video, or one or more images of the same object")
    p.add_argument("--engine", choices=sorted(ENGINES), help="3D program (skips the wizard)")
    p.add_argument("--mode", choices=MODES, help="tutorial, showcase or image (guessed if omitted)")
    p.add_argument("-t", "--transcript", type=Path, help="Transcript of the video (SRT, VTT or copied from YouTube)")
    p.add_argument("--model", default="claude-sonnet-5-5", help="Model id from models.json (default claude-sonnet-5-5)")
    p.add_argument("--detail", choices=("normal", "high"), default="normal", help="How detailed the guide is")
    p.add_argument("--title", help="What is being built (default: the file name)")
    p.add_argument("--url", default="", help="Link to the original video or image, for the guide's frontmatter")
    p.add_argument("--lang", default="English", help="Language of the guide (default English)")
    p.add_argument("--app-version", help="Version of the program (default depends on the engine)")
    p.add_argument("-o", "--output", type=Path, help="Package folder (default output/<name>-<engine>)")
    p.add_argument("--max-images", type=int, default=30, help="Most images to send (default 30)")
    p.add_argument("--threshold", type=float, help="Scene-change threshold passed to the keyframes tool")
    p.add_argument("--max-gap", type=float,
                   help="Seconds between frames when nothing changes (showcase default: duration / 24)")
    p.add_argument("--call", action="store_true", help="Ask Claude for the guide (needs ANTHROPIC_API_KEY)")
    p.add_argument("--build", action="store_true", help="After the guide, build it once (Blender or OpenSCAD)")
    p.add_argument("--max-tokens", type=int, default=16000, help="Longest answer allowed with --call")
    p.add_argument("--parts-from", type=Path, metavar="GUIDE",
                   help="Only draw the parts map from a guide you saved (with --image)")
    p.add_argument("--image", type=Path, help="Image for --parts-from")
    a = p.parse_args()

    # Parts map only (for guides made by pasting prompt.md into a chat)
    if a.parts_from:
        if not a.image:
            sys.exit("--parts-from needs --image IMAGE")
        parts = parts_from_text(read(a.parts_from))
        if not parts:
            sys.exit("No ```json block with \"parts\" found in that guide.")
        draw_parts_map(a.image, parts, a.parts_from.with_name("parts_map.jpg"))
        return

    interactive = a.engine is None
    if interactive and not a.inputs:
        print("3D Guide Generator")
        raw = input("Video or image(s) to use (paths separated by spaces, quotes for spaces in names): ")
        import shlex
        a.inputs = [Path(x) for x in shlex.split(raw, posix=(os.name != "nt"))]
        a.inputs = [Path(str(x).strip('"')) for x in a.inputs]
    if not a.inputs:
        p.error("give an INPUT")
    for path in a.inputs:
        if not path.exists():
            sys.exit(f"Not found: {path}")
    kinds = {("image" if x.suffix.lower() in IMAGE_EXT else "video" if x.suffix.lower() in VIDEO_EXT else "?")
             for x in a.inputs}
    if "?" in kinds or len(kinds) > 1 or (kinds == {"video"} and len(a.inputs) > 1):
        sys.exit("Give either one video or one or more images (png, jpg, webp).")
    is_video = kinds == {"video"}

    models = load_models()
    by_id = {m["id"]: m for m in models}
    if a.model not in by_id:
        sys.exit(f"Unknown --model {a.model}. Known: {', '.join(by_id)}")

    # Mode
    if is_video and not a.transcript:
        a.transcript = find_transcript(a.inputs[0])
    if a.mode:
        mode = a.mode
    elif not is_video:
        mode = "image"
    elif interactive:
        print(f"\n3D Guide Generator\nInput: {a.inputs[0].name} (video"
              + (f", transcript {a.transcript.name})" if a.transcript else ", no transcript)"))
        mi = ask("0) What does the video show?", [
            ("A tutorial: every step, explained", None),
            ("Only the result: turntable, timelapse, showcase", None)], default=1 if a.transcript else 2)
        mode = ("tutorial", "showcase")[mi]
    else:
        mode = "tutorial" if a.transcript else "showcase"
    if not is_video and mode != "image":
        sys.exit("Images can only be used with --mode image.")
    if is_video and mode == "image":
        sys.exit("A video uses --mode tutorial or showcase.")

    stem = a.inputs[0].stem
    title = a.title or stem.replace("_", " ").replace("-", " ")

    # Source material first (it does not depend on the program), in a staging folder
    staging = (a.output or ROOT / "output" / f"{stem}-{a.engine or 'pending'}")
    if staging.exists() and (staging / "images").exists():
        for old in (staging / "images").glob("*.jpg"):
            old.unlink()
    staging.mkdir(parents=True, exist_ok=True)
    if is_video:
        images, source = prepare_video(a.inputs[0], a.transcript, staging, a.max_images, a.threshold, mode, a.max_gap)
    else:
        if interactive:
            print(f"\n3D Guide Generator\nInput: {', '.join(x.name for x in a.inputs)} "
                  f"({len(a.inputs)} image{'s' if len(a.inputs) > 1 else ''})")
        images, source = prepare_images(a.inputs, staging)
    image_sizes = []
    for im_path in images:
        with Image.open(im_path) as im:
            image_sizes.append(im.size)

    # Prompt text size per program (exact), for the estimates
    def prompt_for(engine: str, detail: str) -> str:
        return build_prompt(engine, mode, a.lang, a.app_version or ENGINES[engine][1], title, a.url, detail, source)
    texts = {e: text_tokens(prompt_for(e, "normal")) for e in ENGINES}

    if interactive:
        model, detail, engine, task = wizard(a, models, image_sizes, texts, mode)
        call = model["direct"]
        if call and not os.environ.get("ANTHROPIC_API_KEY"):
            print("\nNo ANTHROPIC_API_KEY found.")
            if not yes("Continue in copy-and-paste mode (no API)?"):
                sys.exit("Set ANTHROPIC_API_KEY and run again.")
            call, task = False, "guide"
    else:
        model, detail, engine = by_id[a.model], a.detail, a.engine
        task = "build" if a.build else "guide"
        call = a.call or a.build
        if task == "build" and engine not in BUILDABLE:
            sys.exit(f"--build works with {', '.join(sorted(BUILDABLE))} for now.")
        if call and not model["direct"]:
            sys.exit(f"{model['name']} can't be called from here; drop --call and paste prompt.md into its chat.")

    # Final package folder
    pkg = a.output or ROOT / "output" / f"{stem}-{engine}"
    if pkg != staging:
        if pkg.exists():
            shutil.rmtree(pkg)
        staging.rename(pkg)
        images = [pkg / "images" / im.name for im in images]

    prompt = prompt_for(engine, detail)
    (pkg / "prompt.md").write_text(prompt, encoding="utf-8")
    est = estimate(model, text_tokens(prompt), image_sizes, detail, engine)
    manifest = {
        "engine": engine, "mode": mode, "title": title, "language": a.lang,
        "app_version": a.app_version or ENGINES[engine][1], "detail": detail,
        "model": model["name"], "task": task,
        "inputs": [x.name for x in a.inputs], "images": [x.name for x in images],
        "estimate": {"guide": est["guide"], "guide_input": est["guide_in"], "guide_output": est["guide_out"],
                     "build_once": est["build"], "per_fix_round": est["round"],
                     "total_for_task": task_total(est, task), "rough": not model["verified"]},
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (pkg / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nPackage ready: {pkg}")
    print(f"  {model['name']} · {ENGINES[engine][0]} · {mode} · {len(images)} image(s) · "
          f"estimated ~{k(task_total(est, task))} tokens")

    if not call:
        print(f"\nNext: attach the files in images/ (in order) and paste prompt.md into {model['name']}.")
        if mode == "image":
            print("Save the answer as guide.md, then draw the parts map with:")
            print(f'  python guidegen.py --parts-from "{pkg / "guide.md"}" --image "{images[0]}"')
        return

    max_tokens = int(a.max_tokens * (HIGH_DETAIL if detail == "high" else 1))
    guide_path = pkg / "guide.md"
    guide, tin, tout = call_claude(prompt, images, model["id"], max_tokens, guide_path)
    used_in, used_out = tin, tout
    if mode == "image":
        parts = parts_from_text(guide)
        if parts:
            draw_parts_map(images[0], parts, pkg / "parts_map.jpg")
        else:
            print("No parts list found in the answer: no parts map drawn.")

    if task == "build":
        bin_, bout = build_once(engine, guide, images, model["id"], pkg, max_tokens, model["name"])
        used_in += bin_
        used_out += bout

    total = used_in + used_out
    print(f"\nTokens used: {used_in:,} input + {used_out:,} output = {total:,} "
          f"(estimated ~{task_total(est, task):,})")
    manifest["used"] = {"input": used_in, "output": used_out, "total": total}
    (pkg / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
