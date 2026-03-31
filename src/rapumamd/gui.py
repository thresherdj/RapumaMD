"""Tkinter settings editor for per-document rapuma config overrides."""

import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from .front_matter import get_rapuma_overrides, set_rapuma_overrides
from .config import load_config
from .settings_schema import SETTINGS_SCHEMA
from .pipeline import run as run_pipeline


def _get_effective_value(section: str, key: str, overrides: dict, base_config: dict) -> str:
    """Return the current value for a setting: override → rapuma.toml → ''."""
    override_val = overrides.get(section, {}).get(key)
    if override_val is not None:
        return str(override_val)
    base_val = base_config.get(section, {}).get(key)
    if base_val is not None:
        return str(base_val)
    return ""


def run_settings_gui(md_path: Path):
    md_path = md_path.resolve()
    project_dir = md_path.parent

    base_config = load_config(project_dir)
    overrides = get_rapuma_overrides(md_path)

    root = tk.Tk()
    root.title(f"Settings — {md_path.name}")
    root.geometry("520x600")

    # ── Header ────────────────────────────────────────────────────────────────
    header = tk.Frame(root, bg="#2b2b2b", padx=12, pady=8)
    header.pack(fill="x")
    tk.Label(
        header,
        text=f"Document overrides: {md_path.name}",
        bg="#2b2b2b", fg="white",
    ).pack(anchor="w")
    tk.Label(
        header,
        text="Empty fields use rapuma.toml defaults. Set a value to override.",
        bg="#2b2b2b", fg="#aaaaaa",
    ).pack(anchor="w")

    # ── Scrollable area ────────────────────────────────────────────────────────
    outer = tk.Frame(root)
    outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer, borderwidth=0, highlightthickness=0)
    scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    form_frame = tk.Frame(canvas)
    canvas_window = canvas.create_window((0, 0), window=form_frame, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_canvas_configure(event):
        canvas.itemconfig(canvas_window, width=event.width)

    form_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    # Mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # ── Settings form (grid layout) ────────────────────────────────────────────
    form_frame.columnconfigure(0, weight=0, minsize=160)
    form_frame.columnconfigure(1, weight=0)
    form_frame.columnconfigure(2, weight=1)

    sections = {}
    for entry in SETTINGS_SCHEMA:
        sections.setdefault(entry["section"], []).append(entry)

    widgets = {}
    row_idx = 0

    for section, entries in sections.items():
        # Section header
        tk.Label(
            form_frame,
            text=section.upper(),
            font=("TkHeadingFont", 10, "bold"),
            fg="#444444",
            pady=6,
        ).grid(row=row_idx, column=0, columnspan=3, sticky="w", padx=12, pady=(14, 0))
        row_idx += 1

        ttk.Separator(form_frame, orient="horizontal").grid(
            row=row_idx, column=0, columnspan=3, sticky="ew", padx=12, pady=(0, 6)
        )
        row_idx += 1

        for entry in entries:
            # Label + optional hint
            label_frame = tk.Frame(form_frame)
            label_frame.grid(row=row_idx, column=0, sticky="nw", padx=(12, 4), pady=3)

            tk.Label(label_frame, text=entry["label"], anchor="w").pack(anchor="w")

            if entry.get("hint"):
                tk.Label(
                    label_frame,
                    text=entry["hint"],
                    fg="#888888",
                    wraplength=150,
                    justify="left",
                    anchor="w",
                ).pack(anchor="w")

            current = _get_effective_value(section, entry["key"], overrides, base_config)
            var = tk.StringVar(value=current)
            widgets[(section, entry["key"])] = var

            if entry["type"] == "choice":
                ttk.Combobox(
                    form_frame,
                    textvariable=var,
                    values=[""] + entry["choices"],
                    width=26,
                    state="readonly",
                ).grid(row=row_idx, column=1, sticky="w", padx=(4, 4), pady=3)
            else:
                tk.Entry(
                    form_frame,
                    textvariable=var,
                    width=28,
                ).grid(row=row_idx, column=1, sticky="w", padx=(4, 4), pady=3)

            # Column 2: show the effective default grayed out
            toml_val = base_config.get(section, {}).get(entry["key"])
            schema_default = entry.get("default", "")
            effective_default = str(toml_val) if toml_val is not None else schema_default

            if effective_default:
                tk.Label(
                    form_frame,
                    text=effective_default,
                    fg="#888888",
                    anchor="w",
                ).grid(row=row_idx, column=2, sticky="w", padx=(8, 12), pady=3)

            row_idx += 1

    # ── Buttons ────────────────────────────────────────────────────────────────
    btn_frame = tk.Frame(root, padx=12, pady=10)
    btn_frame.pack(fill="x", side="bottom")

    def _collect_overrides() -> dict:
        new_overrides = {}
        for (section, key), var in widgets.items():
            val = var.get().strip()
            schema_entry = next(
                e for e in SETTINGS_SCHEMA if e["section"] == section and e["key"] == key
            )
            base_val = str(base_config.get(section, {}).get(key, schema_entry.get("default", "")))
            if val and val != base_val:
                new_overrides.setdefault(section, {})[key] = val
        return new_overrides

    def save():
        set_rapuma_overrides(md_path, _collect_overrides())
        messagebox.showinfo("Saved", f"Overrides saved to {md_path.name}")

    def render():
        set_rapuma_overrides(md_path, _collect_overrides())
        try:
            output = run_pipeline(md_path)
            subprocess.Popen(["xdg-open", str(output)])
        except (ValueError, RuntimeError) as e:
            messagebox.showerror("Render failed", str(e))

    def clear_all():
        for (section, key), var in widgets.items():
            schema_entry = next(
                e for e in SETTINGS_SCHEMA if e["section"] == section and e["key"] == key
            )
            base_val = str(base_config.get(section, {}).get(key, schema_entry.get("default", "")))
            var.set(base_val)

    def open_md_help():
        subprocess.Popen(["google-chrome", "https://pandoc.org/MANUAL.html#pandocs-markdown"])

    ttk.Button(btn_frame, text="Render", command=render).pack(side="right", padx=(4, 0))
    ttk.Button(btn_frame, text="Save", command=save).pack(side="right", padx=(4, 0))
    ttk.Button(btn_frame, text="Close", command=root.destroy).pack(side="right", padx=(4, 0))
    ttk.Button(btn_frame, text="Clear Overrides", command=clear_all).pack(side="right")
    ttk.Button(btn_frame, text="MD Help", command=open_md_help).pack(side="left")

    # Center on screen
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()
