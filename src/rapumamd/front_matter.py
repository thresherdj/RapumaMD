"""Parse and write YAML front matter in markdown files."""

import re
from pathlib import Path

import yaml

_FENCE_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def read_front_matter(md_path: Path) -> dict:
    """Return the parsed front matter dict, or {} if none exists."""
    text = md_path.read_text(encoding="utf-8")
    match = _FENCE_RE.match(text)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def write_front_matter(md_path: Path, front_matter: dict):
    """Write (or replace) the front matter in a markdown file."""
    text = md_path.read_text(encoding="utf-8")
    body = _FENCE_RE.sub("", text, count=1)

    if front_matter:
        fm_text = yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
        new_text = f"---\n{fm_text}---\n{body}"
    else:
        new_text = body

    md_path.write_text(new_text, encoding="utf-8")


def strip_front_matter(source: str) -> str:
    """Remove the YAML front matter block from a markdown string."""
    return _FENCE_RE.sub("", source, count=1)


def get_rapuma_overrides(md_path: Path) -> dict:
    """Return only the rapuma-specific overrides from the front matter."""
    fm = read_front_matter(md_path)
    return fm.get("rapuma", {})


def set_rapuma_overrides(md_path: Path, overrides: dict):
    """Write rapuma overrides into the front matter, preserving other keys."""
    fm = read_front_matter(md_path)
    if overrides:
        fm["rapuma"] = overrides
    else:
        fm.pop("rapuma", None)
    write_front_matter(md_path, fm)
