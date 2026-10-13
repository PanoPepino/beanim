"""Legacy theme selection delegates to the complete presentation-wide application."""
import warnings
from ..themes.application import apply_theme
from ..themes.presets import get_theme
__all__ = ['import_template_beanim']

def import_template_beanim(module_name: str, *, scene=None):
    """Apply theme to future objects; unknown legacy names fall back to default."""
    try:
        theme = get_theme(module_name)
    except ValueError:
        warnings.warn(f'Unknown theme {module_name!r}; using default_template', UserWarning, stacklevel=2)
        theme = get_theme('default_template')
    apply_theme(theme, scene=scene)
