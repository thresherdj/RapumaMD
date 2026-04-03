# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

RapumaMD is a system-wide CLI tool that renders Markdown files to PDF via pandoc + XeLaTeX. It supports `@macro_name(args)` inline macros and per-project `rapuma.toml` config files.

## Commands

```bash
# Install / reinstall after code changes
pipx install -e .

# Render a document
rapumamd render path/to/document.md
rapumamd render path/to/document.md --out path/to/output.pdf

# Open Tkinter GUI to edit per-document settings (writes to front matter)
rapumamd settings path/to/document.md
```

After rendering, the CLI automatically opens the PDF with `xdg-open`. The default output path is `<source>.pdf` in the **same directory** as the source file (not an `output/` subdirectory) unless `--out` is specified.

The `settings` command only saves overrides to front matter — it does not render. Run `rapumamd render` separately afterward.

## Pipeline

```
document.md → preprocessor.py → renderer.py (pandoc + xelatex) → PDF
```

1. `config.py` — loads `rapuma.toml` from the document's directory
2. `front_matter.py` — parses YAML front matter; extracts `rapuma` key as per-doc overrides
3. `pipeline.py` — deep-merges configs (front matter > rapuma.toml), strips front matter, calls preprocess then render
4. `preprocessor.py` — expands `@macro_name(args)` patterns
5. `renderer.py` — calls pandoc via subprocess, passes preprocessed markdown via stdin

## Config Hierarchy

Per-document front matter overrides project-wide `rapuma.toml` via deep merge:

```
front matter rapuma key  >  rapuma.toml  >  built-in defaults
```

**`rapuma.toml`** — project-wide, lives in the document's directory:

```toml
[document]
title = "My Document"
author = "Dennis Drescher"
date = "2026-03-24"
# Note: [document] keys are not currently passed to pandoc (see Known gap above)

[latex]
engine = "xelatex"
paper = "letter"
fontsize = "11pt"
watermark = "DRAFT"   # injected via \usepackage{draftwatermark}, not passed as -V
# Any other key/value pairs under [latex] are passed directly as pandoc -V variables
# e.g. margin-left = "1in"
```

**Front matter** — per-document overrides inside the `.md` file itself:

```yaml
---
rapuma:
  document:
    title: My Specific Doc
  latex:
    fontsize: 12pt
    margin-top: 1in
---
```

New `[latex]` fields automatically flow through to pandoc as `-V key=value` — no code changes needed. The canonical list of known settings (used by both GUI and docs) is in `settings_schema.py`.

**Known gap:** The `[document]` section (title, author, date) is loaded and merged but **never passed to pandoc** — `renderer.py` extracts `doc` from config but doesn't use it. Title/author/date must currently be set as standard pandoc metadata directly in the markdown body or via pandoc's `-M` flags if needed.

## Macro System

Macros are Python functions that return a string substituted into the document.

- **Built-ins** live in `src/rapumamd/macros/builtins.py` and are registered in `BUILTINS`
- **Project-local macros** live in `macros.py` in the document's directory — these override built-ins; all non-private callables are auto-exposed

`src/rapumamd/macros/__init__.py` handles lookup (local → builtins). Unknown macros raise `ValueError`.

Macro syntax: `@name` or `@name(arg1, arg2)`. Built-ins: `@today()`, `@pagebreak()`.

## Dependencies

- Python 3.11+, pandoc 3.1.3, XeLaTeX (TeX Live 2023)
- `click`, `pyyaml` (only non-stdlib dependencies)

## Tests

There are no tests in this codebase. `TestMDs/` contains sample documents used for manual render testing.

## Placeholders

`filters/` and `templates/` directories exist but are empty — intended for future custom pandoc filters and templates.
