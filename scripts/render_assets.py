from __future__ import annotations

from pathlib import Path
from random import Random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#10243A"
PAPER = "#F1EFE8"
COBALT = "#3558D7"
RED = "#D95A43"
MUTED = "#4F5E6E"
HAIR = "#CBD0D2"
WHITE = "#F9F8F4"

FONT_DIR = Path("C:/Windows/Fonts")
SANS = FONT_DIR / "bahnschrift.ttf"
SERIF = FONT_DIR / "georgia.ttf"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def noise_layer(size: tuple[int, int], opacity: int = 8) -> Image.Image:
    rng = Random(2417)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    px = layer.load()
    for y in range(size[1]):
        for x in range(size[0]):
            n = rng.randrange(0, opacity + 1)
            px[x, y] = (16, 36, 58, n)
    return layer.filter(ImageFilter.GaussianBlur(0.25))


def tracking(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, face: ImageFont.FreeTypeFont, fill: str, spacing: int) -> None:
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=face, fill=fill)
        x += int(draw.textlength(char, font=face)) + spacing


def line(draw: ImageDraw.ImageDraw, points: list[tuple[int, int]], fill: str, width: int = 2) -> None:
    draw.line(points, fill=fill, width=width, joint="curve")


def route_graph(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], scale: float = 1.0) -> None:
    x0, y0, x1, y1 = box
    cy = (y0 + y1) // 2
    points = [
        (x0, cy),
        (x0 + int(122 * scale), cy),
        (x0 + int(196 * scale), y0 + int(52 * scale)),
        (x0 + int(302 * scale), y0 + int(52 * scale)),
        (x0 + int(376 * scale), cy),
        (x1, cy),
    ]
    line(draw, points, COBALT, max(3, int(4 * scale)))

    nodes = [
        (points[0][0], points[0][1], "01", INK),
        (points[2][0], points[2][1], "02", COBALT),
        (points[3][0], points[3][1], "03", RED),
        (points[-1][0], points[-1][1], "04", INK),
    ]
    small = font(SANS, max(15, int(17 * scale)))
    for x, y, label, color in nodes:
        r = max(8, int(11 * scale))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=WHITE, outline=color, width=max(2, int(3 * scale)))
        draw.text((x - int(10 * scale), y + int(18 * scale)), label, font=small, fill=color)

    red_x, red_y = points[3]
    draw.rectangle(
        (red_x - int(22 * scale), red_y - int(52 * scale), red_x + int(22 * scale), red_y - int(28 * scale)),
        fill=RED,
    )


def render_banner() -> None:
    size = (1600, 400)
    im = Image.new("RGB", size, PAPER)
    draw = ImageDraw.Draw(im)

    draw.rectangle((0, 0, 22, size[1]), fill=COBALT)
    draw.rectangle((22, 0, 28, size[1]), fill=RED)
    draw.line((92, 64, 1508, 64), fill=HAIR, width=2)
    draw.line((92, 322, 1508, 322), fill=HAIR, width=2)

    tracking(draw, (94, 27), "PAVEL LOGACHEV / PRODUCT ENGINEERING", font(SANS, 19), MUTED, 2)
    draw.text((92, 92), "Pavel", font=font(SERIF, 64), fill=INK)
    draw.text((92, 158), "Logachev", font=font(SERIF, 64), fill=INK)
    draw.text((96, 252), "CONTEXT / SOFTWARE / RELEASE", font=font(SANS, 24), fill=COBALT)

    route_graph(draw, (866, 96, 1460, 286), 1.0)
    tracking(draw, (94, 348), "LOCAL-FIRST", font(SANS, 17), INK, 2)
    tracking(draw, (392, 348), "AI AUTOMATION", font(SANS, 17), INK, 2)
    tracking(draw, (752, 348), "INTERNAL TOOLS", font(SANS, 17), INK, 2)
    tracking(draw, (1155, 348), "MOSCOW / 2026", font(SANS, 17), MUTED, 2)

    im = Image.alpha_composite(im.convert("RGBA"), noise_layer(size)).convert("RGB")
    im.save(OUT / "profile-banner.png", optimize=True, quality=94)


def render_social() -> None:
    size = (1280, 640)
    im = Image.new("RGB", size, PAPER)
    draw = ImageDraw.Draw(im)

    draw.rectangle((0, 0, 26, size[1]), fill=COBALT)
    draw.rectangle((26, 0, 34, size[1]), fill=RED)
    draw.line((94, 82, 1186, 82), fill=HAIR, width=2)
    draw.line((94, 532, 1186, 532), fill=HAIR, width=2)

    tracking(draw, (96, 38), "PRODUCT ENGINEERING / MOSCOW", font(SANS, 18), MUTED, 2)
    draw.text((92, 132), "Pavel", font=font(SERIF, 86), fill=INK)
    draw.text((92, 220), "Logachev", font=font(SERIF, 86), fill=INK)
    draw.text((98, 340), "Digital products and practical automation", font=font(SANS, 28), fill=COBALT)
    route_graph(draw, (652, 188, 1138, 430), 0.82)

    tracking(draw, (96, 566), "CONTEXT", font(SANS, 16), INK, 2)
    tracking(draw, (336, 566), "BUILD", font(SANS, 16), INK, 2)
    tracking(draw, (544, 566), "VERIFY", font(SANS, 16), INK, 2)
    tracking(draw, (784, 566), "RELEASE", font(SANS, 16), INK, 2)
    tracking(draw, (1038, 566), "LOGACHEV.NET", font(SANS, 16), MUTED, 1)

    im = Image.alpha_composite(im.convert("RGBA"), noise_layer(size)).convert("RGB")
    im.save(OUT / "social-preview.png", optimize=True, quality=94)


if __name__ == "__main__":
    render_banner()
    render_social()
    print("Rendered profile-banner.png and social-preview.png")
