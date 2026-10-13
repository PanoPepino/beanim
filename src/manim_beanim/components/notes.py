"""Themed post-it notes with resource-safe SVG loading."""
from ._types import ColorLike, TextContent
from manim import Group, SVGMobject, BulletedList, UP, RIGHT, LEFT
from ..themes.styles import Styled, NOTE_DEFAULTS
from ..rendering.layout import fit_within
from ..themes.provider import resolve_style, get_active_theme
from ..data.dictionaries import svg_resource
from ..rendering.text import text_pieces, template_for
__all__ = ['Post_It']

class Post_It(Styled, Group):
    theme_role = 'post_it'

    def __init__(self, to_dos: TextContent, text_color: ColorLike | None = None, text_size: float | None = None, pin_color: ColorLike | None = None, *, max_width: float | None = None, max_height: float | None = None, **kwargs) -> None:
        tasks = text_pieces(to_dos)
        theme = get_active_theme()
        style = resolve_style('post_it', NOTE_DEFAULTS,
            dict(text_color=text_color, text_size=text_size, pin_color=pin_color), theme=theme)
        self._install_style(style, theme)
        super().__init__(**kwargs)
        with svg_resource('post_it.svg') as file:
            post = SVGMobject(str(file)).set_z_index(-1).scale(2)
        with svg_resource('pin.svg') as file:
            pin = SVGMobject(str(file)).scale(0.2).next_to(post, UP, buff=-0.1).shift(0.2 * RIGHT)
        pin.set_color(self.pin_color)
        args = dict(color=self.text_color, font_size=self.text_size, buff=0.3, dot_scale_factor=2)
        template = template_for(self.theme)
        if template is not None:
            args['tex_template'] = template
        td = BulletedList(*tasks, **args)
        fit_within(td, post.width - 0.4 if max_width is None else min(max_width, post.width - 0.4),
                   post.height - 1.2 if max_height is None else min(max_height, post.height - 1.2))
        td.next_to(post.get_left(), RIGHT, aligned_edge=LEFT, buff=0.2).shift(0.5 * UP)
        self.post_it = Group(post, td, pin)
        self.add(self.post_it)
