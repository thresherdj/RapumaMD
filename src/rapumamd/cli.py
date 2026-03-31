import subprocess
import sys
from pathlib import Path

import click

from .pipeline import run
from .gui import run_settings_gui


@click.group()
def main():
    """RapumaMD — Markdown to PDF publishing tool."""


@main.command()
@click.argument("source", type=click.Path(exists=True, path_type=Path))
@click.option("--out", "-o", type=click.Path(path_type=Path), default=None,
              help="Output PDF path (default: output/<source>.pdf)")
def render(source: Path, out: Path | None):
    """Render a markdown file to PDF."""
    try:
        output = run(source, out)
        click.echo(f"Written: {output}")
        subprocess.Popen(["xdg-open", str(output)])
    except (ValueError, RuntimeError) as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("source", type=click.Path(exists=True, path_type=Path))
def settings(source: Path):
    """Open the settings GUI for a markdown document."""
    run_settings_gui(source)
