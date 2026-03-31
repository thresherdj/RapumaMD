import tomllib
from pathlib import Path


def load_config(project_dir: Path) -> dict:
    config_path = project_dir / "rapuma.toml"
    if not config_path.exists():
        return {}
    with open(config_path, "rb") as f:
        return tomllib.load(f)
