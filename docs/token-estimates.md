# Token estimates

How much it costs to hand a video tutorial to an AI, depending on how many frames you send and how.

All numbers are **approximate** and for Claude. Other models count images differently. To get an exact number, use your provider's token-counting tool or look at the usage report after a request.

## How images are counted (Claude)

- An image costs about **one token per 28 × 28 px patch**: `ceil(width / 28) × ceil(height / 28)`. The older rule of thumb `width × height / 750` gives almost the same result.
- Images larger than the model's limit are **scaled down first**, so a bigger image does not always cost more:

| Model tier | Max long edge | Max tokens per image |
|---|---|---|
| Standard (most models) | 1568 px | 1568 |
| High resolution (newer models, check the docs) | 2576 px | 4784 |

- Text: roughly **4 characters per token** in English (Spanish and other languages use a bit more).

Source: Claude docs, *Vision* and *Vision coordinates* pages.

## Cost per image

| Image | Size | Standard tier | High-res tier |
|---|---|---|---|
| Frame from a 360p video | 640 × 360 | 299 | 299 |
| Frame from a 480p video | 854 × 480 | 558 | 558 |
| Frame at the tool's default width | 1280 × 720 | 1,196 | 1,196 |
| Full HD frame | 1920 × 1080 | 1,560 (scaled down) | 2,691 |
| Contact sheet, 6 frames (3 × 2) | 1920 × 720 | 1,176 (scaled down) | 1,794 |

`keyframes.py` prints these estimates for every video it processes.

## Measured example

A 25-minute Blender tutorial (a slime character, modelling + animation + Unreal), processed with the default settings:

| | |
|---|---|
| Duration | 25:03 |
| Key frames kept | 124 (78 scene changes, 45 fillers, 1 start), about **5 per minute** |
| Contact sheets | 21 (6 frames each, 1920 × 720) |
| Transcript | about 3,700 words, about 6k tokens |

Blender tutorials change slowly on screen, so 4-6 frames per minute is typical with the default `--threshold 0.12`. Fast-cut videos produce more; `--threshold 0.08` also produces more.

## Estimate per video length

Assuming ~5 frames per minute, ~150 spoken words per minute and 6 frames per sheet:

| Video | Frames | Sheets | Text (`for_ai.md`) | Sheets, standard | Sheets, high-res | All frames at 1280 px |
|---|---|---|---|---|---|---|
| 10 min | ~50 | 9 | ~3k | ~11k | ~16k | ~60k |
| 25 min | ~125 | 21 | ~8k | ~25k | ~38k | ~150k |
| 60 min | ~300 | 50 | ~19k | ~59k | ~90k | ~360k |

**Recommended input** (text + all sheets): about **14k / 33k / 78k** tokens on the standard tier, **19k / 46k / 109k** on the high-res tier.

Then add:
- **The guide the AI writes** (output tokens): a detailed guide for a 25-minute video is around 10-15k tokens.
- **Working overhead**: reading the vault rules and templates (~5-8k), checking your `.blend` (~1-3k per check), and your conversation. In an agent session the conversation is re-read on every step, so a long session costs several times the numbers above; prompt caching makes the repeated part much cheaper.

## The generator's own text

`guidegen.py` sends the rules, the program profile, the mode profile and the template with every request: about **2-2.5k tokens** of text on top of the source material. It prints the estimate for each package and saves it in `manifest.json`.

## Image mode

| Input | Images | Approx. input |
|---|---|---|
| One image | 1 (≤ 1,568 tokens, or up to 4,784 on high-res models) | ~4-7k |
| Three views of the same object | 3 | ~7-17k |

Plus 6-15k output tokens for the guide. More views make proportions and hidden sides much more reliable, so for important models 2-3 views are worth it.

## Per AI (what the wizard shows)

`guidegen.py` estimates each choice before running, with the numbers in `models.json`:

- **Input** = the prompt text (measured) + the images, counted with each provider's rule: Claude 28 px patches (above), OpenAI tiles (85 + 170 per 512 px tile after resizing), Gemini 258 tokens per 768 px tile. The OpenAI and Gemini rules are documented approximations and are marked "rough estimate".
- **Output** = the usual length of a guide for that model (`guide_out`), × 1.5 at high detail.
- **Build once** = the guide + the build instructions + the images in, a script out (`build_out`).
- **Each fix round** (coming soon) = a build plus a render of the result sent back (~1.2k).

After a direct run it prints the real usage next to the estimate; edit `models.json` if your numbers keep differing.

## Ways to send the video

| Option | What you send | 25 min, approx. | Good for |
|---|---|---|---|
| A. Text only | Transcript | ~6-8k | Talky tutorials, or a first draft |
| B. Text + sheets *(default)* | `for_ai.md` + `sheets/` | ~33-46k | Full guide that knows what is on screen |
| C. Text + selected frames | `for_ai.md` + 10-20 full frames for the visual parts | ~20-30k | Cheaper than B, sharper images where it matters |
| D. All full frames | Every frame | ~150k | Rarely worth it |
| E. One stretch | The frames and text of a few minutes | ~3-8k | "I'm stuck at 11:30" |

Notes:
- **Low-resolution source videos** (360p, 480p): sending the individual frames costs about the same as the sheets and each image is sharper. Use C or even D.
- **Contact sheets lose detail.** On the standard tier a 1920 px sheet is scaled to 1568 px, so each panel is about 520 px wide: good for "what is happening", not for reading small menu text. Send the full frame for those moments.
- **Long videos**: process one chapter at a time instead of the whole video in one request.
- **OCR** (`--ocr`) adds on-screen text to `for_ai.md` for a few hundred tokens and can replace some images.
