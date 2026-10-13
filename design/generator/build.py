"""Генератор картинок GitHub-аккаунта pavel-logachev: баннеры, карточки профиля, соцпревью, схемы.

Запуск (из любого каталога; пути к шаблонам, шрифтам и скриншотам — относительно этого файла):
    python design/generator/build.py                         # 33 PNG в design/generator/out/
    python design/generator/build.py --out ../assets          # другой каталог вывода
    python design/generator/build.py --only pora             # только файлы, в имени которых есть «pora»
    python design/generator/build.py --preview               # + превью README (см. ниже)

Что нужно: Python 3.10+ с Pillow и PyYAML; Playwright CLI с именованными сессиями
(`<cli> -s=<сессия> run-code --filename=<js>`). Путь к CLI: --playwright, иначе переменная
окружения PLAYWRIGHT_CLI, иначе обёртка DeepSeek Harness (DEFAULT_PW). Сессия: --session (ghdesign).
Для --preview дополнительно нужен `gh` с авторизацией (рендер через GitHub Markdown API).

Входы: texts.yaml — все строки на картинках; templates/*.css — оформление; sources/*.png —
реальные скриншоты приложений; fonts/ — Onest и JetBrains Mono (SIL OFL 1.1, тексты лицензий
лежат рядом: fonts/*-OFL.txt; шрифты встраиваются в HTML на время рендера, в PNG попадают растром).

Выход: <out>/<репозиторий>/... повторяет пути в репозиториях: pavel-logachev/assets/*.png,
<repo>/docs/assets/*.png. Десктопные картинки рендерятся в 2×, мобильные (*-mobile.png,
для <picture media="(max-width: 767px)">) — в 1,5× от ширины 720, соцпревью — 1280×640.
Сборка падает (код 1), если текст обрезан, вылез за рамку, зоны наложились или кегль при показе
меньше 11 px (моно — 10 px). PNG > 500 КБ квантуются Pillow.

Превью (--preview): для каждого <out>/<repo>/README.md, если он есть, рендер через
`gh api markdown` в обёртке github-markdown-css (templates/github-markdown-*.css, MIT) при ширине
1012 px (профиль) или 830 px (репозиторий) и 390 px, светлая и тёмная тема -> --preview-dir
(по умолчанию design/generator/preview/), плюс нарезка tiles/ по 1800 px.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from PIL import Image

GEN = Path(__file__).resolve().parent
SRC = GEN / "sources"
TPL = GEN / "templates"
DEFAULT_PW = r"C:\Users\pavel\Documents\DeepSeekHarness\tools\playwright\playwright-dsh.cmd"
# Заполняются в main() из аргументов командной строки.
OUT = GEN / "out"
PREVIEW = GEN / "preview"
BUILD: Path = Path()
PW = DEFAULT_PW
SESSION = "ghdesign"
MAX_BYTES = 500 * 1024
DESK_CHECK = 760                            # минимальная ширина показа десктопного варианта
MOB_CHECK = 340                             # ширина колонки README на телефоне 390 px
MIN_PX = 11.0                               # минимальный кегль текста на экране, CSS px
MIN_PX_MONO = 10.0                          # для моноширинных капс-меток

T = yaml.safe_load((GEN / "texts.yaml").read_text(encoding="utf-8"))
OWNER = T["owner"]
REPOS = ["ai-tender-radar", "stock-configurator", "dsh-mobile", "voice-input", "pora"]


def e(s: str) -> str:
    return html.escape(str(s), quote=True)


def furl(p: Path) -> str:
    return p.resolve().as_uri()


# ---------------------------------------------------------------- общие фрагменты
ARROW_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg>')


# Знак перехода в верхней строке десктопной карточки: стоит рядом с адресом и не перекрывает скриншот.
GO = f'<span class="go">{ARROW_SVG}</span>'


def top_slug(repo: str, go: bool = False) -> str:
    return (f'<div class="top" data-zone="top"><span class="mark"></span>'
            f'<span class="slug">{e(OWNER)} / <b>{e(repo)}</b></span>{GO if go else ""}</div>')


def meta_line(text: str) -> str:
    """Нижняя строка карточки: платформа, стек и лицензия (или статус закрытого проекта)."""
    return f'<div class="cmeta" data-zone="meta">{e(text)}</div>'


def synth_tag(key: str = "synthetic_label") -> str:
    return f'<div class="synth-tag" data-zone="synth">{e(T[key])}</div>'


def card_text(c: dict) -> str:
    """Заголовок карточки и плашка с типом решения."""
    return (f'<div class="txt" data-zone="txt"><p class="line">{e(c["line"])}</p>'
            f'<div class="kind"><span class="dot"></span>{e(c["kind"])}</div></div>')


def byline() -> str:
    """Подпись автора на баннерах и соцпревью репозиториев."""
    return f'<div class="byline" data-zone="by">{e(T["byline"])}</div>'


def top_url(url: str, go: bool = False) -> str:
    """Верхняя строка карточки проекта без репозитория: адрес сайта вместо «владелец / репозиторий»."""
    host, _, rest = url.partition("/")
    inner = f'{e(host)}/<b>{e(rest)}</b>' if rest else f'<b>{e(host)}</b>'
    return (f'<div class="top" data-zone="top"><span class="mark"></span><span class="slug">{inner}</span>'
            f'{GO if go else ""}</div>')


def phone(src: str, left: float, top: float, width: float, rot: float = 0, z: int = 1, extra: str = "") -> str:
    return (f'<div class="phone" style="left:{left}px;top:{top}px;width:{width}px;'
            f'transform:rotate({rot}deg);z-index:{z};{extra}"><img src="{furl(SRC / src)}"></div>')


def window(src: str, left: float, top: float, width: float, z: int = 1) -> str:
    return (f'<div class="window" style="left:{left}px;top:{top}px;width:{width}px;z-index:{z}">'
            f'<img src="{furl(SRC / src)}"></div>')


def tg_bubble(c: dict, kb: bool) -> str:
    q = "".join(f"<p>• {e(x)}</p>" for x in c["questions"])
    out = f"""
<div class="tg-bubble">
  <p><b>{e(c['grade'])}</b> · {e(c['customer'])}</p>
  <p>{e(c['one_line'])}</p>
  <div class="gap"></div>
  <p><b>{e(c['what_label'])}</b> {e(c['what'])}</p>
  <p><b>{e(c['deadline_label'])}</b> {e(c['deadline'])}</p>
  <p><b>{e(c['economics_label'])}</b> {e(c['economics'])}</p>
  <div class="gap"></div>
  <p><b>{e(c['contacts_label'])}</b></p>
  <p>• {e(c['contact_name'])} — {e(c['contact_role'])}</p>
  <p class="ind">☎ {e(c['contact_phone'])}</p>
  <div class="gap"></div>
  <p><b>{e(c['opening_label'])}</b> {e(c['opening'])}</p>
  <div class="gap"></div>
  <p><b>{e(c['questions_label'])}</b></p>
  {q}
  <div class="gap"></div>
  <p><a>{e(c['link'])}</a></p>
  <div class="tg-time">{e(c['time'])}</div>
</div>"""
    if kb:
        out += '<div class="tg-kb">' + "".join(f"<div>{e(b)}</div>" for b in c["buttons"]) + "</div>"
    return out


def xl_sheet(s: dict) -> str:
    cols = len(s["headers"])
    letters = "".join(f"<td>{chr(65 + i)}</td>" for i in range(cols))
    spans = [3, 3, 2]
    meta_l = "".join(f'<td colspan="{spans[i]}">{e(k)}</td>' for i, (k, _) in enumerate(s["meta"]))
    meta_v = "".join(f'<td colspan="{spans[i]}">{e(v)}</td>' for i, (_, v) in enumerate(s["meta"]))
    head = "".join(f"<td>{e(h)}</td>" for h in s["headers"])
    num_cols = {3, 4, 6}
    rows = "".join("<tr>" + "".join(
        f'<td class="{"num" if i in num_cols else ""}">{e(v)}</td>' for i, v in enumerate(r)) + "</tr>" for r in s["rows"])
    checks = "".join(f'<tr class="check"><td colspan="{cols}">□ {e(x)}</td></tr>' for x in s["checks"])
    tabs = "".join(f'<div class="{"on" if i == 0 else ""}">{e(t)}</div>' for i, t in enumerate(s["tabs"]))
    return f"""
<div class="xl" style="position:absolute;left:0;top:22px;width:820px;zoom:.7317">
  <div class="xl-bar"><i></i><i></i><i></i><span>{e(s['file'])}</span></div>
  <table>
    <tr class="colh">{letters}</tr>
    <tr class="title"><td colspan="{cols}">{e(s['title'])}</td></tr>
    <tr class="meta">{meta_l}</tr>
    <tr class="metav">{meta_v}</tr>
    <tr class="total"><td colspan="{cols - 2}">{e(s['total_label'])}</td><td colspan="2" class="num">{e(s['total'])}</td></tr>
    <tr class="sect"><td colspan="{cols}">{e(s['section'])}</td></tr>
    <tr class="head">{head}</tr>
    {rows}
    <tr class="review"><td colspan="{cols}">{e(s['checks_label'])}</td></tr>
    {checks}
  </table>
  <div class="xl-tabs">{tabs}</div>
</div>"""


def pill(src: str, left: float, top: float, width: float, z: int, bbox=(86, 75, 610, 168)) -> str:
    x0, y0, x1, y1 = bbox
    k = width / (x1 - x0)
    h = (y1 - y0) * k
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{h:.1f}px;'
            f'border-radius:{22 * k:.1f}px;overflow:hidden;z-index:{z};'
            f'box-shadow:0 0 0 1px rgba(233,238,242,.14),0 18px 40px rgba(0,0,0,.6)">'
            f'<img src="{furl(SRC / src)}" style="position:absolute;left:{-x0 * k:.1f}px;top:{-y0 * k:.1f}px;'
            f'width:{696 * k:.1f}px;max-width:none"></div>')


def vis(repo: str, card: bool = False) -> str:
    """Визуальная зона 600×420 с реальными скриншотами (или синтетическим макетом).
    card=True — вариант для карточки профиля, если он отличается от баннера репозитория."""
    glow = {"ai-tender-radar": "#6ab3f3", "stock-configurator": "#3fae6a", "dsh-mobile": "#c3f451",
            "voice-input": "#8b7cff", "pora": "#2f8f6b", "resnichki": "#d6a66a", "fund-portal": "#3b6fd1"}[repo]
    g = f'<div class="vglow" style="background:{glow}"></div>'
    if repo == "ai-tender-radar":
        body = (f'<div class="tg" style="position:absolute;left:64px;top:16px;width:476px;height:560px;'
                f'border-radius:16px;box-shadow:0 0 0 1px rgba(233,238,242,.16),0 30px 60px rgba(0,0,0,.55)">'
                f'{tg_bubble(T["tender_card"], kb=False)}</div>')
    elif repo == "stock-configurator":
        body = xl_sheet(T["stock_sheet"])
    elif repo == "dsh-mobile":
        s = T["dsh_screens"]
        body = (phone(s[1]["file"], 30, 70, 186, -7, 1) + phone(s[2]["file"], 384, 70, 186, 7, 1)
                + phone(s[0]["file"], 196, 22, 208, 0, 2))
    elif repo == "voice-input" and card:
        # в карточке — только оверлей в трёх состояниях, крупно; окно настроек остаётся в баннере репозитория
        body = (pill("voice-listening.png", 40, 36, 400, 3)
                + pill("voice-processing.png", 100, 150, 400, 3)
                + pill("voice-success.png", 160, 264, 400, 3, (86, 73, 610, 159)))
    elif repo == "voice-input":
        body = ('<div class="window" style="left:292px;top:14px;width:296px">'
                f'<img src="{furl(SRC / "voice-settings.png")}"></div>'
                + pill("voice-listening.png", 0, 92, 352, 3)
                + pill("voice-processing.png", 26, 184, 352, 3)
                + pill("voice-success.png", 52, 276, 352, 3, (86, 73, 610, 159)))
    elif repo == "pora":
        body = (phone("pora-history.png", 30, 70, 186, -7, 1) + phone("pora-today-dark.png", 384, 70, 186, 7, 1)
                + phone("pora-today.png", 196, 22, 208, 0, 2))
    elif repo == "resnichki":
        # главная студии (десктоп) и страница курса (телефон), снимки resnichki.moscow
        body = (window("resnichki-home.jpg", 0, 34, 470, 1)
                + phone("resnichki-kurs-mobile.jpg", 398, 64, 178, 5, 2))
    elif repo == "fund-portal":
        # кабинет оргкомитета (пилот) и кабинет предприятия (прототип), демонстрационные данные
        body = (window("fund-orgcommittee-dashboard.png", 0, 16, 470, 1)
                + window("fund-enterprise-work.png", 124, 148, 470, 2))
    else:
        raise KeyError(repo)
    return g + body


def viswrap(repo: str, left: float, top: float, z: float, flow: bool = False, crop_h: float | None = None,
            card: bool = False) -> str:
    w, h = 600 * z, (crop_h if crop_h else 420 * z)
    pos = "" if flow else f"left:{left}px;top:{top}px;"
    ov = "overflow:hidden;" if flow else ""
    return (f'<div class="viswrap" data-zone="vis" style="{pos}width:{w:.1f}px;height:{h:.1f}px;{ov}">'
            f'<div class="vis" data-illus="1" style="zoom:{z}">{vis(repo, card)}</div></div>')


def product_text(repo: str, mobile: bool = False) -> str:
    p = T["products"][repo]
    sub = "".join(f'<span class="ln">{e(x)}</span>' for x in p["subtitle"])
    sec = ""
    if p.get("labels"):
        sec = '<div class="sec chips">' + "".join(
            f'<span class="chip"><span class="dot"></span>{e(x)}</span>' for x in p["labels"]) + "</div>"
    elif p.get("pipeline"):
        parts = []
        for i, x in enumerate(p["pipeline"]):
            if i:
                parts.append('<span class="arrow">→</span>')
            parts.append(f'<span class="step">{e(x)}</span>')
        sec = '<div class="sec pipe">' + "".join(parts) + "</div>"
    elif p.get("note"):
        sec = f'<div class="sec note-line">{e(p["note"])}</div>'
    elif p.get("hint"):
        hint = e(p["hint"])
        for k in ("Ctrl", "Shift", "Space"):
            hint = re.sub(rf"\b{k}\b", f"<kbd>{k}</kbd>", hint, count=1)
        sec = f'<div class="sec hint">{hint}</div>'
    return (f'<div class="txt" data-zone="txt"><h1 class="h title">{e(p["name"])}</h1>'
            f'<p class="sub">{sub}</p>{sec}</div>')


SYNTH = {"ai-tender-radar", "stock-configurator"}


# ---------------------------------------------------------------- мотив профиля
# Формы решения — контурные значки 24×24 (сайт, кабинет, бот, приложение, автоматизация).
FORM_ICONS = [
    '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 8.5h18"/><path d="M6.5 12.5h8"/><path d="M6.5 16h5"/>',
    '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M8.5 4v16"/><path d="M11.5 9h6"/><path d="M11.5 12.5h6"/><path d="M11.5 16h4"/>',
    '<path d="M4.5 4.5h15a1.5 1.5 0 0 1 1.5 1.5v9a1.5 1.5 0 0 1-1.5 1.5H10l-4.5 3.5v-3.5h-1A1.5 1.5 0 0 1 3 15V6a1.5 1.5 0 0 1 1.5-1.5z"/>'
    '<path d="M8 10.5h.01"/><path d="M12 10.5h.01"/><path d="M16 10.5h.01"/>',
    '<rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/>',
    '<path d="M20.5 11a8.5 8.5 0 0 0-14.8-4.7L3.5 8.5"/><path d="M3.5 3.5v5h5"/>'
    '<path d="M3.5 13a8.5 8.5 0 0 0 14.8 4.7l2.2-2.2"/><path d="M20.5 20.5v-5h-5"/>',
]


def motif(w: int, h: int, seed: int = 7) -> str:
    """Разбор (steel-точки сходятся) -> одна задача (lime, знак бренда) -> пять форм решения:
    сайт, кабинет, бот, приложение, автоматизация. Лаймовая точка на форме — запущено."""
    rnd = random.Random(seed)
    cy = h / 2
    ts = min(h * 0.3, 76)                       # задача
    tx = w * 0.30
    n = len(FORM_ICONS)
    pitch = (h - 4) / n
    s = min(pitch * 0.8, 52)                    # плитка формы
    xr = w - s / 2 - 6
    bulge = min(w * 0.07, 34)
    dots = []
    for _ in range(int(w * 0.16)):
        t = rnd.random() ** 0.8
        x = t * (tx - ts / 2 - 12)
        spread = (1 - t) * (h / 2 - 6) + ts * 0.28 * t
        y = cy + rnd.uniform(-1, 1) * spread
        r = rnd.uniform(1.0, 2.2)
        op = 0.16 + 0.6 * t * rnd.uniform(0.6, 1)
        dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#7f99ad" opacity="{op:.2f}"/>')
    links, tiles = [], []
    x0 = tx + ts / 2 + 6
    for i, icon in enumerate(FORM_ICONS):
        k = (i - (n - 1) / 2) / ((n - 1) / 2)
        fx = xr - bulge * k * k
        fy = 2 + pitch * (i + 0.5)
        x1 = fx - s / 2 - 8
        mx = x0 + (x1 - x0) * 0.5
        links.append(f'<path d="M{x0:.1f} {cy:.1f} C{mx:.1f} {cy:.1f} {mx:.1f} {fy:.1f} {x1:.1f} {fy:.1f}" fill="none" '
                     f'stroke="url(#ln)" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>')
        sc = s * 0.56 / 24
        tiles.append(
            f'<rect x="{fx - s / 2:.1f}" y="{fy - s / 2:.1f}" width="{s:.1f}" height="{s:.1f}" rx="{s * 0.24:.1f}" '
            f'fill="#0a0f14" stroke="#e9eef2" stroke-opacity=".24" stroke-width="1.5"/>'
            f'<g transform="translate({fx - 12 * sc:.2f} {fy - 12 * sc:.2f}) scale({sc:.3f})" fill="none" stroke="#e9eef2" '
            f'stroke-width="{1.7 / sc * s / 44:.2f}" stroke-linecap="round" stroke-linejoin="round" opacity=".92">{icon}</g>'
            f'<circle cx="{fx + s / 2 - s * 0.02:.1f}" cy="{fy - s / 2 + s * 0.02:.1f}" r="{max(3.0, s * 0.075):.1f}" '
            f'fill="#c3f451" stroke="#05070a" stroke-width="2.5"/>')
    return f"""<svg class="motif" width="{w}" height="{h}" viewBox="0 0 {w} {h}" data-illus="1" data-zone="vis">
  <defs>
    <radialGradient id="lg"><stop offset="0" stop-color="#c3f451" stop-opacity=".28"/><stop offset="1" stop-color="#c3f451" stop-opacity="0"/></radialGradient>
    <linearGradient id="ln" gradientUnits="userSpaceOnUse" x1="{x0:.1f}" x2="{xr - bulge:.1f}" y1="0" y2="0"><stop offset="0" stop-color="#c3f451"/><stop offset="1" stop-color="#e9eef2" stop-opacity=".7"/></linearGradient>
  </defs>
  {''.join(dots)}
  {''.join(links)}
  <circle cx="{tx:.1f}" cy="{cy:.1f}" r="{ts * 1.1:.1f}" fill="url(#lg)"/>
  <rect x="{tx - ts / 2:.1f}" y="{cy - ts / 2:.1f}" width="{ts:.1f}" height="{ts:.1f}" rx="{ts * 0.26:.1f}" fill="#0b1008" stroke="#c3f451" stroke-width="2.5"/>
  <rect x="{tx - ts * 0.14:.1f}" y="{cy - ts * 0.14:.1f}" width="{ts * 0.28:.1f}" height="{ts * 0.28:.1f}" rx="2" fill="#c3f451"/>
  {''.join(tiles)}
</svg>"""


# ---------------------------------------------------------------- регистрация ассетов
JOBS: list[dict] = []


NBSP_RE = re.compile(r"(?<![\w-])([а-яёА-ЯЁ]{1,2}|[—–]) (?=\S)")


def typo(body: str) -> str:
    """Типографика картинок: неразрывный пробел после коротких предлогов/союзов и после тире.
    Слова не меняются, меняется только перенос строк."""
    def fix(m):
        txt = m.group(1)
        txt = NBSP_RE.sub(lambda k: k.group(1) + "\u00a0", txt)
        txt = re.sub(r" (?=[—–][ \u00a0])", "\u00a0", txt)
        txt = re.sub(r"(\d) (?=(?:[а-яё]{1,4}|₽|ГБ|ТБ)\b)", "\\1\u00a0", txt)
        return ">" + txt + "<"
    return re.sub(r">([^<>]+)<", fix, body)


def add(out: Path, cls: str, body: str, w: int, h: int | None, dpr: float, display: int | None,
        square: bool = False, photo: bool = False):
    name = out.stem
    body = typo(body)
    BUILD.joinpath("html").mkdir(parents=True, exist_ok=True)
    hp = BUILD / "html" / f"{out.parent.parts[-3] if 'docs' in out.parts else out.parent.parts[-2]}__{name}.html"
    size = f"width:{w}px;" + (f"height:{h}px;" if h else "")
    flow = " flow" if h is None else ""
    sq = " square" if square else ""
    doc = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<link rel="stylesheet" href="{furl(BUILD / 'fonts.css')}">
<link rel="stylesheet" href="{furl(TPL / 'base.css')}">
<link rel="stylesheet" href="{furl(TPL / 'layouts.css')}">
<style>html,body{{width:{w}px}}</style></head>
<body><div id="stage"><div class="frame {cls}{flow}{sq}" style="{size}">{body}</div></div></body></html>"""
    hp.write_text(doc, encoding="utf-8")
    JOBS.append({"name": f"{out.parent.name}/{out.name}", "html": furl(hp), "out": str(out).replace("\\", "/"),
                 "w": w, "h": h or 0, "dpr": dpr, "display": display or 0, "square": square, "photo": photo})


def a_profile():
    d = OUT / OWNER / "assets"
    b = T["profile"]["banner"]
    title = f'<span class="l">{e(b["title"][0])}</span><br><span class="l lime">{e(b["title"][1])}</span>'
    top = f'<div class="top mono" data-zone="top"><span class="mark"></span>{e(b["eyebrow"])}</div>'
    # слова через дефис («Telegram-боты», «веб-сервисы») не разрываются переносом; текст не меняется
    sub = re.sub(r"(\w+(?:-\w+)+)", r'<span class="nw">\1</span>', e(b["subtitle"]))
    txt = f'<div class="txt" data-zone="txt"><h1 class="h title">{title}</h1><p class="sub">{sub}</p></div>'
    add(d / "profile-banner.png", "f-pb", top + txt + motif(330, 300), 1200, 400, 2, DESK_CHECK)
    add(d / "profile-banner-mobile.png", "f-pbm", top + txt + motif(640, 300, 11), 720, None, 1.5, MOB_CHECK)
    add(d / "social-preview.png", "f-ps", top + txt + motif(320, 340, 5), 1280, 640, 1, None, square=True)
    for repo in REPOS:
        c = T["profile"]["cards"][repo]
        line = card_text(c)
        arrow = f'<div class="arrow-btn">{ARROW_SVG}</div>'
        st = synth_tag() if repo in SYNTH else ""
        meta = meta_line(c["meta"])
        add(d / f"card-{repo}.png", "f-card",
            top_slug(repo, go=True) + line + st + meta + viswrap(repo, 640, 26, 0.88, card=True),
            1200, 360, 2, DESK_CHECK)
        add(d / f"card-{repo}-mobile.png", "f-cardm",
            top_slug(repo) + line + meta + st + arrow
            + viswrap(repo, 0, 0, 640 / 600, flow=True, crop_h=380, card=True),
            720, None, 1.5, MOB_CHECK)
    # проекты без открытого репозитория: тот же формат, вверху — адрес сайта, на который ведёт карточка
    for key, c in T["profile"]["external_cards"].items():
        line = card_text(c)
        arrow = f'<div class="arrow-btn">{ARROW_SVG}</div>'
        st = synth_tag("demo_label") if c.get("demo") else ""
        meta = meta_line(c["meta"])
        ph = bool(c.get("photo"))
        add(d / f"card-{key}.png", "f-card",
            top_url(c["url"], go=True) + line + st + meta + viswrap(key, 640, 26, 0.88), 1200, 360, 2, DESK_CHECK,
            photo=ph)
        add(d / f"card-{key}-mobile.png", "f-cardm",
            top_url(c["url"]) + line + meta + st + arrow
            + viswrap(key, 0, 0, 640 / 600, flow=True, crop_h=380),
            720, None, 1.5, MOB_CHECK, photo=ph)


def a_products():
    for repo in REPOS:
        d = OUT / repo / "docs" / "assets"
        st = synth_tag() if repo in SYNTH else ""
        add(d / f"{repo}-banner.png", "f-banner",
            top_slug(repo) + product_text(repo) + st + byline() + viswrap(repo, 618, 40, 0.92),
            1200, 460, 2, DESK_CHECK)
        add(d / f"{repo}-banner-mobile.png", "f-mobile",
            top_slug(repo) + product_text(repo, True) + st
            + viswrap(repo, 0, 0, 640 / 600, flow=True, crop_h=400) + byline(),
            720, None, 1.5, MOB_CHECK)
        add(d / f"{repo}-social-preview.png", "f-social",
            top_slug(repo) + product_text(repo) + st + byline() + viswrap(repo, 666, 150, 1.0),
            1280, 640, 1, None, square=True)


def a_tender():
    d = OUT / "ai-tender-radar" / "docs" / "assets"
    s = T["tender_scheme"]
    for cls, w, dpr, disp, suffix in (("f-diag", 1200, 2, DESK_CHECK, ""), ("f-diagm", 720, 1.5, MOB_CHECK, "-mobile")):
        rows = "".join(
            f'<div class="row k-{x["kind"]}"><span class="num">{i + 1:02d}</span>'
            f'<span class="node"><i></i></span><span class="t">{e(x["title"])}</span>'
            f'<span class="d">{e(x["text"])}</span></div>' for i, x in enumerate(s["steps"]))
        body = (f'<div class="diag"><div class="rows"><div class="rail"></div>{rows}</div>'
                f'<div class="note"><span class="bang">!</span><span>{e(s["note"])}</span></div></div>')
        add(d / f"ai-tender-radar-how-it-works{suffix}.png", f"{cls} diag", body, w, None, dpr, disp)
    body = synth_tag() + f'<div class="tg">{tg_bubble(T["tender_card"], kb=True)}</div>'
    add(d / "ai-tender-radar-card.png", "f-tgcard", body, 400, None, 2, MOB_CHECK)


def a_dsh_screens():
    d = OUT / "dsh-mobile" / "docs" / "assets"
    for cls, w, dpr, disp, suffix in (("f-screens", 1000, 2, DESK_CHECK, ""), ("f-screensm", 720, 1.5, MOB_CHECK, "-mobile")):
        cols = "".join(
            f'<div class="col"><div class="ph" data-illus="1"><img src="{furl(SRC / x["file"])}"></div>'
            f'<div class="cap">{e(x["caption"])}</div></div>' for x in T["dsh_screens"])
        add(d / f"dsh-mobile-screens{suffix}.png", cls, f'<div class="screens">{cols}</div>', w, None, dpr, disp)


# ---------------------------------------------------------------- шрифты и рендер
def write_fonts_css():
    BUILD.mkdir(parents=True, exist_ok=True)
    css = []
    for fam, f, wt in (("Onest", "Onest-VF.ttf", "100 900"), ("JBM", "JetBrainsMono-VF.ttf", "100 800")):
        b64 = base64.b64encode((GEN / "fonts" / f).read_bytes()).decode()
        css.append(f'@font-face{{font-family:"{fam}";src:url(data:font/ttf;base64,{b64}) format("truetype");'
                   f'font-weight:{wt};font-display:block}}')
    (BUILD / "fonts.css").write_text("\n".join(css), encoding="utf-8")


RENDER_JS = r"""async page => {
  const jobs = __JOBS__;
  const MIN = __MIN__, MINM = __MINM__;
  const browser = page.context().browser();
  const report = [];
  const ctxs = {};
  for (const j of jobs) {
    const key = String(j.dpr);
    if (!ctxs[key]) ctxs[key] = await browser.newContext({deviceScaleFactor: j.dpr, viewport: {width: 1400, height: 1000}});
    const p = await ctxs[key].newPage();
    await p.setViewportSize({width: j.w, height: j.h || 3000});
    await p.goto(j.html);
    await p.evaluate(async () => {
      await Promise.all(['400 20px Onest', '600 20px Onest', '500 20px JBM', '600 20px JBM'].map(f => document.fonts.load(f)));
      await document.fonts.ready;
    });
    await p.waitForFunction(() => [...document.images].every(i => i.complete && i.naturalWidth > 0), null, {timeout: 15000});
    const res = await p.evaluate(({display, MIN, MINM}) => {
      const errs = [], warn = [];
      const frame = document.querySelector('.frame');
      const fr = frame.getBoundingClientRect();
      if (!document.fonts.check('600 20px Onest') || !document.fonts.check('500 20px JBM')) errs.push('fonts not loaded');
      const scale = display ? display / fr.width : 0;
      let minSeen = 99, minEl = '';
      for (const el of frame.querySelectorAll('*')) {
        const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
        if (!hasText) continue;
        const cs = getComputedStyle(el);
        const label = (el.textContent || '').trim().slice(0, 40);
        if (/(hidden|clip)/.test(cs.overflow + cs.overflowX) && el.scrollWidth > el.clientWidth + 1)
          errs.push('clipped: ' + label);
        if (el.closest('[data-illus]')) continue;
        const r = document.createRange(); r.selectNodeContents(el); const rr = r.getBoundingClientRect();
        if (rr.left < fr.left - .5 || rr.right > fr.right + .5 || rr.top < fr.top - .5 || rr.bottom > fr.bottom + .5)
          errs.push('outside frame: ' + label);
        if (scale) {
          const fs = parseFloat(cs.fontSize) * scale;
          const mono = cs.fontFamily.includes('JBM');
          if (fs < (mono ? MINM : MIN)) errs.push(`too small ${fs.toFixed(1)}px: ` + label);
          if (fs < minSeen) { minSeen = fs; minEl = label; }
        }
      }
      // текстовые зоны не пересекаются друг с другом и с визуальной зоной
      const zones = [...frame.querySelectorAll('[data-zone]')].map(z => {
        let rc = z.getBoundingClientRect();
        if (z.dataset.zone !== 'vis') {
          const r = document.createRange(); r.selectNodeContents(z); rc = r.getBoundingClientRect();
        }
        return {n: z.dataset.zone, r: rc};
      });
      for (let a = 0; a < zones.length; a++) for (let b = a + 1; b < zones.length; b++) {
        const A = zones[a].r, B = zones[b].r;
        if (A.width === 0 || B.width === 0) continue;
        if (A.left < B.right - 1 && B.left < A.right - 1 && A.top < B.bottom - 1 && B.top < A.bottom - 1)
          errs.push(`overlap: ${zones[a].n} x ${zones[b].n}`);
      }
      return {errs, warn, minSeen: minSeen === 99 ? null : +minSeen.toFixed(1), minEl, h: fr.height};
    }, {display: j.display, MIN, MINM});
    const el = await p.$('.frame');
    await el.screenshot({path: j.out, omitBackground: !j.square});
    await p.close();
    report.push({name: j.name, ...res});
  }
  for (const k in ctxs) await ctxs[k].close();
  return '@@R@@' + JSON.stringify(report) + '@@R@@';
}"""


def run_js(js: str, tag: str) -> str:
    p = BUILD / f"{tag}.js"
    p.write_text(js, encoding="utf-8")
    r = subprocess.run([str(PW), f"-s={SESSION}", "run-code", f"--filename={p.as_posix()}"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    out = r.stdout + r.stderr
    m = re.search(r"@@R@@(.*?)@@R@@", out, re.S)
    if not m:
        if "is not open" in out or "not running" in out.lower():
            subprocess.run([str(PW), f"-s={SESSION}", "open", "about:blank"], capture_output=True, timeout=120)
            return run_js(js, tag + "_retry")
        raise SystemExit(f"Playwright: нет результата.\n{out[-3000:]}")
    raw = m.group(1).strip()
    try:
        return json.loads(raw) if raw.startswith("[") else json.loads(json.loads(f'"{raw}"'))
    except json.JSONDecodeError:
        return json.loads(raw.encode().decode("unicode_escape").encode("latin-1").decode("utf-8"))


def quantize_photo(im: Image.Image) -> tuple[Image.Image, bytes]:
    """Палитра для фотоснимков с прозрачными скруглёнными углами: median cut по RGB (октодерево
    даёт пятна на градиентах кожи и фона) + 16 уровней прозрачности цвета фона для краёв рамки."""
    import numpy as np
    a = np.asarray(im)
    q = im.convert("RGB").quantize(240, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    idx = np.asarray(q).copy()
    pal = q.getpalette()[:240 * 3] + [5, 7, 10] * 16
    trns = bytes([255] * 240 + [round(k * 255 / 15) for k in range(16)])
    edge = a[..., 3] < 255
    idx[edge] = 240 + np.round(a[..., 3][edge] / 17).astype(np.uint8)
    out = Image.fromarray(idx, "P")
    out.putpalette(pal)
    return out, trns


def optimize(path: Path, photo: bool = False) -> str:
    im = Image.open(path)
    im.load()
    if im.mode == "RGBA" and im.getchannel("A").getextrema() == (255, 255):
        im = im.convert("RGB")
    im.save(path, optimize=True)
    note = ""
    if path.stat().st_size > MAX_BYTES and photo and im.mode == "RGBA":
        q, trns = quantize_photo(im)
        q.save(path, optimize=True, transparency=trns)
        return "quantized"
    if path.stat().st_size > MAX_BYTES:
        if im.mode == "RGBA":
            q = im.quantize(256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
        else:
            q = im.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        tmp = path.with_suffix(".q.png")
        q.save(tmp, optimize=True)
        if tmp.stat().st_size < path.stat().st_size:
            tmp.replace(path)
            note = "quantized"
        else:
            tmp.unlink()
    return note


# ---------------------------------------------------------------- превью README
def gh_markdown(md_path: Path, context: str) -> str:
    r = subprocess.run(["gh", "api", "markdown", "-f", "mode=gfm", "-f", f"context={context}", "-F", f"text=@{md_path}"],
                       capture_output=True, timeout=120)
    if r.returncode:
        raise SystemExit("gh api markdown: " + r.stderr.decode("utf-8", "replace"))
    return r.stdout.decode("utf-8")


def previews():
    PREVIEW.mkdir(parents=True, exist_ok=True)
    jobs = []
    for repo in [OWNER] + REPOS:
        md = OUT / repo / "README.md"
        if not md.is_file():
            continue
        ctx, deskw = f"{OWNER}/{repo}", (1012 if repo == OWNER else 830)
        body = gh_markdown(md, ctx)
        (BUILD / f"{repo}.gfm.html").write_text(body, encoding="utf-8")
        for theme, bg in (("light", "#ffffff"), ("dark", "#0d1117")):
            for mode, vw, aw, pad in (("desktop", deskw + 64, deskw, 24), ("mobile", 390, 390 - 16, 16)):
                doc = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<base href="{furl(OUT / repo)}/">
<link rel="stylesheet" href="{furl(TPL / f'github-markdown-{theme}.css')}">
<style>body{{margin:0;background:{bg};padding:8px 0}} .markdown-body{{box-sizing:border-box;width:{aw}px;margin:0 auto;padding:{pad}px;
border:1px solid {'#d1d9e0' if theme == 'light' else '#3d444d'};border-radius:6px}}</style></head>
<body><article class="markdown-body">{body}</article></body></html>"""
                hp = BUILD / "html" / f"preview-{repo}-{mode}-{theme}.html"
                hp.write_text(doc, encoding="utf-8")
                jobs.append({"html": furl(hp), "out": (PREVIEW / f"{repo}-{mode}-{theme}.png").as_posix(),
                             "w": vw, "scheme": theme})
    if not jobs:
        print(f"  README.md в {OUT}\\<репозиторий>\\ не найдены — превью пропущено.")
        return False
    js = r"""async page => {
  const jobs = __JOBS__;
  const browser = page.context().browser();
  const rep = [];
  for (const j of jobs) {
    const ctx = await browser.newContext({deviceScaleFactor: 1, viewport: {width: j.w, height: 900}, colorScheme: j.scheme});
    const p = await ctx.newPage();
    await p.goto(j.html);
    await p.waitForFunction(() => [...document.images].every(i => i.complete), null, {timeout: 15000});
    const info = await p.evaluate(() => {
      const art = document.querySelector('.markdown-body');
      const broken = [...document.images].filter(i => !i.naturalWidth).map(i => i.getAttribute('src'));
      const imgs = [...document.images].map(i => ({src: i.currentSrc.split('/').slice(-1)[0], w: Math.round(i.getBoundingClientRect().width)}));
      return {broken, imgs, overflow: art.scrollWidth > art.clientWidth + 1, h: document.body.scrollHeight};
    });
    await p.screenshot({path: j.out, fullPage: true});
    rep.push({out: j.out.split('/').slice(-1)[0], ...info});
    await ctx.close();
  }
  return '@@R@@' + JSON.stringify(rep) + '@@R@@';
}""".replace("__JOBS__", json.dumps(jobs))
    rep = run_js(js, "preview")
    bad = False
    for r in rep:
        flag = ""
        if r["broken"] or r["overflow"]:
            flag, bad = "  <-- ОШИБКА", True
        imgs = ";".join(f"{i['src']}@{i['w']}" for i in r["imgs"])
        print(f'  {r["out"]:44} h={r["h"]:5}  imgs={imgs}'
              f'{"  broken=" + str(r["broken"]) if r["broken"] else ""}{flag}')
        tile(PREVIEW / r["out"])
    return bad


def tile(p: Path, step: int = 1800):
    d = PREVIEW / "tiles"
    d.mkdir(exist_ok=True)
    for old in d.glob(p.stem + "-*.png"):
        old.unlink()
    im = Image.open(p)
    n = math.ceil(im.height / step)
    for i in range(n):
        im.crop((0, i * step, im.width, min(im.height, (i + 1) * step))).save(d / f"{p.stem}-{i + 1}.png", optimize=True)


# ---------------------------------------------------------------- main
def main():
    global OUT, PREVIEW, BUILD, PW, SESSION
    for s in (sys.stdout, sys.stderr):
        s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Генератор картинок GitHub-аккаунта (подробности — в docstring build.py).")
    ap.add_argument("--out", type=Path, default=GEN / "out", help="каталог вывода (по умолчанию ./out рядом с build.py)")
    ap.add_argument("--only", default="", help="собрать только файлы, в имени которых есть эта подстрока")
    ap.add_argument("--preview", action="store_true", help="отрендерить README из --out через GitHub Markdown API")
    ap.add_argument("--preview-dir", type=Path, default=GEN / "preview", help="каталог превью (по умолчанию ./preview)")
    ap.add_argument("--playwright", default=os.environ.get("PLAYWRIGHT_CLI") or DEFAULT_PW,
                    help="Playwright CLI (по умолчанию $PLAYWRIGHT_CLI, иначе обёртка DSH)")
    ap.add_argument("--session", default=SESSION, help="имя сессии Playwright CLI (по умолчанию ghdesign)")
    ap.add_argument("--keep-build", action="store_true", help="не удалять промежуточные HTML/JS")
    a = ap.parse_args()

    OUT = a.out.resolve()
    PREVIEW = a.preview_dir.resolve()
    PW, SESSION = a.playwright, a.session
    if not (Path(PW).is_file() or shutil.which(PW)):
        raise SystemExit(f"Playwright CLI не найден: {PW}. Укажите --playwright или PLAYWRIGHT_CLI.")
    BUILD = Path(tempfile.mkdtemp(prefix="gh-assets-"))
    try:
        failed = render_all(a.only)
        if a.preview:
            print("Превью README (GitHub Markdown API)…")
            failed |= previews()
    finally:
        if a.keep_build:
            print("Промежуточные файлы:", BUILD)
        else:
            shutil.rmtree(BUILD, ignore_errors=True)
    if failed:
        print("СБОРКА С ОШИБКАМИ")
        sys.exit(1)
    print("Готово:", OUT)


def render_all(only: str) -> bool:
    write_fonts_css()
    a_profile()
    a_products()
    a_tender()
    a_dsh_screens()
    jobs = [j for j in JOBS if only in j["name"]]
    if not jobs:
        raise SystemExit(f"Нет файлов, подходящих под --only {only!r}")
    for j in jobs:
        Path(j["out"]).parent.mkdir(parents=True, exist_ok=True)
    print(f"Рендер {len(jobs)} изображений в {OUT}…")
    js = RENDER_JS.replace("__JOBS__", json.dumps(jobs, ensure_ascii=False)) \
        .replace("__MIN__", str(MIN_PX)).replace("__MINM__", str(MIN_PX_MONO))
    report = run_js(js, "render")
    failed = False
    for r, j in zip(report, jobs):
        p = Path(j["out"])
        note = optimize(p, j.get("photo", False))
        with Image.open(p) as im:
            size = im.size
        kb = p.stat().st_size / 1024
        flag = ""
        if r["errs"]:
            failed = True
            flag = "  <-- " + "; ".join(r["errs"][:6])
        if kb * 1024 > MAX_BYTES:
            flag += "  (>500 KB)"
        ms = f'min {r["minSeen"]}px@{j["display"]}' if r["minSeen"] else ""
        print(f'  {r["name"]:58} {size[0]:>4}×{size[1]:<4} {kb:6.0f} KB {note:9} {ms}{flag}')
    return failed


if __name__ == "__main__":
    main()