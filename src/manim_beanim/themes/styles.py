"""Validated, immutable style snapshots and legacy attribute access."""
from collections.abc import Mapping, Iterator
from dataclasses import dataclass
from numbers import Real
from types import MappingProxyType
import math
import numpy as np
from manim import ManimColor, WHITE, RED, BLUE, GREEN

TEXT_DEFAULTS = dict(direction=(1, 0, 0), aligned_direction=(0, 0, 0), text_size=35,
    text_color=WHITE, decorator_presence='no', decorator_color=WHITE,
    decorator_stroke_width=1, corner_rad=0, corner_rad_direction=(0, 0, 0, 0),
    fill_opa=0, tightness=0.3, stroke_opa=1, dot_scale=1)
TABLE_DEFAULTS = dict(highlight_top='yes', text_size=55, text_color=WHITE,
    decorator_presence='box', decorator_color=WHITE, decorator_color_2=RED,
    decorator_color_3=BLUE, decorator_color_4=GREEN, decorator_stroke_width=1,
    corner_rad=0.1, corner_rad_direction=(1, 1, 1, 1), fill_opa=0.1,
    h_tightness=0.5, v_tightness=0.5, tightness=0, stroke_opa=1, stroke_color=WHITE)
PHOTO_DEFAULTS = dict(decorator_style='techno', text_size=35, text_color=WHITE,
    decorator_color=WHITE, pin_color=WHITE, corner_rad=0, decorator_stroke_w=1)
NOTE_DEFAULTS = dict(text_color='#000000', text_size=35, pin_color=WHITE)
ROLE_FIELDS = {role: frozenset(TEXT_DEFAULTS) for role in
    ('text', 'presentation_title', 'section_title', 'bullets', 'reference', 'equation', 'underbar')}
ROLE_FIELDS.update(table=frozenset(TABLE_DEFAULTS), photo=frozenset(PHOTO_DEFAULTS),
                   post_it=frozenset(NOTE_DEFAULTS))
ROLE_FIELDS = MappingProxyType(ROLE_FIELDS)
DECORATORS = frozenset({'no', 'box', 'box_long_left', 'box_long_right', 'back_frame'})

def finite_number(value, field: str, *, minimum: float = 0, positive: bool = False) -> float:
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f'{field} must be a finite number')
    if not math.isfinite(value) or (value <= minimum if positive else value < minimum):
        comparison = 'greater than' if positive else 'at least'
        raise ValueError(f'{field} must be finite and {comparison} {minimum}')
    return float(value)

def normalize_flag(value) -> bool:
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, str) and value in {'yes', 'no'}:
        return value == 'yes'
    raise ValueError("highlight_top must be bool or 'yes'/'no'")

def normalize_style(values: Mapping, *, role: str | None = None) -> dict:
    if not isinstance(values, Mapping):
        raise ValueError('Style must be a mapping')
    allowed = ROLE_FIELDS.get(role) if role is not None else frozenset().union(*ROLE_FIELDS.values())
    if allowed is None:
        raise ValueError(f'Unknown theme role: {role}')
    unknown = set(values) - allowed
    if unknown:
        raise ValueError(f'Unknown style fields: {sorted(unknown, key=str)}')
    result = {}
    for field, value in values.items():
        if 'color' in field:
            if value is None:
                raise ValueError(f'{field} must be a valid color')
            try:
                value = str(ManimColor(value))
            except (TypeError, ValueError) as error:
                raise ValueError(f'Invalid {field}: {value!r}') from error
        elif field in {'text_size', 'dot_scale'}:
            value = finite_number(value, field, positive=True)
        elif field in {'fill_opa', 'stroke_opa'}:
            value = finite_number(value, field)
            if value > 1:
                raise ValueError(f'{field} must lie between 0 and 1')
        elif field in {'corner_rad', 'decorator_stroke_width', 'decorator_stroke_w',
                       'tightness', 'h_tightness', 'v_tightness'}:
            value = finite_number(value, field)
        elif field in {'direction', 'aligned_direction', 'corner_rad_direction'}:
            try:
                vector = np.asarray(value, dtype=float)
            except (ValueError, TypeError) as error:
                raise ValueError(f'{field} must contain finite numbers') from error
            size = 4 if field == 'corner_rad_direction' else 3
            if vector.shape != (size,) or not np.isfinite(vector).all():
                raise ValueError(f'{field} must be a finite {size}-dimensional vector')
            if field == 'direction' and not np.any(vector):
                raise ValueError('direction must be nonzero')
            if field == 'corner_rad_direction' and (vector < 0).any():
                raise ValueError('corner_rad_direction must contain nonnegative weights')
            value = tuple(float(item) for item in vector)
        elif field == 'decorator_presence':
            supported = {'no', 'box'} if role == 'table' else DECORATORS
            if not isinstance(value, str) or value not in supported:
                raise ValueError(f'decorator_presence must be one of {sorted(supported)}')
        elif field == 'decorator_style':
            if not isinstance(value, str) or value not in {'techno', 'polaroid'}:
                raise ValueError('decorator_style must be techno or polaroid')
        elif field == 'highlight_top':
            value = normalize_flag(value)
        result[field] = value
    return result

@dataclass(frozen=True, init=False)
class StyleSpec(Mapping):
    _values: Mapping

    def __init__(self, values: Mapping):
        object.__setattr__(self, '_values', MappingProxyType(normalize_style(values)))

    @classmethod
    def _from_normalized(cls, values: Mapping):
        record = cls.__new__(cls)
        object.__setattr__(record, '_values', MappingProxyType(dict(values)))
        return record

    def __getitem__(self, key: str):
        return self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __deepcopy__(self, memo):
        copy = type(self).__new__(type(self))
        object.__setattr__(copy, '_values', self._values)
        memo[id(self)] = copy
        return copy

    def __reduce__(self):
        return (type(self), (dict(self),))

    def updated(self, **changes):
        return type(self)._from_normalized({**self, **normalize_style(changes)})

class Styled:
    """One source of styling state. Attribute assignments validate new snapshots."""

    @property
    def style(self) -> StyleSpec:
        return self._style

    def _install_style(self, values: Mapping, theme) -> None:
        self._style = StyleSpec._from_normalized(values)
        self.theme = theme

def _style_property(field):
    def get(owner):
        if field not in owner._style:
            raise AttributeError(f'{type(owner).__name__} has no {field} style')
        value = owner._style[field]
        return np.array(value, copy=True) if field in {'direction', 'aligned_direction'} else value
    def set_value(owner, value):
        changes = normalize_style({field: value}, role=getattr(owner, 'theme_role', None))
        owner._style = owner._style.updated(**changes)
    return property(get, set_value)

for _field in frozenset().union(*ROLE_FIELDS.values()) - {'stroke_color'}:
    setattr(Styled, _field, _style_property(_field))

# Shared defaults contain immutable primitives only; constructors never mutate them.
TEXT_DEFAULTS = MappingProxyType(normalize_style(TEXT_DEFAULTS, role='text'))
TABLE_DEFAULTS = MappingProxyType(normalize_style(TABLE_DEFAULTS, role='table'))
PHOTO_DEFAULTS = MappingProxyType(normalize_style(PHOTO_DEFAULTS, role='photo'))
NOTE_DEFAULTS = MappingProxyType(normalize_style(NOTE_DEFAULTS, role='post_it'))
