from ..my_imports import *
from .text_general import *

__all__ = ["Underbar"]


class Underbar(Text_General, VGroup):
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

    def __init__(self, **kwargs) -> VGroup:

        super().__init__(**kwargs)

        self.text_down = VGroup(*[
            Tex(self.content[i], font_size=0.45*self.text_size, color=self.text_color)
            for i in range(len(self.content))
        ]).arrange(RIGHT, buff=12/len(self.content))
        self.text_down.to_corner(DOWN, buff=0.07)
        self.add_decorator(self.text_down)

    def add_decorator(self, mobject):
        print("add_decorator overriden")
        mobject.set_z_index(5)
        self.rectangle = Rectangle(
            height=mobject.get_height() + 0.8*self.tightness,
            width=config.frame_width + 0.1,
            stroke_width=self.decorator_stroke_width,
            color=self.decorator_color,
            fill_opacity=self.fill_opa,
            stroke_opacity=self.stroke_opa)
        self.rectangle.move_to([0, mobject.get_y(), 0])
        return self.add(mobject, self.rectangle)
