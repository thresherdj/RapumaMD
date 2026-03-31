from .builtins import BUILTINS


def get_macro(name: str, project_dir):
    """Look up a macro by name. Project-local macros override builtins."""
    local = _load_local_macros(project_dir)
    if name in local:
        return local[name]
    if name in BUILTINS:
        return BUILTINS[name]
    return None


def _load_local_macros(project_dir) -> dict:
    """Load macros.py from the project directory if it exists."""
    from pathlib import Path
    import importlib.util

    macros_file = Path(project_dir) / "macros.py"
    if not macros_file.exists():
        return {}

    spec = importlib.util.spec_from_file_location("project_macros", macros_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return {
        name: fn
        for name, fn in vars(module).items()
        if callable(fn) and not name.startswith("_")
    }
