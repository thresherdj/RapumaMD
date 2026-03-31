"""Built-in macros available in all RapumaMD documents."""

from datetime import date


def today(*_args) -> str:
    """@today() — inserts the current date as YYYY-MM-DD."""
    return date.today().isoformat()


def pagebreak(*_args) -> str:
    """@pagebreak() — inserts a LaTeX page break."""
    return r"\newpage"


BUILTINS = {
    "today": today,
    "pagebreak": pagebreak,
}
