from ..rendering.text import render_text, text_pieces
from manim import Mobject, DOWN, RIGHT, Rectangle, VGroup, config
from .base import Text_General
from ..rendering.layout import replace_rendered
__all__ = ['Underbar']

class Underbar(Text_General):
    """
    Create a bar in the lower part of the slide with several information to be chosen by the author. The information will be rearranged to properly fit in the slide bottom part.

    :param content: A LaTeX string or a list of strings.
    :type content: str or list[str]

    :seealso: :class:`Text_General`

    .. note::

        - The content to be displayed is up to decision of the author. Author, affiliation, name of the talk, date, where the talk given... These are some of choices.

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_beanim import *

        class Underbar_Test(Scene):
            def construct(self):
                under = Underbar(content=["Pano Pepino", "Some University", "My talk in the Mooon",
                      "30th February 2050"])
                self.add(under)
    """
    theme_role = 'underbar'

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.content = text_pieces(self.content)
        self.text_down = VGroup(*[render_text(self.content[i], self, size=0.45 * self.text_size) for i in range(len(self.content))]).arrange(RIGHT, buff=max(0.1, (config.frame_width - 2) / len(self.content)))
        if self.text_down.width > config.frame_width - 0.5:
            self.text_down.scale_to_fit_width(config.frame_width - 0.5)
        self.text_down.to_corner(DOWN, buff=0.07)
        self.add_decorator(self.text_down)

    def add_decorator(self, mobject: Mobject) -> None:
        mobject.set_z_index(5)
        rectangle = Rectangle(height=mobject.height + 0.8 * self.tightness, width=config.frame_width + 0.1, stroke_width=self.decorator_stroke_width, color=self.decorator_color, fill_opacity=self.fill_opa, stroke_opacity=self.stroke_opa)
        rectangle.move_to([0, mobject.get_y(), 0])
        replace_rendered(self, (mobject, rectangle))
        self.rectangle = rectangle
