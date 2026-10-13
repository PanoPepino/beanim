"""Presentation selection and validated per-object style resolution."""
from .styles import normalize_style
_active_theme = None
_UNSET = object()

def get_active_theme():
    return _active_theme

def set_active_theme(theme) -> None:
    global _active_theme
    _active_theme = theme

def resolve_style(role: str, defaults, overrides, *, theme=_UNSET) -> dict:
    if theme is _UNSET:
        theme = get_active_theme()
    values = dict(defaults)
    if theme is not None:
        values.update({key: getattr(theme, key) for key in ('text_size', 'text_color') if key in values})
        if role not in {'table', 'photo', 'post_it'}:
            values.update(theme.styles.get('text', {}))
        values.update(theme.styles.get(role, {}))
    values.update({key: value for key, value in overrides.items() if value is not None})
    return normalize_style(values, role=role)
