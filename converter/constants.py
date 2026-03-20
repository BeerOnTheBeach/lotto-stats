# 6aus49 Lotto constants
# Official win class reference:
#   Class 1:  6 correct + super number  (jackpot)
#   Class 2:  6 correct
#   Class 3:  5 correct + super number
#   Class 4:  5 correct
#   Class 5:  4 correct + super number
#   Class 6:  4 correct
#   Class 7:  3 correct + super number
#   Class 8:  3 correct
#   Class 9:  2 correct + super number
#   No prize: 2 correct / 1 correct + super number / 1 correct / 0 correct

# ---------------------------------------------------------------------------
# WIN_CLASSES
# Key   = win class number (1 = best, 9 = lowest prize tier)
# None  = no official prize
# avg_win_eur:
#   Classes 1-3  → variable / jackpot, not tracked
#   Classes 4-6  → variable, averaged
#   Classes 7-9  → fixed amounts
# ---------------------------------------------------------------------------
WIN_CLASSES: dict[int | None, dict] = {
    1: {
        "correct": 6,
        "super_number": True,
        "label": "6 correct + super number",
        "avg_win_eur": None,       # jackpot, not tracked
    },
    2: {
        "correct": 6,
        "super_number": False,
        "label": "6 correct",
        "avg_win_eur": None,       # jackpot range, not tracked
    },
    3: {
        "correct": 5,
        "super_number": True,
        "label": "5 correct + super number",
        "avg_win_eur": None,       # variable, not tracked
    },
    4: {
        "correct": 5,
        "super_number": False,
        "label": "5 correct",
        "avg_win_eur": 2900.00,    # avg variable prize
    },
    5: {
        "correct": 4,
        "super_number": True,
        "label": "4 correct + super number",
        "avg_win_eur": 150.00,     # avg variable prize
    },
    6: {
        "correct": 4,
        "super_number": False,
        "label": "4 correct",
        "avg_win_eur": 45.00,      # avg variable prize
    },
    7: {
        "correct": 3,
        "super_number": True,
        "label": "3 correct + super number",
        "avg_win_eur": 10.00,      # fixed
    },
    8: {
        "correct": 3,
        "super_number": False,
        "label": "3 correct",
        "avg_win_eur": 10.00,      # fixed
    },
    9: {
        "correct": 2,
        "super_number": True,
        "label": "2 correct + super number",
        "avg_win_eur": 5.00,       # fixed
    },
    # No-prize combinations below (win_class = None)
}

# No-prize combinations for reference (used in COLUMN_MAP)
NO_PRIZE_COMBINATIONS = [
    {"correct": 2, "super_number": False, "label": "2 correct",                  "avg_win_eur": 0.00},
    {"correct": 1, "super_number": True,  "label": "1 correct + super number",   "avg_win_eur": 0.00},
    {"correct": 1, "super_number": False, "label": "1 correct",                  "avg_win_eur": 0.00},
    {"correct": 0, "super_number": True,  "label": "0 correct + super number",   "avg_win_eur": 0.00},
    {"correct": 0, "super_number": False, "label": "0 correct",                  "avg_win_eur": 0.00},
]

# ---------------------------------------------------------------------------
# COLUMN_MAP
# Maps every possible CSV column name to its hit metadata.
# Naming convention in the CSV:
#   TrefferN    → N correct numbers, no super number
#   TrefferNSZ  → N correct numbers + super number
# "Treffer1" = 1 correct number (no super number) – no prize
# ---------------------------------------------------------------------------
COLUMN_MAP: dict[str, dict] = {
    # --- 0 correct ---
    "Treffer0":   {"correct": 0, "super_number": False, "win_class": None},   # 0 correct
    "Treffer0SZ": {"correct": 0, "super_number": True,  "win_class": None},   # 0 correct + SZ

    # --- 1 correct ---
    "Treffer1":   {"correct": 1, "super_number": False, "win_class": None},   # 1 correct
    "Treffer1SZ": {"correct": 1, "super_number": True,  "win_class": None},   # 1 correct + SZ

    # --- 2 correct ---
    "Treffer2":   {"correct": 2, "super_number": False, "win_class": None},   # 2 correct (no prize)
    "Treffer2SZ": {"correct": 2, "super_number": True,  "win_class": 9},      # 2 correct + SZ  → class 9

    # --- 3 correct ---
    "Treffer3":   {"correct": 3, "super_number": False, "win_class": 8},      # 3 correct       → class 8
    "Treffer3SZ": {"correct": 3, "super_number": True,  "win_class": 7},      # 3 correct + SZ  → class 7

    # --- 4 correct ---
    "Treffer4":   {"correct": 4, "super_number": False, "win_class": 6},      # 4 correct       → class 6
    "Treffer4SZ": {"correct": 4, "super_number": True,  "win_class": 5},      # 4 correct + SZ  → class 5

    # --- 5 correct ---
    "Treffer5":   {"correct": 5, "super_number": False, "win_class": 4},      # 5 correct       → class 4
    "Treffer5SZ": {"correct": 5, "super_number": True,  "win_class": 3},      # 5 correct + SZ  → class 3

    # --- 6 correct ---
    "Treffer6":   {"correct": 6, "super_number": False, "win_class": 2},      # 6 correct       → class 2
    "Treffer6SZ": {"correct": 6, "super_number": True,  "win_class": 1},      # 6 correct + SZ  → class 1 (jackpot)
}

