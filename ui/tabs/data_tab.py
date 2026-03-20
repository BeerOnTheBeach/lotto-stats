"""
Tab 1 – Data: inline-editable table, save, delete, add.
"""

import gradio as gr

from ui.constants import TABLE_HEADERS, TABLE_DATATYPE, TABLE_COL_WIDTHS, WIN_CLASS_EUR
from ui.helpers import (
    load, save, all_players, win_class_for, player_entry,
    build_table_rows, fmt_date_iso, tdata_row, tdata_len,
)


def build(demo: gr.Blocks) -> gr.Dataframe:
    """Render Tab 1 inside an already-open gr.Blocks context."""

    gr.Markdown(
        "### All entries\n"
        "Click any cell in the **Correct** or **SZ** column to change it directly — "
        "then hit **💾 Save changes** when you're done. "
        "The other columns update themselves automatically, no need to touch them. "
        "To remove a row, click it to select it and then hit **🗑 Delete row**."
    )

    table = gr.Dataframe(
        headers=TABLE_HEADERS,
        datatype=TABLE_DATATYPE,
        interactive=True,
        wrap=False,
        column_count=(8, "fixed"),
        column_widths=TABLE_COL_WIDTHS,
        elem_classes=["lotto-table"],
    )

    with gr.Row():
        refresh_btn = gr.Button("🔄 Refresh", variant="secondary")
        save_btn    = gr.Button("💾 Save changes", variant="primary")
        delete_btn  = gr.Button("🗑 Delete row", variant="stop")

    gr.Markdown("---")
    gr.Markdown("#### ➕ Add new entry")
    with gr.Row():
        add_date    = gr.Textbox(label="Date (DD.MM.YYYY)", placeholder="25.03.2026")
        add_player  = gr.Textbox(label="Player name")
        add_correct = gr.Slider(0, 6, step=1, value=0, label="Correct numbers")
        add_sz      = gr.Checkbox(label="Super number")
        add_btn     = gr.Button("Add", variant="primary")

    status_msg   = gr.Textbox(label="Status", interactive=False)
    selected_row = gr.State(None)

    # ── handlers ──────────────────────────────────────────────────────────────

    def on_select(evt: gr.SelectData, _cur):
        return evt.index[0]

    def do_save(tdata):
        data    = load()
        changed = 0
        for i in range(tdata_len(tdata)):
            row = tdata_row(tdata, i)
            try:
                di, pi = int(row[6]), int(row[7])
            except (ValueError, TypeError):
                continue
            p = data["draws"][di]["players"][pi]
            try:
                new_correct = max(0, min(6, int(float(str(row[2])))))
            except (ValueError, TypeError):
                new_correct = p["correct"]
            new_sz = str(row[3]).strip().lower() in ("✓", "1", "true", "yes")
            if new_correct != p["correct"] or new_sz != p["super_number"]:
                p["correct"]     = new_correct
                p["super_number"] = new_sz
                wc               = win_class_for(new_correct, new_sz)
                p["win_class"]   = wc
                p["avg_win_eur"] = WIN_CLASS_EUR.get(wc, 0.0) if wc else 0.0
                changed += 1
        save(data)
        msg = f"✅ Saved – {changed} row(s) updated." if changed else "ℹ️ No changes detected."
        return msg, build_table_rows(load()), None

    def do_delete(sel, tdata):
        if sel is None:
            return "⚠ Click a row first, then delete.", build_table_rows(load()), None
        row = tdata_row(tdata, int(sel))
        try:
            di, pi = int(row[6]), int(row[7])
        except (ValueError, TypeError):
            return "⚠ Could not identify row.", build_table_rows(load()), None
        data = load()
        del data["draws"][di]["players"][pi]
        data["draws"] = [d for d in data["draws"] if d["players"]]
        save(data)
        return "✅ Row deleted.", build_table_rows(load()), None

    def do_add(dt, name, correct, sz):
        if not dt or not name:
            return "⚠ Date and player name required.", build_table_rows(load())
        dt    = fmt_date_iso(dt)
        data  = load()
        entry = player_entry(name.strip(), int(correct), bool(sz))
        for draw in data["draws"]:
            if draw["date"] == dt:
                for p in draw["players"]:
                    if p["name"] == entry["name"]:
                        return f"⚠ {name} already has an entry for {dt}.", build_table_rows(data)
                draw["players"].append(entry)
                break
        else:
            data["draws"].append({"date": dt, "players": [entry]})
            data["draws"].sort(key=lambda d: d["date"])
        save(data)
        return f"✅ Added {name} for {dt}.", build_table_rows(load())

    def do_refresh():
        return build_table_rows(load()), None, ""

    # ── wiring ─────────────────────────────────────────────────────────────────

    table.select(on_select, inputs=[selected_row], outputs=[selected_row])

    save_btn.click(do_save,
        inputs=[table],
        outputs=[status_msg, table, selected_row])

    delete_btn.click(do_delete,
        inputs=[selected_row, table],
        outputs=[status_msg, table, selected_row])

    add_btn.click(do_add,
        inputs=[add_date, add_player, add_correct, add_sz],
        outputs=[status_msg, table])

    refresh_btn.click(do_refresh,
        outputs=[table, selected_row, status_msg])

    # populate on startup
    demo.load(lambda: build_table_rows(load()), outputs=[table])

    return table

