"""
Tab 2 – Statistics: all charts loaded on demand.
"""

import gradio as gr

from ui.helpers import load
from ui.charts import generate_all_plots


def build() -> None:
    """Render Tab 2 inside an already-open gr.Blocks context."""

    stats_refresh_btn = gr.Button("🔄 Load / Refresh Stats", variant="primary", size="lg")

    summary_md = gr.Markdown()

    gr.Markdown("---")
    gr.Markdown("### 🏆 Cumulative Wins Over Time");          plot_wins_time  = gr.Plot()
    gr.Markdown("### 🎱 Cumulative Hits Over Time (≥1 correct)"); plot_hits_time = gr.Plot()
    gr.Markdown("### 💶 Cumulative Winnings (€) Over Time");  plot_eur_time  = gr.Plot()
    gr.Markdown("### 🥇 Win Class Distribution");             plot_wc_dist   = gr.Plot()
    gr.Markdown("### 🍕 Share of Total Wins");                plot_pie       = gr.Plot()
    gr.Markdown("### 💸 Extremely Professional Financial Overview"); plot_3d_pie = gr.Plot()
    gr.Markdown("### 🎯 Avg Correct Numbers per Player");     plot_avg_corr  = gr.Plot()
    gr.Markdown("### 🔥 Prize Streaks (win class required)"); plot_streaks   = gr.Plot()
    gr.Markdown("### 🎱 Hit Streaks (≥1 correct)");          plot_hit_streak = gr.Plot()

    def on_refresh():
        return generate_all_plots(load())

    stats_refresh_btn.click(
        on_refresh,
        outputs=[
            summary_md,
            plot_wins_time,
            plot_hits_time,
            plot_eur_time,
            plot_wc_dist,
            plot_pie,
            plot_3d_pie,
            plot_avg_corr,
            plot_streaks,
            plot_hit_streak,
        ],
    )
