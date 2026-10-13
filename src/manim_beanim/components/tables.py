"""Validated tables with transactional rebuilding and isolated input data."""
from ._types import ColorLike, DictionarySource, TableRows, VectorLike
from copy import deepcopy
from collections.abc import Mapping
import math
from manim import VGroup, Mobject, MathTable, SurroundingRectangle
from ..themes.provider import resolve_style, get_active_theme
from ..themes.styles import Styled, TABLE_DEFAULTS
from ..data.dictionaries import read_dictionary, split_dictionary_path, check_file_exists
from ..rendering.text import template_for
from ..rendering.layout import replace_rendered
__all__ = ['Table']

class Table(Styled, VGroup):
    """Table from rows or dictionary key; explicit options override active theme.

    highlight_top accepts booleans and legacy 'yes'/'no'. Inputs are copied.
    Rebuilding replaces owned content and preserves user-added children.
    """
    theme_role = 'table'

    def __init__(self, content: str | TableRows | None = None, dictionary: DictionarySource | None = None, highlight_top: bool | str | None = None, text_size: float | None = None,
                 text_color: ColorLike | None = None, decorator_presence: str | None = None, decorator_color: ColorLike | None = None,
                 decorator_color_2: ColorLike | None = None, decorator_color_3: ColorLike | None = None, decorator_color_4: ColorLike | None = None,
                 decorator_stroke_width: float | None = None, corner_rad: float | None = None, corner_rad_direction: VectorLike | None = None,
                 fill_opa: float | None = None, h_tightness: float | None = None, v_tightness: float | None = None, tightness: float | None = None,
                 stroke_opa: float | None = None, *, stroke_color: ColorLike | None = None, **kwargs) -> None:
        if 'the_dictionary' in kwargs:
            if dictionary is not None:
                raise TypeError('Provide dictionary or the_dictionary, not both')
            dictionary = kwargs.pop('the_dictionary')
        overrides = dict(highlight_top=highlight_top, text_size=text_size, text_color=text_color,
            decorator_presence=decorator_presence, decorator_color=decorator_color,
            decorator_color_2=decorator_color_2, decorator_color_3=decorator_color_3,
            decorator_color_4=decorator_color_4, decorator_stroke_width=decorator_stroke_width,
            corner_rad=corner_rad, corner_rad_direction=corner_rad_direction, fill_opa=fill_opa,
            h_tightness=h_tightness, v_tightness=v_tightness, tightness=tightness,
            stroke_opa=stroke_opa, stroke_color=stroke_color)
        theme = get_active_theme()
        values = resolve_style(self.theme_role, TABLE_DEFAULTS, overrides, theme=theme)
        if stroke_color is None and not (theme and 'stroke_color' in theme.styles.get('table', {})):
            values['stroke_color'] = values['text_color']
        self._install_style(values, theme)
        super().__init__(**kwargs)
        self.content = deepcopy(content)
        self.dictionary = deepcopy(dict(dictionary)) if isinstance(dictionary, Mapping) else dictionary
        self.tex_template = template_for(theme)
        self._dictionary = None
        if dictionary is None:
            self.handle_no_dictionary()
        else:
            self.handle_with_dictionary()

    @property
    def crad(self) -> float:
        return self.corner_rad

    @crad.setter
    def crad(self, value: float) -> None:
        self.corner_rad = value

    @property
    def corner_rad_all(self) -> list[float]:
        return [self.corner_rad * weight for weight in self.corner_rad_direction]

    @staticmethod
    def _validated_rows(rows) -> tuple[tuple[str, ...], ...]:
        if not isinstance(rows, (list, tuple)) or not rows:
            raise ValueError('Table requires nonempty rows')
        if not all(isinstance(row, (list, tuple)) and row for row in rows):
            raise ValueError('Table rows must be nonempty sequences')
        if len({len(row) for row in rows}) != 1:
            raise ValueError('Table rows must have equal length')
        for row in rows:
            for cell in row:
                if isinstance(cell, bool) or not isinstance(cell, (str, int, float)):
                    raise ValueError('Table cells must be strings or finite numbers')
                if isinstance(cell, float) and not math.isfinite(cell):
                    raise ValueError('Table cells must be strings or finite numbers')
        return tuple(tuple(str(cell) for cell in row) for row in rows)

    def _validate_rows(self) -> None:
        self._rows = self._validated_rows(self._rows)

    def _build(self, rows: tuple[tuple[str, ...], ...]) -> Mobject:
        entry = dict(font_size=self.text_size, color=self.text_color)
        if self.tex_template is not None:
            entry['tex_template'] = self.tex_template.copy()
        return MathTable([list(row) for row in rows], element_to_mobject_config=entry,
            line_config=dict(stroke_width=self.decorator_stroke_width, color=self.style['stroke_color']),
            include_outer_lines=False, v_buff=self.v_tightness, h_buff=self.h_tightness,
            stroke_opacity=self.stroke_opa)

    def _highlight(self, table, columns: int) -> None:
        old = getattr(table, '_beanim_highlights', ())
        table.remove(*old)
        highlights = []
        colors = (self.decorator_color_2, self.decorator_color_3, self.decorator_color_4)
        for column in range(columns):
            corners = (int(column == 0), 0, 0, int(column == columns - 1))
            before = tuple(table.submobjects)
            table.add_highlighted_cell((1, column + 1), color=colors[column % len(colors)],
                corner_radius=[self.corner_rad * weight for weight in corners])
            highlights.extend(obj for obj in table.submobjects if obj not in before)
        table._beanim_highlights = tuple(highlights)

    def _decorated(self, table, rows) -> tuple[Mobject, ...]:
        if self.highlight_top:
            self._highlight(table, len(rows[0]))
        if self.decorator_presence == 'box':
            return (table, SurroundingRectangle(table, corner_radius=self.corner_rad_all,
                buff=4 * self.tightness, stroke_width=self.decorator_stroke_width,
                color=self.decorator_color, fill_opacity=self.fill_opa, stroke_opacity=self.stroke_opa))
        return (table,)

    def _render(self, rows, dictionary=None) -> None:
        rows = self._validated_rows(rows)
        table = self._build(rows)
        objects = self._decorated(table, rows)
        replace_rendered(self, objects)
        self._rows, self.chosen_content, self._dictionary = rows, table, dictionary

    def handle_no_dictionary(self) -> None:
        self._render(self.content if self.dictionary is None else self._rows, self._dictionary)

    def handle_with_dictionary(self, dic_in_data_base='tables') -> None:
        if dic_in_data_base != 'tables':
            raise ValueError('Table dictionary kind must be tables')
        if not isinstance(self.content, str):
            raise ValueError('Dictionary-backed table content must be a key string')
        dictionary = self.load_dictionary()
        if self.content not in dictionary:
            raise KeyError(f'Missing tables key: {self.content}')
        self._render(dictionary[self.content], dictionary)

    def load_dictionary(self) -> dict:
        return read_dictionary(self.dictionary, 'tables')

    def filter_type(self) -> list[str]:
        return list(self._rows[0])

    def add_highlight_top_row(self) -> None:
        self._highlight(self.chosen_content, len(self._rows[0]))

    def add_decorator(self, mobject: Mobject) -> None:
        replace_rendered(self, self._decorated(mobject, self._rows))

    def split_dictionary_path(self, input_string) -> list[str]:
        return split_dictionary_path(input_string)

    def check_file_exists(self, directory, filename) -> bool:
        return check_file_exists(directory, filename)
