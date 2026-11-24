# text-eye

An animated eye made entirely of text characters, built with Python and pygame. A pencil sketch is converted into a grid of ink values, drawn as characters (dense symbols for dark pencil, blank for paper), and given a blinking animation.

![https://www.pinterest.com/pin/1132866481307581828/](screenshot.png)

## How it works

1. **Load the sketch** and shrink it to a grid of brightness values.
2. **Stretch the contrast** so the paper becomes blank and only the pencil strokes remain.
3. **Map each cell to a character** from `" .:+*%#@"`, denser for darker areas, and pre-render the result to a single surface.
4. **Blink** using a small state machine (`waiting`, `closing`, `opening`) that outputs an "openness" value between 0 and 1.
5. **Scale to the screen.** The window is 3/4 of the desktop size, and the grid is rebuilt to fit it.

## Run it

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python eye.py
```

On macOS or Linux, activate with `source .venv/bin/activate` instead.

## Controls

| Key | Action |
| --- | --- |
| Space | Blink |
| F | Fullscreen |
| Esc | Quit |

## Roadmap

- Split the picture into layers so only the eye blinks
- A separate hair layer that stays in front
- Colour palettes
- Real words instead of single characters

## Credits

Inspired by an Instagram video of an eye made from code[just.tanya23]. The sketch used for development is by [emarillo_art]. Please do not reuse it without their permission.