"""Beanim public API. Named imports load only their required implementation."""
from importlib import import_module
from typing import TYPE_CHECKING
from .__version__ import __version__ as __version__
if TYPE_CHECKING:
    from .components.titles_section import Title_Section as Title_Section
    from .components.titles_presentation import Title_Presentation as Title_Presentation
    from .components.bullets import BlB as BlB
    from .components.references import Reference as Reference
    from .components.base import Text_General as Text_General
    from .components.equations import Equation as Equation
    from .components.underbar import Underbar as Underbar
    from .components.photos import Photo as Photo
    from .components.notes import Post_It as Post_It
    from .components.tables import Table as Table
    from .templates.color_scheme import import_template_beanim as import_template_beanim
    from .tools.extract_eq_from_tex import extract_equations as extract_equations
    from .tools.extract_refs_from_bib import extract_citation as extract_citation
    from .themes.application import apply_theme as apply_theme
    from .themes.presets import get_theme as get_theme
    from .themes.models import Theme as Theme
_EXPORTS = {'Title_Section': 'components.titles_section', 'Title_Presentation': 'components.titles_presentation', 'BlB': 'components.bullets', 'Reference': 'components.references', 'Text_General': 'components.base', 'Equation': 'components.equations', 'Underbar': 'components.underbar', 'Photo': 'components.photos', 'Post_It': 'components.notes', 'Table': 'components.tables', 'import_template_beanim': 'templates.color_scheme', 'extract_equations': 'tools.extract_eq_from_tex', 'extract_citation': 'tools.extract_refs_from_bib', 'apply_theme': 'themes.application', 'get_theme': 'themes.presets', 'Theme': 'themes.models'}
__all__ = list(_EXPORTS)

def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError(f'{__name__} has no attribute {name!r}')
    value = getattr(import_module('.' + _EXPORTS[name], __name__), name)
    globals()[name] = value
    return value

def __dir__():
    return sorted(set(globals()) | set(__all__))
