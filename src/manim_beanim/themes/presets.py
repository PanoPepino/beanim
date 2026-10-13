"""Eight data-only themes. Reading presets never changes render defaults."""
import json
from importlib.resources import files
from .models import Theme
PRESETS = json.loads(files(__package__).joinpath('presets.json').read_text(encoding='utf-8'))
THEMES = {name: Theme(**values) for name, values in PRESETS.items()}

def get_theme(value: str | Theme) -> Theme:
    if isinstance(value, Theme):
        return value
    try:
        return THEMES[value]
    except (KeyError, TypeError):
        raise ValueError(f"Unknown theme {value!r}. Choose from {', '.join(THEMES)}") from None
