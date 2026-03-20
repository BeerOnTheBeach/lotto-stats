"""
All matplotlib chart functions + generate_all_plots().
"""

from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker
import numpy as np
from matplotlib.ticker import MaxNLocator

matplotlib.use("Agg")

from ui.constants import WIN_CLASS_LABELS, WIN_CLASS_EUR, PLAYER_COLORS
from ui.helpers import all_players


# ── Color helper ──────────────────────────────────────────────────────────────

def _color(player: str, players: list[str]) -> str:
    return PLAYER_COLORS[players.index(player) % len(PLAYER_COLORS)]

def _parse_dates(draws: list[dict]) -> list:
    return [datetime.strptime(d["date"], "%Y-%m-%d") for d in draws]


# ── Summary ───────────────────────────────────────────────────────────────────

def stats_overview(data: dict) -> str:
    players = all_players(data)
    lines = ["## 📊 Overall Summary\n"]
    lines.append(f"**Draws recorded:** {len(data['draws'])}  ")
    lines.append(f"**Players:** {', '.join(players)}  \n")
    lines.append("| Player | Entries | Hits | Hits% | Wins | Win% | Total € |")
    lines.append("|--------|---------|------|-------|------|------|---------|")
    for name in players:
        entries = [p for d in data["draws"] for p in d["players"] if p["name"] == name]
        wins    = [p for p in entries if p["win_class"] is not None]
        hits    = [p for p in entries if p["correct"] >= 1]
        total   = sum(p.get("avg_win_eur", 0) or 0 for p in entries)
        win_pct  = 100 * len(wins) / len(entries) if entries else 0
        hit_pct  = 100 * len(hits) / len(entries) if entries else 0
        lines.append(f"| {name} | {len(entries)} | {len(hits)} | {hit_pct:.1f}% | {len(wins)} | {win_pct:.1f}% | €{total:.2f} |")
    return "\n".join(lines)


# ── Charts ────────────────────────────────────────────────────────────────────

def plot_wins_over_time(data: dict):
    players = all_players(data)
    dates   = _parse_dates(data["draws"])
    fig, ax = plt.subplots(figsize=(12, 5))
    for name in players:
        cum, total = [], 0
        for draw in data["draws"]:
            for p in draw["players"]:
                if p["name"] == name and p["win_class"] is not None:
                    total += 1
            cum.append(total)
        ax.plot(dates, cum, marker="o", markersize=3, label=name,
                color=_color(name, players), linewidth=2)
    ax.set_title("Cumulative Wins Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Total Wins")
    ax.legend(loc="upper left")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate(); ax.grid(True, alpha=0.3); fig.tight_layout()
    return fig


def plot_hits_over_time(data: dict):
    players = all_players(data)
    dates   = _parse_dates(data["draws"])
    fig, ax = plt.subplots(figsize=(12, 5))
    for name in players:
        cum, total = [], 0
        for draw in data["draws"]:
            for p in draw["players"]:
                if p["name"] == name and p["correct"] >= 1:
                    total += 1
            cum.append(total)
        ax.plot(dates, cum, marker="o", markersize=3, label=name,
                color=_color(name, players), linewidth=2)
    ax.set_title("Cumulative Hits Over Time (≥1 correct)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Total Hits")
    ax.legend(loc="upper left")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate(); ax.grid(True, alpha=0.3); fig.tight_layout()
    return fig


def plot_winnings_over_time(data: dict):
    players = all_players(data)
    dates   = _parse_dates(data["draws"])
    fig, ax = plt.subplots(figsize=(12, 5))
    for name in players:
        cum, total = [], 0.0
        for draw in data["draws"]:
            for p in draw["players"]:
                if p["name"] == name:
                    total += p.get("avg_win_eur", 0) or 0
            cum.append(total)
        ax.plot(dates, cum, marker="o", markersize=3, label=name,
                color=_color(name, players), linewidth=2)
    ax.set_title("Cumulative Winnings (€) Over Time", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Total € Won")
    ax.legend(loc="upper left")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    fig.autofmt_xdate()
    ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("€%.0f"))
    ax.grid(True, alpha=0.3); fig.tight_layout()
    return fig


def plot_win_class_distribution(data: dict):
    players     = all_players(data)
    class_keys  = sorted(WIN_CLASS_LABELS.keys())
    class_labels = [WIN_CLASS_LABELS[k] for k in class_keys]
    counts = {name: [0] * len(class_keys) for name in players}
    for draw in data["draws"]:
        for p in draw["players"]:
            if p["win_class"] in class_keys:
                counts[p["name"]][class_keys.index(p["win_class"])] += 1

    x     = np.arange(len(class_keys))
    width = 0.8 / max(len(players), 1)
    fig, ax = plt.subplots(figsize=(13, 5))
    for i, name in enumerate(players):
        offset = (i - len(players) / 2 + 0.5) * width
        ax.bar(x + offset, counts[name], width, label=name,
               color=_color(name, players), alpha=0.85)
    ax.set_title("Win Class Distribution per Player", fontsize=14, fontweight="bold")
    ax.set_xlabel("Win Class"); ax.set_ylabel("Count")
    ax.set_xticks(x); ax.set_xticklabels(class_labels, rotation=25, ha="right", fontsize=9)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(); ax.grid(True, axis="y", alpha=0.3); fig.tight_layout()
    return fig



def plot_win_rate_pie(data: dict):
    players = all_players(data)
    wins    = {n: 0 for n in players}
    for draw in data["draws"]:
        for p in draw["players"]:
            if p["name"] in wins and p["win_class"] is not None:
                wins[p["name"]] += 1
    labels = [n for n in players if wins[n] > 0]
    sizes  = [wins[n] for n in labels]
    colors = [_color(n, players) for n in labels]
    fig, ax = plt.subplots(figsize=(7, 7))
    _, _, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%",
                             startangle=140, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
    for t in autotexts:
        t.set_fontsize(10)
    ax.set_title("Share of Total Wins", fontsize=14, fontweight="bold")
    fig.tight_layout()
    return fig


def plot_3d_money_pie(data: dict):
    """
    Super-monstrous-fancy 3D pie chart.
    Shows total €, win count, win-rate %, entries, AND current streak all at once.
    Do not question it.
    """
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    players = all_players(data)

    # ── gather per-player stats ───────────────────────────────────────────────
    stats = {}
    for name in players:
        entries = [p for d in data["draws"] for p in d["players"] if p["name"] == name]
        wins    = [p for p in entries if p["win_class"] is not None]
        total_eur = sum(p.get("avg_win_eur", 0) or 0 for p in entries)
        # current active win streak
        cur_streak = 0
        for p in reversed(entries):
            if p["win_class"] is not None:
                cur_streak += 1
            else:
                break
        stats[name] = {
            "eur":        total_eur,
            "wins":       len(wins),
            "entries":    len(entries),
            "win_pct":    100 * len(wins) / len(entries) if entries else 0,
            "cur_streak": cur_streak,
        }

    # size slices by total € won; fallback to entry count if nobody won anything
    sizes_raw = [stats[n]["eur"] for n in players]
    if sum(sizes_raw) == 0:
        sizes_raw = [stats[n]["entries"] for n in players]
        pie_metric = "entries"
    else:
        pie_metric = "€ won"

    total   = sum(sizes_raw)
    colors  = [_color(n, players) for n in players]

    # ── figure setup ─────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 9))
    fig.patch.set_facecolor("#0d0d0d")
    ax  = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#0d0d0d")

    depth   = 0.35
    explode = 0.12
    theta1  = 0.0
    slices  = []   # store midpoints for annotation arrows

    for name, size, color in zip(players, sizes_raw, colors):
        frac   = size / total if total else 1 / len(players)
        theta2 = theta1 + 2 * np.pi * frac
        theta  = np.linspace(theta1, theta2, 200)
        mid    = (theta1 + theta2) / 2
        ex     = explode * np.cos(mid)
        ey     = explode * np.sin(mid)

        # ── top face ─────────────────────────────────────────────────────────
        xs = np.concatenate([[ex], ex + np.cos(theta), [ex]])
        ys = np.concatenate([[ey], ey + np.sin(theta), [ey]])
        for z_val, alpha in [(depth, 0.95), (0.0, 0.55)]:
            ax.plot_surface(
                xs.reshape(1, -1).repeat(2, axis=0),
                ys.reshape(1, -1).repeat(2, axis=0),
                np.full((2, len(xs)), z_val),
                color=color, alpha=alpha, shade=True,
            )

        # ── side wall ────────────────────────────────────────────────────────
        wall_x = np.array([ex + np.cos(theta)] * 2)
        wall_y = np.array([ey + np.sin(theta)] * 2)
        wall_z = np.array([np.zeros_like(theta), np.full_like(theta, depth)])
        ax.plot_surface(wall_x, wall_y, wall_z, color=color, alpha=0.80, shade=True)

        # ── edge highlight on top rim ─────────────────────────────────────────
        ax.plot(ex + np.cos(theta), ey + np.sin(theta),
                np.full_like(theta, depth + 0.002),
                color="white", linewidth=0.6, alpha=0.5)

        slices.append((name, mid, ex, ey, frac))
        theta1 = theta2

    # ── annotation labels (outside the pie, with leader lines) ───────────────
    for name, mid, ex, ey, frac in slices:
        s     = stats[name]
        r_tip = 1.18          # where the leader line ends
        r_txt = 1.30          # where the text starts
        lx    = ex + r_tip * np.cos(mid)
        ly    = ey + r_tip * np.sin(mid)
        tx    = ex + r_txt * np.cos(mid)
        ty    = ey + r_txt * np.sin(mid)
        z_mid = depth + 0.04

        # leader line
        ax.plot([ex + 0.98 * np.cos(mid), lx],
                [ey + 0.98 * np.sin(mid), ly],
                [z_mid, z_mid],
                color="white", linewidth=0.8, alpha=0.7)

        ha  = "left" if np.cos(mid) >= 0 else "right"
        pct_str = f"{frac*100:.1f}%"
        label = (
            f"{name}\n"
            f"{'─'*14}\n"
            f"€ {s['eur']:.0f}  ({pct_str})\n"
            f"🏆 {s['wins']} wins / {s['entries']} draws\n"
            f"📈 {s['win_pct']:.1f}% win-rate\n"
            f"🔥 streak: {s['cur_streak']}"
        )
        ax.text(tx, ty, z_mid, label,
                ha=ha, va="center", fontsize=7.5,
                color="white", fontfamily="monospace",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#1a1a2e",
                          edgecolor=_color(name, players), linewidth=1.2, alpha=0.88))

    # ── centre title embossed on the pie ─────────────────────────────────────
    ax.text(0, 0, depth + 0.01, "💸", ha="center", va="bottom",
            fontsize=22, zorder=20)

    ax.set_xlim(-2.1, 2.1)
    ax.set_ylim(-2.1, 2.1)
    ax.set_zlim(0, depth * 4)
    ax.set_axis_off()
    ax.view_init(elev=32, azim=-55)

    fig.suptitle(
        "💸  Extremely Professional Financial Overview  💸\n"
        f"Sliced by: {pie_metric}  |  labels: €, wins, entries, win-rate, active streak",
        fontsize=11, fontweight="bold", color="white", y=0.97,
    )
    fig.text(
        0.5, 0.01,
        "* avg prize values used  •  past performance ≠ future results  •  "
        "please gamble responsibly  •  this chart is legally a work of art",
        ha="center", fontsize=6.5, color="#888888", style="italic",
    )
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    return fig


def plot_avg_correct_per_player(data: dict):
    players = all_players(data)
    avgs, stds = [], []
    for name in players:
        vals = [p["correct"] for d in data["draws"] for p in d["players"] if p["name"] == name]
        avgs.append(np.mean(vals) if vals else 0)
        stds.append(np.std(vals) if vals else 0)
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [_color(n, players) for n in players]
    bars   = ax.bar(players, avgs, yerr=stds, capsize=5, color=colors, alpha=0.85,
                    error_kw={"elinewidth": 1.5})
    ax.set_title("Avg Correct Numbers per Player (±1 std dev)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Avg Correct"); ax.set_ylim(0, 6.5)
    ax.axhline(np.mean(avgs), color="gray", linestyle="--", linewidth=1,
               label=f"Overall avg {np.mean(avgs):.2f}")
    ax.legend()
    for bar, avg in zip(bars, avgs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                f"{avg:.2f}", ha="center", va="bottom", fontsize=9)
    ax.grid(True, axis="y", alpha=0.3); fig.tight_layout()
    return fig


def plot_streak(data: dict):
    """Best consecutive prize-winning streak and worst losing streak per player."""
    players = all_players(data)
    win_streaks, lose_streaks = [], []
    for name in players:
        entries = [
            1 if p["win_class"] is not None else 0
            for d in data["draws"] for p in d["players"] if p["name"] == name
        ]
        best_w = best_l = cur_w = cur_l = 0
        for e in entries:
            if e:
                cur_w += 1; cur_l = 0
            else:
                cur_l += 1; cur_w = 0
            best_w = max(best_w, cur_w)
            best_l = max(best_l, cur_l)
        win_streaks.append(best_w)
        lose_streaks.append(best_l)

    x, width = np.arange(len(players)), 0.35
    fig, ax  = plt.subplots(figsize=(10, 5))
    bars_w   = ax.bar(x - width / 2, win_streaks,  width, label="Best win streak",   color="#59a14f", alpha=0.85)
    bars_l   = ax.bar(x + width / 2, lose_streaks, width, label="Worst lose streak", color="#e15759", alpha=0.85)
    ax.set_title("Best Prize-Win & Worst Lose Streak per Player", fontsize=13, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(players); ax.set_ylabel("Draws")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(); ax.grid(True, axis="y", alpha=0.3)
    for bars, color in [(bars_w, "#59a14f"), (bars_l, "#e15759")]:
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.1, str(int(h)),
                        ha="center", va="bottom", fontsize=9, fontweight="bold", color=color)
    fig.tight_layout()
    return fig


def plot_hit_streak(data: dict):
    """Best consecutive streak of hitting at least 1 correct number per player."""
    players = all_players(data)
    hit_streaks, miss_streaks = [], []
    for name in players:
        entries = [
            1 if p["correct"] >= 1 else 0
            for d in data["draws"] for p in d["players"] if p["name"] == name
        ]
        best_h = best_m = cur_h = cur_m = 0
        for e in entries:
            if e:
                cur_h += 1; cur_m = 0
            else:
                cur_m += 1; cur_h = 0
            best_h = max(best_h, cur_h)
            best_m = max(best_m, cur_m)
        hit_streaks.append(best_h)
        miss_streaks.append(best_m)

    x, width = np.arange(len(players)), 0.35
    fig, ax  = plt.subplots(figsize=(10, 5))
    bars_h   = ax.bar(x - width / 2, hit_streaks,  width, label="Best hit streak (≥1 correct)",  color="#4e79a7", alpha=0.85)
    bars_m   = ax.bar(x + width / 2, miss_streaks, width, label="Worst miss streak (0 correct)", color="#f28e2b", alpha=0.85)
    ax.set_title("Best Hit & Worst Miss Streak per Player  (≥1 correct = hit)", fontsize=13, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(players); ax.set_ylabel("Draws")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(); ax.grid(True, axis="y", alpha=0.3)
    for bars, color in [(bars_h, "#4e79a7"), (bars_m, "#f28e2b")]:
        for bar in bars:
            h = bar.get_height()
            if h > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, h + 0.1, str(int(h)),
                        ha="center", va="bottom", fontsize=9, fontweight="bold", color=color)
    fig.tight_layout()
    return fig


# ── Aggregator ────────────────────────────────────────────────────────────────

def generate_all_plots(data: dict) -> tuple:
    return (
        stats_overview(data),
        plot_wins_over_time(data),
        plot_hits_over_time(data),
        plot_winnings_over_time(data),
        plot_win_class_distribution(data),
        plot_win_rate_pie(data),
        plot_3d_money_pie(data),
        plot_avg_correct_per_player(data),
        plot_streak(data),
        plot_hit_streak(data),
    )

