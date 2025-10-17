from ..my_imports import *
from .text_general import *

__all__ = ["Title_Presentation"]


class Title_Presentation(Text_General, VGroup):
    """
    Generate presentation title slides with hierarchical text styling.

    This class creates a title group containing the presentation title, affiliation,
    and author information, each styled with decreasing font sizes to create a
    visual hierarchy. An optional background decorator can be applied.

    :param content: A list containing presentation information in order:
        1. The presentation title
        2. Institution/affiliation
        3. Author name(s)
    :type content: list[str]

    :param kwargs: Additional parameters passed to :class:`Text_General`.

    .. note::

       The title text automatically scales to fit the frame width with appropriate margins.
       Font sizes decrease progressively: title (2x), affiliation (1.5x), author (1x).

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_beanim import *

        class Title_Slide_Test(Scene):
            def construct(self):
                tp = Title_Presentation(
                    content=[
                        "This is a Title Presentation",
                        "Your institution",
                        "Your name"
                    ]
                )
                self.add(tp)

    :seealso: :class:`Text_General`
    """

    def __init__(self, **kwargs) -> VGroup:
        super().__init__(**kwargs)

        self.text_group = VGroup(*[
            Tex(self.content[i], font_size=(2-0.5*i) * self.text_size, color=self.text_color)
            for i in range(len(self.content))
        ]).arrange(DOWN, buff=0.4)

        self.text_group.scale_to_fit_width(config.frame_width - 3)
        self.add_decorator(self.text_group)
