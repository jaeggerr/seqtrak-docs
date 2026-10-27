"""Word-level PDF extraction with coordinates.

`pdftotext -layout` loses column boundaries whenever a cell wraps, so every
table in this repo is rebuilt from `pdftotext -bbox-layout`, which gives each
word an exact bounding box. Rows are recovered by clustering on the vertical
centre of each word; columns by binning on the horizontal centre.
"""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

WORD = re.compile(
    r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>'
)
ENTITIES = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&apos;": "'"}
TICK = ""


@dataclass(frozen=True)
class Word:
    x0: float
    y0: float
    x1: float
    y1: float
    text: str

    @property
    def cx(self) -> float:
        return (self.x0 + self.x1) / 2

    @property
    def cy(self) -> float:
        return (self.y0 + self.y1) / 2


def page_words(pdf: Path, page: int) -> list[Word]:
    xml = subprocess.run(
        ["pdftotext", "-bbox-layout", "-f", str(page), "-l", str(page), str(pdf), "-"],
        check=True, capture_output=True, text=True,
    ).stdout
    out = []
    for x0, y0, x1, y1, text in WORD.findall(xml):
        for ent, ch in ENTITIES.items():
            text = text.replace(ent, ch)
        out.append(Word(float(x0), float(y0), float(x1), float(y1), text))
    return out


def rows(words: list[Word], tolerance: float = 3.0) -> list[list[Word]]:
    """Group words into visual lines, top to bottom, each sorted left to right."""
    out: list[list[Word]] = []
    for word in sorted(words, key=lambda w: (w.cy, w.x0)):
        if out and abs(out[-1][0].cy - word.cy) <= tolerance:
            out[-1].append(word)
        else:
            out.append([word])
    return [sorted(line, key=lambda w: w.x0) for line in out]


def find(words: list[Word], text: str) -> Word | None:
    return next((w for w in words if w.text == text), None)


def join(words: list[Word], x0: float, x1: float) -> str:
    """Text of every word whose centre falls in [x0, x1), reading order."""
    picked = [w for w in sorted(words, key=lambda w: (w.cy, w.x0))
              if x0 <= w.cx < x1 and w.text != TICK]
    return " ".join(w.text for w in picked).strip()


def ticked(words: list[Word], centre: float, tolerance: float = 14.0) -> bool:
    return any(w.text == TICK and abs(w.cx - centre) <= tolerance for w in words)


def nearest(words: list[Word], anchors: list[float], x0: float, x1: float) -> list[list[Word]]:
    """Bucket words in a column by the anchor row they are vertically closest to.

    Yamaha centres every cell vertically inside its row, so a wrapped name or
    description is always nearer its own row's anchor line than any other.
    """
    buckets: list[list[Word]] = [[] for _ in anchors]
    for word in words:
        if not (x0 <= word.cx < x1):
            continue
        best = min(range(len(anchors)), key=lambda i: abs(anchors[i] - word.cy))
        buckets[best].append(word)
    return buckets


def text_of(words: list[Word]) -> str:
    """Join words in reading order, closing up hyphens the PDF split apart.

    pdftotext emits "Lo", "-", "Fi" as three words. When a hyphen touches its
    neighbour (gap under ~1.5pt) the glyphs are adjacent on the page, so no
    space belongs there; a hyphen with real space around it keeps its spaces.
    """
    picked = [w for w in sorted(words, key=lambda w: (w.cy, w.x0)) if w.text != TICK]
    out = ""
    previous: Word | None = None
    for word in picked:
        if previous is not None:
            same_line = abs(word.cy - previous.cy) <= 3.0
            hyphen = word.text.startswith("-") or previous.text.endswith("-")
            if same_line and hyphen and word.x0 - previous.x1 < 1.5:
                out += word.text
                previous = word
                continue
            out += " "
        out += word.text
        previous = word
    return out.strip()


def label_groups(words: list[Word], x0: float, x1: float, gap: float = 5.5):
    """Cluster a spanning column (e.g. Category) into (centre_y, label) pairs."""
    picked = sorted((w for w in words if x0 <= w.cx < x1), key=lambda w: (w.cy, w.x0))
    groups: list[list[Word]] = []
    for word in picked:
        if groups and word.cy - max(w.cy for w in groups[-1]) <= gap:
            groups[-1].append(word)
        else:
            groups.append([word])
    return [(sum(w.cy for w in g) / len(g), text_of(g)) for g in groups]


def assign_spanning(anchor_ys: list[float], labels: list[tuple[float, str]]) -> list[str]:
    """Map rows to a column whose cells span several rows (Category, Block, ...).

    The label is drawn centred in its group of rows, so the group boundaries are
    recovered by choosing the split points that put each label's own centre
    closest to the midpoint of the rows it would then cover.
    """
    if not labels:
        return [""] * len(anchor_ys)
    n, k = len(anchor_ys), len(labels)
    if k == 1:
        return [labels[0][1]] * n

    INF = float("inf")
    # best[i][j] = cost of covering rows[i:] with labels[j:]
    best = [[INF] * (k + 1) for _ in range(n + 1)]
    cut = [[0] * (k + 1) for _ in range(n + 1)]
    best[n][k] = 0.0
    for j in range(k - 1, -1, -1):
        for i in range(n - 1, -1, -1):
            for end in range(i + 1, n + 1):
                if best[end][j + 1] == INF:
                    continue
                mid = (anchor_ys[i] + anchor_ys[end - 1]) / 2
                cost = abs(mid - labels[j][0]) + best[end][j + 1]
                if cost < best[i][j]:
                    best[i][j] = cost
                    cut[i][j] = end
    out, i = [], 0
    for j in range(k):
        end = cut[i][j] or n
        out += [labels[j][1]] * (end - i)
        i = end
    out += [labels[-1][1]] * (n - len(out))
    return out[:n]


SPREAD = 0.05


def partition(anchor_ys: list[float], items: list[tuple[float, object]]):
    """Split a column's text lines across table rows by vertical centring.

    Yamaha centres each cell's text on its row, so the right split is the one
    that puts every group's midpoint on its own row's anchor line. Nearest-anchor
    assignment gets this wrong whenever neighbouring rows have different heights,
    which happens throughout the Parameter Change Table.
    """
    n, k = len(items), len(anchor_ys)
    groups: list[list[object]] = [[] for _ in anchor_ys]
    if not n or not k:
        return groups

    ys = [y for y, _ in items]
    INF = float("inf")
    # Lines sitting on an anchor line itself are pinned to that row.
    pinned = [next((j for j in range(k) if abs(ys[i] - anchor_ys[j]) <= 2.0), None)
              for i in range(n)]

    best = [[INF] * (k + 1) for _ in range(n + 1)]
    cut = [[0] * (k + 1) for _ in range(n + 1)]
    best[n][k] = 0.0
    for j in range(k - 1, -1, -1):
        best[n][j] = 0.0
        cut[n][j] = n
        for i in range(n - 1, -1, -1):
            for end in range(i, n + 1):
                if any(pinned[t] is not None and pinned[t] != j for t in range(i, end)):
                    break
                if best[end][j + 1] == INF:
                    continue
                if end == i:
                    cost = 0.0 if pinned[i] != j else INF
                else:
                    # Centring is the primary signal; a small per-line distance
                    # term stops the solver from parking several rows' worth of
                    # text in one row and leaving its neighbours empty.
                    cost = abs((ys[i] + ys[end - 1]) / 2 - anchor_ys[j]) + SPREAD * sum(
                        abs(ys[t] - anchor_ys[j]) for t in range(i, end)
                    )
                total = cost + best[end][j + 1]
                if total < best[i][j]:
                    best[i][j] = total
                    cut[i][j] = end
    i = 0
    for j in range(k):
        end = cut[i][j]
        groups[j] = [obj for _, obj in items[i:end]]
        i = end
    for _, obj in items[i:]:
        groups[-1].append(obj)
    return groups


def column(lines: list[list[Word]], anchor_ys: list[float], x0: float, x1: float) -> list[str]:
    """Text of one column, split across rows by `partition`."""
    items = []
    for line in lines:
        picked = [w for w in line if x0 <= w.cx < x1 and w.text != TICK]
        if picked:
            items.append((line[0].cy, picked))
    groups = partition(anchor_ys, items)
    return [text_of([w for part in g for w in part]) for g in groups]


def grid(lines: list[list[Word]], anchor: tuple[float, float], bounds: list[float],
         top: float = 0.0, bottom: float = 800.0) -> list[list[str]]:
    """Read a plain grid: rows anchored by a leading column, cells by x bounds.

    `anchor` is the x range of the column that always carries a value (usually
    the row number); `bounds` are the column edges, len(bounds) == columns + 1.
    """
    body = [l for l in lines if top < l[0].cy < bottom]
    ys = [l[0].cy for l in body
          if any(anchor[0] <= w.cx < anchor[1] for w in l)]
    cols = [column(body, ys, bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)]
    return [list(cells) for cells in zip(*cols)]


def banded_column(lines: list[list[Word]], anchor_ys: list[float],
                  x0: float, x1: float) -> list[str]:
    """Text of one column, split by strict top-aligned bands.

    Cells whose content starts on the row's own anchor line and runs downwards —
    the per-byte Range column of a multi-byte parameter, for instance — are not
    vertically centred, so centring would steal their tail for the next row.
    """
    out = []
    for i, top in enumerate(anchor_ys):
        bottom = anchor_ys[i + 1] if i + 1 < len(anchor_ys) else 10_000.0
        picked = [w for line in lines if top - 1.0 <= line[0].cy < bottom - 1.0
                  for w in line if x0 <= w.cx < x1]
        out.append(text_of(picked))
    return out
