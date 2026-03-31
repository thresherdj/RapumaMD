"""Invokes pandoc to render preprocessed markdown to PDF."""

import subprocess
import tempfile
import os
from pathlib import Path

_SKIP_AS_V_VAR = {"engine", "paper", "fontsize", "watermark"}


def _watermark_header(text: str) -> str:
    return (
        r"\usepackage{draftwatermark}" + "\n"
        r"\SetWatermarkText{" + text + "}\n"
        r"\SetWatermarkScale{1}" + "\n"
        r"\SetWatermarkColor[gray]{0.85}" + "\n"
    )


def render(md_source: str, config: dict, output_path: Path):
    doc = config.get("document", {})
    latex = config.get("latex", {})

    engine = latex.get("engine", "xelatex")
    paper = latex.get("paper", "letter")
    fontsize = latex.get("fontsize", "11pt")
    watermark = latex.get("watermark", "").strip()

    args = [
        "pandoc",
        "-f", "markdown",
        "-o", str(output_path),
        f"--pdf-engine={engine}",
        "-V", f"papersize={paper}",
        "-V", f"fontsize={fontsize}",
    ]

    # Pass any extra latex variables (margins, etc.) directly
    for key, value in latex.items():
        if key in _SKIP_AS_V_VAR:
            continue
        args += ["-V", f"{key}={value}"]

    # Write a temp header file for the watermark if requested
    tmp_header = None
    if watermark:
        tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False)
        tmp.write(_watermark_header(watermark))
        tmp.close()
        tmp_header = tmp.name
        args += ["--include-in-header", tmp_header]

    # Read from stdin so we render the preprocessed source
    args += ["--from=markdown", "-"]

    try:
        result = subprocess.run(args, input=md_source, text=True, capture_output=True)
    finally:
        if tmp_header:
            os.unlink(tmp_header)

    if result.returncode != 0:
        raise RuntimeError(f"pandoc error:\n{result.stderr}")
