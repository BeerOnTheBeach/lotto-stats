"""
Converts lotto.csv → lotto.json

Usage:
    python -m converter.csv_to_json
    python -m converter.csv_to_json --input path/to/lotto.csv --output path/to/lotto.json
"""

import csv
import json
import argparse
from datetime import datetime
from collections import defaultdict

try:
    from converter.constants import COLUMN_MAP, WIN_CLASSES
except ModuleNotFoundError:
    from constants import COLUMN_MAP, WIN_CLASSES  # type: ignore[no-redef]


def parse_date(date_str: str) -> str:
    """Convert DD.MM.YYYY to ISO 8601 (YYYY-MM-DD)."""
    return datetime.strptime(date_str.strip(), "%d.%m.%Y").strftime("%Y-%m-%d")


def get_best_hit(row: dict) -> dict | None:
    """
    Returns the best hit for a player row.
    Iterates all known columns, picks the entry with the lowest win_class number
    (lower = better prize). win_class=None means no prize.
    Returns None if no column was marked.
    """
    best = None
    for col, info in COLUMN_MAP.items():
        if row.get(col, "").strip() != "1":
            continue
        if best is None:
            best = info
        else:
            curr_cls = best["win_class"]
            new_cls = info["win_class"]
            # None = no prize, always worse than any numbered class
            if new_cls is not None and (curr_cls is None or new_cls < curr_cls):
                best = info
    return best


def build_player_entry(row: dict) -> dict:
    """Build a clean player entry dict from a CSV row."""
    name = row["Spieler"].strip()
    hit = get_best_hit(row)

    win_class = hit["win_class"] if hit else None
    correct = hit["correct"] if hit else 0
    super_number = hit["super_number"] if hit else False
    avg_win_eur = WIN_CLASSES[win_class]["avg_win_eur"] if win_class is not None else 0.00

    return {
        "name": name,
        "win_class": win_class,
        "correct": correct,
        "super_number": super_number,
        "avg_win_eur": avg_win_eur,
    }


def convert(input_path: str = "lotto.csv", output_path: str = "lotto.json") -> None:
    draws_by_date: dict[str, list] = defaultdict(list)

    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_iso = parse_date(row["Datum"])
            draws_by_date[date_iso].append(build_player_entry(row))

    draws = [
        {"date": date, "players": players}
        for date, players in sorted(draws_by_date.items())
    ]

    output = {
        "meta": {
            "description": "6aus49 Lotto community tip pool",
            "win_classes": {
                str(k): v for k, v in WIN_CLASSES.items()
            },
        },
        "draws": draws,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total_entries = sum(len(d["players"]) for d in draws)
    prize_entries = [p for d in draws for p in d["players"] if p["win_class"] is not None]

    print(f"✓ {len(draws)} draws, {total_entries} player entries → {output_path}")
    print(f"✓ {len(prize_entries)} prize-winning hits recorded")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert lotto.csv to lotto.json")
    parser.add_argument("--input",  default="lotto.csv",  help="Path to the CSV input file")
    parser.add_argument("--output", default="lotto.json", help="Path to the JSON output file")
    args = parser.parse_args()

    convert(args.input, args.output)

