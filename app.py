"""
Lotto Tipp-Gemeinschaft – Web UI
Run: python app.py
"""

import os
import gradio as gr

from ui.constants import LOCKED_COL_CSS
from ui.tabs import data_tab, stats_tab, import_tab

# Force dark mode regardless of system/browser preference
FORCE_DARK_JS = "document.documentElement.classList.add('dark');"

with gr.Blocks(title="🎰 Lotto Tipp-Gemeinschaft", css=LOCKED_COL_CSS, js=FORCE_DARK_JS) as demo:
    gr.Markdown("# 🎰 Lotto Tipp-Gemeinschaft – 6aus49")

    with gr.Tabs():
        with gr.TabItem("📋 Data"):
            table = data_tab.build(demo)

        with gr.TabItem("📈 Statistics"):
            stats_tab.build()

        with gr.TabItem("📂 Import CSV"):
            import_tab.build(table)

if __name__ == "__main__":
    port = int(os.environ.get("GRADIO_SERVER_PORT", 7861))
    demo.launch(server_port=port)
