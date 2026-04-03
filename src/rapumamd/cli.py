import shutil
import subprocess
import sys
from pathlib import Path

import click

from .pipeline import run
from .gui import run_settings_gui


def _show_error(message: str):
    """Show an error to the user via stderr or a GUI dialog if no TTY."""
    if sys.stderr.isatty():
        click.echo(f"Error: {message}", err=True)
    else:
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("RapumaMD Error", message)
            root.destroy()
        except Exception:
            click.echo(f"Error: {message}", err=True)


@click.group()
def main():
    """RapumaMD — Markdown to PDF publishing tool."""


@main.command()
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@click.option("--out", "-o", type=click.Path(path_type=Path), default=None,
              help="Output PDF path (default: <source>.pdf alongside the source file)")
def render(source: Path, out: Path | None):
    """Render a markdown file to PDF."""
    try:
        output = run(source, out)
        click.echo(f"Written: {output}")
    except (ValueError, RuntimeError) as e:
        _show_error(str(e))
        sys.exit(1)

    xdg_open = shutil.which("xdg-open")
    if xdg_open is None:
        _show_error(f"PDF written to {output} but xdg-open was not found — cannot open automatically.")
        return

    result = subprocess.run([xdg_open, str(output)])
    if result.returncode != 0:
        _show_error(f"PDF written to {output} but xdg-open failed to open it (exit code {result.returncode}).")


@main.command()
@click.argument("source", type=click.Path(exists=True, path_type=Path))
def settings(source: Path):
    """Open the settings GUI for a markdown document."""
    run_settings_gui(source)
