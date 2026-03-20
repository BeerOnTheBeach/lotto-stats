"""
Shared constants for the Lotto web UI.
"""

from pathlib import Path

JSON_PATH = Path("lotto.json")

WIN_CLASS_LABELS = {
    1: "6 correct + SZ",
    2: "6 correct",
    3: "5 correct + SZ",
    4: "5 correct",
    5: "4 correct + SZ",
    6: "4 correct",
    7: "3 correct + SZ",
    8: "3 correct",
    9: "2 correct + SZ",
}

WIN_CLASS_EUR = {1: None, 2: None, 3: None, 4: 2900, 5: 150, 6: 45, 7: 10, 8: 10, 9: 5}

PLAYER_COLORS = [
    "#4e79a7", "#f28e2b", "#e15759", "#76b7b2",
    "#59a14f", "#edc948", "#b07aa1", "#ff9da7",
    "#9c755f", "#bab0ac",
]

# ── Dataframe table ──────────────────────────────────────────────────────────
# Columns:  0=Date  1=Player  2=Correct(editable)  3=SZ(editable)
#           4=Win Class(locked)  5=Avg Win €(locked)  6=_di(locked)  7=_pi(locked)
TABLE_HEADERS = [
    "📅 Date", "👤 Player", "✏ Correct", "✏ SZ",
    "🔒 Win Class", "🔒 Avg Win €", "🔒 _di", "🔒 _pi",
]
TABLE_DATATYPE = ["str", "str", "number", "str", "str", "str", "number", "number"]
TABLE_COL_WIDTHS = ["110px", "90px", "80px", "50px", "100px", "100px", "55px", "55px"]

# ── Custom CSS ───────────────────────────────────────────────────────────────
LOCKED_COL_CSS = """
/* Dim locked columns (Win Class, Avg Win €, _di, _pi) — cols 5-8 (1-indexed in CSS nth-child) */
.lotto-table table tbody tr td:nth-child(5),
.lotto-table table tbody tr td:nth-child(6),
.lotto-table table tbody tr td:nth-child(7),
.lotto-table table tbody tr td:nth-child(8) {
    color: #999 !important;
    background-color: #f5f5f5 !important;
    font-style: italic;
    cursor: not-allowed !important;
}
.lotto-table table thead tr th:nth-child(5),
.lotto-table table thead tr th:nth-child(6),
.lotto-table table thead tr th:nth-child(7),
.lotto-table table thead tr th:nth-child(8) {
    color: #999 !important;
    background-color: #ececec !important;
}
"""

