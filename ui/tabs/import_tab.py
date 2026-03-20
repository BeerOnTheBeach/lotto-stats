"""
Tab 3 – Import CSV: upload a CSV, convert to JSON, show summary.
"""

import shutil

import gradio as gr

from ui.helpers import load, all_players


def build() -> None:
    """Render Tab 3 inside an already-open gr.Blocks context."""

    gr.Markdown(
        "### Import from CSV\n"
        "Upload a `lotto.csv` file – it will be converted to `lotto.json` "
        "and **overwrite** the current data. Switch to the Data tab afterwards to review."
    )

    csv_upload     = gr.File(label="Upload lotto.csv", file_types=[".csv"], type="filepath")
    import_btn     = gr.Button("⚙️ Convert & Import", variant="primary")
    import_status  = gr.Textbox(label="Status", interactive=False)
    import_preview = gr.Markdown()

    def do_import(filepath):
        if filepath is None:
            return "⚠ No file selected.", ""
        from converter.csv_to_json import convert
        shutil.copy(filepath, "lotto.csv")
        try:
            convert("lotto.csv", "lotto.json")
        except Exception as e:
            return f"❌ Conversion failed: {e}", ""
        data     = load()
        n_draws  = len(data["draws"])
        n_entries = sum(len(d["players"]) for d in data["draws"])
        n_wins   = sum(1 for d in data["draws"] for p in d["players"] if p["win_class"] is not None)
        players  = all_players(data)
        preview  = (
            f"**✅ Import successful!**\n\n"
            f"- **Draws:** {n_draws}\n"
            f"- **Player entries:** {n_entries}\n"
            f"- **Prize-winning hits:** {n_wins}\n"
            f"- **Players found:** {', '.join(players)}"
        )
        return "✅ Done – switch to the Data tab to see the updated entries.", preview

    import_btn.click(
        do_import,
        inputs=[csv_upload],
        outputs=[import_status, import_preview],
    )

