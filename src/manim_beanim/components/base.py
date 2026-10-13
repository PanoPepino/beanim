from ._types import ColorLike, DictionarySource, TextContent, VectorLike
from copy import deepcopy
from ..themes.provider import resolve_style, get_active_theme
from ..data.dictionaries import read_dictionary, split_dictionary_path, check_file_exists
from ..rendering.text import render_text, text_pieces, template_for
from ..rendering.decorators import decorate
from manim import VGroup, Mobject
import numpy as np
from collections.abc import Mapping
from ..themes.styles import Styled, TEXT_DEFAULTS
from ..rendering.layout import replace_rendered
__all__ = ['Text_General']

class Text_General(Styled, VGroup):
    """
    Base class for all Beanim TeX-supporting rendering components.

    This class provides standardized behavior and styling for any derived classes that generate
    LaTeX-rendered content using Manim. It arranges and optionally decorates text content, with
    support for loading content from string literals or from dictionary sources.

    Subclasses may override rendering behavior while keeping the base logic for positioning,
    styling, and decoration.

    :param content: The primary text to display. May be either a string or list of strings.
        Strings should contain valid LaTeX. Each list entry will be rendered individually.
    :type content: str or list[str]

    :param dictionary: Optional path to a dictionary file used to resolve content labels
        into LaTeX code. If set to ``"data_base"``, a built-in library dictionary is used.
    :type dictionary: str, optional

    :param direction: Direction in which multiple entries will be stacked (e.g., ``RIGHT``, ``DOWN``).
    :type direction: np.ndarray

    :param aligned_direction: Alignment edge for stacked/arranged objects (e.g., ``LEFT``, ``UP``).
    :type aligned_direction: np.ndarray or list

    :param text_size: Font size of the rendered text content.
    :type text_size: float

    :param text_color: Manim color of the LaTeX text.
    :type text_color: ParsableManimColor

    :param decorator_presence: Type of decoration to apply. Options include:
        ``"box"``, ``"box_long_left"``, ``"box_long_right"``, ``"back_frame"``, ``"no"``.
    :type decorator_presence: str

    :param decorator_color: Outline or fill color used in decoration elements.
    :type decorator_color: ParsableManimColor

    :param decorator_stroke_width: Stroke width of the decorative borders.
    :type decorator_stroke_width: float

    :param corner_rad: Scalar used in combination with ``corner_rad_direction`` to round rectangle corners.
    :type corner_rad: float

    :param corner_rad_direction: List controlling corner rounding; format: [top-left, top-right, bottom-right, bottom-left].
    :type corner_rad_direction: list[int]

    :param fill_opa: Opacity for backgrounds (e.g., for surround boxes or frames).
    :type fill_opa: float

    :param tightness: Buffer/margin around the decorated content.
    :type tightness: float

    :param stroke_opa: Opacity of the border stroke around decorations.
    :type stroke_opa: float

    :param dot_scale: Scale of bullet points (used in subclasses like bullet lists).
    :type dot_scale: float

    :param kwargs: Other keyword arguments passed to Manim's :class:`VGroup`.

    :raises FileNotFoundError: If the given dictionary file path is invalid.
    :raises KeyError: If requested keys are not found in the dictionary.

    .. note::

       This class is not intended to be used directly in scenes, but rather subclassed to create content
       blocks like paragraphs, bullet points, or formulas. See subclasses like :class:`Equation` or
       :class:`BlB` for examples of how this class is used.

       To create your own dictionaries for content control, see the functions in the ``tools`` package,
       such as ``extract_pieces_from_bib()``.

    :seealso:
        - :class:`Equation`
        - :class:`BlB`
        - :class:`VGroup`
    """
    theme_role = 'text'
    dictionary_kind = None
    math_text = False

    def __init__(self, content: TextContent | None = None, dictionary: DictionarySource | None = None, direction: VectorLike | None = None, aligned_direction: VectorLike | None = None,
                 text_size: float | None = None, text_color: ColorLike | None = None, decorator_presence: str | None = None, decorator_color: ColorLike | None = None,
                 decorator_stroke_width: float | None = None, corner_rad: float | None = None, corner_rad_direction: VectorLike | None = None,
                 fill_opa: float | None = None, tightness: float | None = None, stroke_opa: float | None = None, dot_scale: float | None = None, **kwargs) -> None:
        if 'the_dictionary' in kwargs:
            if dictionary is not None:
                raise TypeError('Provide dictionary or the_dictionary, not both')
            dictionary = kwargs.pop('the_dictionary')
        if 'the_direction' in kwargs:
            if direction is not None:
                raise TypeError('Provide direction or the_direction, not both')
            direction = kwargs.pop('the_direction')
        overrides = dict(direction=direction, aligned_direction=aligned_direction,
            text_size=text_size, text_color=text_color, decorator_presence=decorator_presence,
            decorator_color=decorator_color, decorator_stroke_width=decorator_stroke_width,
            corner_rad=corner_rad, corner_rad_direction=corner_rad_direction, fill_opa=fill_opa,
            tightness=tightness, stroke_opa=stroke_opa, dot_scale=dot_scale)
        theme = get_active_theme()
        self._install_style(resolve_style(self.theme_role, TEXT_DEFAULTS, overrides, theme=theme), theme)
        super().__init__(**kwargs)
        self.content = deepcopy(content)
        self.dictionary = deepcopy(dict(dictionary)) if isinstance(dictionary, Mapping) else dictionary
        self.tex_template = template_for(theme)

    @property
    def corner_rad(self) -> list[float]:
        return list(self.style['corner_rad'] * np.array(self.corner_rad_direction))

    @corner_rad.setter
    def corner_rad(self, value: float) -> None:
        self._style = self._style.updated(corner_rad=value)

    @property
    def crad(self) -> float:
        return self.style['corner_rad']

    @crad.setter
    def crad(self, value: float) -> None:
        self.corner_rad = value

    def _render_pieces(self, pieces: list[str], *, buff: float) -> Mobject:
        rendered = [render_text(piece, self, math=self.math_text) for piece in pieces]
        if isinstance(self.content, (list, tuple)):
            return VGroup(*rendered).arrange(self.direction, aligned_edge=self.aligned_direction, buff=buff)
        return rendered[0]

    def handle_no_dictionary(self) -> None:
        content = self._render_pieces(text_pieces(self.content), buff=0.2)
        self.add_decorator(content)
        self.chosen_content = content

    def handle_with_dictionary(self, dic_in_data_base: str) -> None:
        data = self.load_dictionary() if dic_in_data_base == self.dictionary_kind else read_dictionary(self.dictionary, dic_in_data_base)
        pieces = text_pieces(self.content)
        for piece in pieces:
            if piece not in data:
                raise KeyError(f'Missing {dic_in_data_base} key: {piece}')
        # Keep get_tex_from_dict as subclass extension point.
        rendered = [self.get_tex_from_dict(piece, data) for piece in pieces]
        content = VGroup(*rendered).arrange(self.direction, aligned_edge=self.aligned_direction, buff=0.1) if isinstance(self.content, (list, tuple)) else rendered[0]
        self.add_decorator(content)
        self.dictionary_kind = dic_in_data_base
        self.chosen_content = content

    def load_dictionary(self) -> dict:
        return read_dictionary(self.dictionary, self.dictionary_kind)

    def get_tex_from_dict(self, the_piece: str, dictionary: Mapping) -> Mobject:
        if the_piece not in dictionary:
            raise KeyError(f'Missing {self.dictionary_kind or "dictionary"} key: {the_piece}')
        return render_text(dictionary[the_piece], self, math=self.math_text)

    def add_decorator(self, mobject: Mobject) -> None:
        objects = decorate(self, mobject)
        replace_rendered(self, objects)
        if self.decorator_presence in {'box_long_left', 'box_long_right'}:
            self.box_long = objects[-1]
        elif 'box_long' in self.__dict__:
            del self.box_long
        if self.decorator_presence == 'back_frame':
            self.rectangle = objects[-1]
        elif 'rectangle' in self.__dict__:
            del self.rectangle

    def split_dictionary_path(self, input_string) -> list[str]:
        return split_dictionary_path(input_string)

    def check_file_exists(self, directory, filename) -> bool:
        return check_file_exists(directory, filename)
