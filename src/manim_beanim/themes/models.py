"""Immutable preset values, independent of Manim component classes."""
from dataclasses import dataclass
from types import MappingProxyType
from collections.abc import Mapping
from numbers import Real
import math

def freeze(value):
    if hasattr(value, 'tolist'):
        return freeze(value.tolist())
    if isinstance(value, Mapping):
        return MappingProxyType({key: freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple((freeze(item) for item in value))
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError('Theme configuration must contain data values, not mutable objects')

@dataclass(frozen=True)
class Theme:
    name: str
    background_color: str
    tex_font: str
    text_size: float
    text_color: str
    styles: Mapping
    text_font: str = ''

    def __post_init__(self):
        for field in ('name', 'background_color', 'tex_font', 'text_color', 'text_font'):
            if not isinstance(getattr(self, field), str):
                raise ValueError(f'{field} must be a string')
        if not self.name or not self.tex_font:
            raise ValueError('Theme name and tex_font must be nonempty')
        if isinstance(self.text_size, bool) or not isinstance(self.text_size, Real) or not math.isfinite(self.text_size) or self.text_size <= 0:
            raise ValueError('Theme text size must be positive and finite')
        if not isinstance(self.styles, Mapping) or not all(isinstance(key, str) and isinstance(value, Mapping) for key, value in self.styles.items()):
            raise ValueError('Theme styles must map role names to style mappings')
        object.__setattr__(self, 'styles', freeze(self.styles))

    def __deepcopy__(self, memo):
        # Immutable theme snapshots can be shared by independently copied mobjects.
        memo[id(self)] = self
        return self

    def __reduce__(self):
        def thaw(value):
            if isinstance(value, Mapping):
                return {key: thaw(item) for key, item in value.items()}
            if isinstance(value, tuple):
                return tuple(thaw(item) for item in value)
            return value
        return (type(self), (self.name, self.background_color, self.tex_font,
                            self.text_size, self.text_color, thaw(self.styles), self.text_font))
