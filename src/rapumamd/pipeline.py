"""Orchestrates the full render pipeline: preprocess → render."""

from pathlib import Path

from .config import load_config
from .front_matter import get_rapuma_overrides, strip_front_matter
from .preprocessor import preprocess
from .renderer import render


def _merge(base: dict, overrides: dict) -> dict:
    """Deep merge overrides into base, returning a new dict."""
    merged = {k: dict(v) if isinstance(v, dict) else v for k, v in base.items()}
    for section, values in overrides.items():
        if isinstance(values, dict):
            merged.setdefault(section, {}).update(values)
        else:
            merged[section] = values
    return merged


def run(md_path: Path, output_path: Path | None = None):
    project_dir = md_path.parent
    config = load_config(project_dir)
    config = _merge(config, get_rapuma_overrides(md_path))

    if output_path is None:
        output_path = md_path.with_suffix(".pdf")
    else:
        output_path.parent.mkdir(parents=True, exist_ok=True)

    source = md_path.read_text(encoding="utf-8")
    source = strip_front_matter(source)
    source = preprocess(source, project_dir)
    render(source, config, output_path)

    return output_path
