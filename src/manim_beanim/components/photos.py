"""Photo frames using source-resolution clipping and bundled pin resources."""
from os import PathLike
import numpy as np
from ._types import ColorLike
from manim import Group, ImageMobject, RoundedRectangle, SurroundingRectangle, Cutout, SVGMobject, Tex, WHITE, UP, RIGHT, DOWN, config
from ..themes.styles import Styled, PHOTO_DEFAULTS
from ..rendering.layout import fit_within
from ..themes.provider import resolve_style, get_active_theme
from ..data.dictionaries import svg_resource
from ..rendering.text import template_for
from ..rendering.images import clip_image_to_mobject
__all__ = ['Photo']

class Photo(Styled, Group):
    theme_role = 'photo'

    def __init__(self, photo: str | PathLike[str] | np.ndarray, decorator_style: str | None = None, caption: str = '', text_size: float | None = None, text_color: ColorLike | None = None, decorator_color: ColorLike | None = None, pin_color: ColorLike | None = None, corner_rad: float | None = None, decorator_stroke_w: float | None = None, **kwargs) -> None:
        overrides = dict(decorator_style=decorator_style, text_size=text_size,
            text_color=text_color, decorator_color=decorator_color, pin_color=pin_color,
            corner_rad=corner_rad, decorator_stroke_w=decorator_stroke_w)
        theme = get_active_theme()
        style = resolve_style('photo', PHOTO_DEFAULTS, overrides, theme=theme)
        if not isinstance(caption, str):
            raise TypeError('caption must be a string')
        self._install_style(style, theme)
        super().__init__(**kwargs)
        image = ImageMobject(photo)
        if self.decorator_style == 'polaroid':
            outer = RoundedRectangle(width=2, height=2.9, corner_radius=self.corner_rad / 2)
            inner = RoundedRectangle(width=1.8, height=2.1, corner_radius=self.corner_rad / 2).shift(0.3 * UP)
            polaroid = Cutout(outer, inner, fill_opacity=1, color=WHITE, stroke_color=self.decorator_color, stroke_width=3 * self.decorator_stroke_w)
            image.scale_to_fit_height(inner.height)
            if image.width < inner.width:
                image.scale_to_fit_width(inner.width)
            image.move_to(inner)
            clip = clip_image_to_mobject(image, inner).set_z_index(-10)
            frame = SurroundingRectangle(inner, color=self.decorator_color, stroke_width=self.decorator_stroke_w, buff=0)
            with svg_resource('pin.svg') as file:
                pin = SVGMobject(str(file)).scale(0.2).next_to(outer, UP, buff=-0.05).shift(0.2 * RIGHT)
            pin.set_color(self.pin_color)
            items = [polaroid, clip, frame, pin]
            if caption:
                args = dict(font_size=self.text_size, color=self.text_color)
                template = template_for(self.theme)
                if template is not None:
                    args['tex_template'] = template
                label = Tex(caption, **args)
                fit_within(label, inner.width, 0.45)
                items.append(label.next_to(clip, DOWN, buff=0.2).set_z_index(4))
        else:
            image.scale_to_fit_height(config.frame_height)
            frame = SurroundingRectangle(image, corner_radius=self.corner_rad, color=self.decorator_color, stroke_width=3 * self.decorator_stroke_w, buff=-0.2)
            clip = clip_image_to_mobject(image, frame)
            items = [clip, frame]
        self.chosen_photo = Group(*items)
        self.add(self.chosen_photo)
