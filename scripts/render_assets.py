"""Render the GitHub profile banner and social preview in the logachev.net style.

Palette and metaphor mirror the site: a dark dispatch room where steel particles are
the data stream, lime is the agent working inside its bounds, and the white flash is
the human decision.
"""
from __future__ import annotations

from pathlib import Path
from random import Random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)

BG = (5, 7, 10)
BG2 = (9, 13, 18)
FG = (233, 238, 242)
MUTED = (143, 154, 163)
LIME = (195, 244, 81)
STEEL = (127, 153, 173)
HAIR = (233, 238, 242, 26)

FONTS = Path(__file__).resolve().parent / "fonts"
BOLD = FONTS / "Onest-Bold.ttf"
MEDIUM = FONTS / "Onest-Medium.ttf"
MONO = Path("C:/Windows/Fonts/consola.ttf")

SS = 3  # supersampling factor, downscaled at the end


def font(path: Path, size: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=int(size * SS))


class Canvas:
    """Drawing surface in logical units; everything is scaled by SS internally."""

    def __init__(self, width: int, height: int) -> None:
        self.w, self.h = width, height
        self.im = Image.new("RGBA", (width * SS, height * SS), BG + (255,))
        self.glow = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        self._background()

    def _background(self) -> None:
        d = ImageDraw.Draw(self.im)
        for y in range(self.h * SS):
            t = y / (self.h * SS)
            c = tuple(int(BG[i] + (BG2[i] - BG[i]) * t) for i in range(3))
            d.line((0, y, self.w * SS, y), fill=c + (255,))

    def p(self, v: float) -> int:
        return int(v * SS)

    def layer(self) -> tuple[Image.Image, ImageDraw.ImageDraw]:
        im = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        return im, ImageDraw.Draw(im)

    def paste(self, layer: Image.Image) -> None:
        self.im = Image.alpha_composite(self.im, layer)

    def hline(self, x0: float, x1: float, y: float, fill=HAIR, width: float = 1) -> None:
        layer, d = self.layer()
        d.line((self.p(x0), self.p(y), self.p(x1), self.p(y)), fill=fill, width=max(1, self.p(width)))
        self.paste(layer)

    def text(self, xy, text: str, face: ImageFont.FreeTypeFont, fill, spacing: float = 0, anchor: str = "ls") -> None:
        layer, d = self.layer()
        x, y = self.p(xy[0]), self.p(xy[1])
        if spacing:
            for ch in text:
                d.text((x, y), ch, font=face, fill=fill, anchor=anchor)
                x += int(d.textlength(ch, font=face)) + self.p(spacing)
        else:
            d.text((x, y), text, font=face, fill=fill, anchor=anchor)
        self.paste(layer)

    def text_width(self, text: str, face: ImageFont.FreeTypeFont, spacing: float = 0) -> float:
        d = ImageDraw.Draw(self.im)
        return (sum(d.textlength(ch, font=face) + self.p(spacing) for ch in text) if spacing else d.textlength(text, font=face)) / SS

    def dot(self, x: float, y: float, r: float, fill, alpha: int = 255, glow: float = 0) -> None:
        if glow:
            g, gd = self.layer()
            gr = self.p(r + glow)
            gd.ellipse((self.p(x) - gr, self.p(y) - gr, self.p(x) + gr, self.p(y) + gr), fill=fill + (int(alpha * 0.9),))
            g = g.filter(ImageFilter.GaussianBlur(self.p(glow * 0.7)))
            self.paste(g)
        layer, d = self.layer()
        rr = self.p(r)
        d.ellipse((self.p(x) - rr, self.p(y) - rr, self.p(x) + rr, self.p(y) + rr), fill=fill + (alpha,))
        self.paste(layer)

    def finish(self, size: tuple[int, int], dest: Path) -> None:
        out = self.im.convert("RGB").resize(size, Image.LANCZOS)
        out.save(dest, optimize=True)


def flow(c: Canvas, x0: float, x1: float, cy: float, height: float, unit: float, labels: bool = True) -> None:
    """Data stream -> bounded agent -> human decision."""
    rng = Random(2026)
    span = x1 - x0
    gate0 = x0 + span * 0.36
    gate1 = x0 + span * 0.70
    end = x0 + span * 0.96

    # inbound steel stream converging into the agent boundary
    layer, d = c.layer()
    d.line((c.p(x0), c.p(cy), c.p(gate0), c.p(cy)), fill=STEEL + (70,), width=max(1, c.p(1.2 * unit)))
    c.paste(layer)
    for _ in range(int(150 * unit * unit)):
        t = rng.random() ** 0.8
        x = x0 + (gate0 - x0) * t
        spread = height * 0.5 * (1 - t) ** 1.4 + 1.5 * unit
        y = cy + rng.uniform(-spread, spread)
        a = int(60 + 150 * t)
        c.dot(x, y, rng.uniform(0.9, 2.1) * unit, STEEL, a)

    # agent boundary, lime
    bh = height * 0.62
    layer, d = c.layer()
    box = (c.p(gate0), c.p(cy - bh / 2), c.p(gate1), c.p(cy + bh / 2))
    d.rounded_rectangle(box, radius=c.p(8 * unit), fill=LIME + (14,), outline=LIME + (190,), width=max(1, c.p(1.6 * unit)))
    c.paste(layer)
    for i in range(7):
        t = (i + 0.5) / 7
        x = gate0 + (gate1 - gate0) * t
        y = cy + (rng.random() - 0.5) * bh * 0.55 * (1 - abs(t - 0.5))
        c.dot(x, y, 2.4 * unit, LIME, 235, glow=4 * unit)

    # single verified output line to the human decision
    layer, d = c.layer()
    d.line((c.p(gate1), c.p(cy), c.p(end), c.p(cy)), fill=LIME + (200,), width=max(1, c.p(1.8 * unit)))
    c.paste(layer)
    for i in range(4):
        c.dot(gate1 + (end - gate1) * (i + 0.6) / 4.6, cy, 1.8 * unit, LIME, 220)

    # human decision: white flash
    c.dot(end, cy, 5.5 * unit, FG, 255, glow=14 * unit)

    if labels:
        face = font(MONO, 12 * unit)
        y = cy + bh / 2 + 30 * unit
        c.text((x0, y), "ПОТОК ДАННЫХ", face, STEEL, spacing=1.6 * unit)
        c.text((gate0, y), "АГЕНТ В ГРАНИЦАХ", face, LIME, spacing=1.6 * unit)
        label = "РЕШЕНИЕ ЧЕЛОВЕКА"
        c.text((end - c.text_width(label, face, 1.6 * unit) + 14 * unit, y), label, face, FG, spacing=1.6 * unit)


def render_banner() -> None:
    c = Canvas(1600, 400)
    c.hline(92, 1508, 64)
    c.hline(92, 1508, 322)

    mono = font(MONO, 17)
    c.text((94, 46), "ПАВЕЛ ЛОГАЧЕВ / ВНЕДРЕНИЕ ИИ-АГЕНТОВ", mono, MUTED, spacing=2.2)
    big = font(BOLD, 76)
    c.text((90, 168), "Агент готовит", big, FG)
    c.text((90, 252), "Человек решает", big, LIME)

    flow(c, 800, 1500, 176, 190, 1.0)

    mono_s = font(MONO, 15)
    c.text((94, 358), "LOCAL-FIRST", mono_s, FG, spacing=2.2)
    c.text((300, 358), "ИИ-АВТОМАТИЗАЦИЯ", mono_s, FG, spacing=2.2)
    c.text((548, 358), "ВНУТРЕННИЕ ИНСТРУМЕНТЫ", mono_s, FG, spacing=2.2)
    note = "LOGACHEV.NET"
    c.text((1508 - c.text_width(note, mono_s, 2.2), 358), note, mono_s, LIME, spacing=2.2)
    c.finish((2400, 600), OUT / "profile-banner.png")


def render_social() -> None:
    c = Canvas(1280, 640)
    c.hline(80, 1200, 84)
    c.hline(80, 1200, 548)

    mono = font(MONO, 18)
    c.text((82, 62), "ПАВЕЛ ЛОГАЧЕВ / ВНЕДРЕНИЕ ИИ-АГЕНТОВ", mono, MUTED, spacing=2.4)
    big = font(BOLD, 92)
    c.text((78, 222), "Агент готовит", big, FG)
    c.text((78, 324), "Человек решает", big, LIME)

    medium = font(MEDIUM, 25)
    c.text((82, 392), "Внедряю ИИ-агентов под задачи бизнеса:", medium, MUTED)
    c.text((82, 426), "заявки, расчёты, документы, отчёты.", medium, MUTED)

    flow(c, 80, 1200, 490, 90, 1.0, labels=False)
    mono_s = font(MONO, 16)
    c.text((82, 592), "LOCAL-FIRST", mono_s, FG, spacing=2.2)
    c.text((290, 592), "ИИ-АВТОМАТИЗАЦИЯ", mono_s, FG, spacing=2.2)
    c.text((560, 592), "ВНУТРЕННИЕ ИНСТРУМЕНТЫ", mono_s, FG, spacing=2.2)
    note = "LOGACHEV.NET"
    c.text((1200 - c.text_width(note, mono_s, 2.2), 592), note, mono_s, LIME, spacing=2.2)
    c.finish((1280, 640), OUT / "social-preview.png")


if __name__ == "__main__":
    render_banner()
    render_social()
    print("Rendered profile-banner.png and social-preview.png")
