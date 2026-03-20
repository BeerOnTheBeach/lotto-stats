"""
Lotto Tipp-Gemeinschaft – Web UI
Run: python app.py
"""

import os
import gradio as gr

from ui.constants import LOCKED_COL_CSS
from ui.tabs import data_tab, stats_tab, import_tab

with gr.Blocks(title="🎰 Lotto Tipp-Gemeinschaft", css=LOCKED_COL_CSS) as demo:
    gr.Markdown("# 🎰 Lotto Tipp-Gemeinschaft – 6aus49")

    with gr.Tabs():
        with gr.TabItem("📋 Data"):
            data_tab.build(demo)

        with gr.TabItem("📈 Statistics"):
            stats_tab.build()

        with gr.TabItem("📂 Import CSV"):
            import_tab.build()

if __name__ == "__main__":
    port = int(os.environ.get("GRADIO_SERVER_PORT", 7861))
    demo.launch(theme=gr.themes.Soft(), server_port=port)

