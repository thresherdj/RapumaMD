"""Expands @macro_name(args) calls in markdown source."""

import re
from pathlib import Path

from .macros import get_macro

# Matches @macro_name or @macro_name(arg1, arg2, ...)
_MACRO_RE = re.compile(r"@(\w+)(?:\(([^)]*)\))?")


def preprocess(source: str, project_dir: Path) -> str:
    def replace(match):
        name = match.group(1)
        raw_args = match.group(2) or ""
        args = [a.strip() for a in raw_args.split(",")] if raw_args.strip() else []

        macro = get_macro(name, project_dir)
        if macro is None:
            raise ValueError(f"Unknown macro: @{name}")
        return macro(*args)

    return _MACRO_RE.sub(replace, source)
