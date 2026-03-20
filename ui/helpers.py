"""
Shared helper functions: JSON I/O, player utils, table row builders.
"""

import json
import pandas as pd
from datetime import datetime

from ui.constants import JSON_PATH, WIN_CLASS_EUR, TABLE_HEADERS


# ── JSON I/O ─────────────────────────────────────────────────────────────────

def load() -> dict:
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)

def save(data: dict) -> None:
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── Domain helpers ────────────────────────────────────────────────────────────

def all_players(data: dict) -> list[str]:
    names: set[str] = set()
    for draw in data["draws"]:
        for p in draw["players"]:
            names.add(p["name"])
    return sorted(names)

def win_class_for(correct: int, super_number: bool) -> int | None:
    mapping = {
        (6, True): 1, (6, False): 2,
        (5, True): 3, (5, False): 4,
        (4, True): 5, (4, False): 6,
        (3, True): 7, (3, False): 8,
        (2, True): 9,
    }
    return mapping.get((correct, super_number), None)

def player_entry(name: str, correct: int, super_number: bool) -> dict:
    wc = win_class_for(correct, super_number)
    return {
        "name": name,
        "win_class": wc,
        "correct": correct,
        "super_number": super_number,
        "avg_win_eur": WIN_CLASS_EUR.get(wc, 0.0) if wc else 0.0,
    }


# ── Formatting ────────────────────────────────────────────────────────────────

def fmt_date_display(iso: str) -> str:
    y, m, d = iso.split("-")
    return f"{d}.{m}.{y}"

def fmt_date_iso(display: str) -> str:
    """Convert DD.MM.YYYY or YYYY-MM-DD to YYYY-MM-DD."""
    display = display.strip()
    if "." in display:
        parts = display.split(".")
        return f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
    return display


# ── Table helpers ─────────────────────────────────────────────────────────────

def _row(di: int, pi: int, draw: dict, p: dict) -> list:
    sz  = "✓" if p["super_number"] else ""
    wc  = str(p["win_class"]) if p["win_class"] else "–"
    eur = f"€{p['avg_win_eur']:.2f}" if p.get("avg_win_eur") else "€0.00"
    return [fmt_date_display(draw["date"]), p["name"], p["correct"], sz, wc, eur, di, pi]

def build_table_rows(data: dict) -> list[list]:
    rows = []
    for di, draw in enumerate(data["draws"]):
        for pi, p in enumerate(draw["players"]):
            rows.append(_row(di, pi, draw, p))
    return rows

def tdata_row(tdata, i: int) -> list:
    """Return row i whether tdata is a list-of-lists or a pandas DataFrame."""
    if isinstance(tdata, pd.DataFrame):
        return list(tdata.iloc[i])
    return list(tdata[i])

def tdata_len(tdata) -> int:
    if isinstance(tdata, pd.DataFrame):
        return len(tdata.index)
    return len(tdata)

