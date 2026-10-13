from ..rendering.text import render_text, text_pieces
from manim import DOWN, VGroup, config
from .base import Text_General
from ..rendering.layout import fit_within
__all__ = ['Title_Presentation']

class Title_Presentation(Text_General):
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
    theme_role = 'presentation_title'

    def __init__(self, *, max_width: float | None = None, max_height: float | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.content = text_pieces(self.content)
        self.text_group = VGroup(*[render_text(self.content[i], self, size=max(1, (2 - 0.5 * i) * self.text_size)) for i in range(len(self.content))]).arrange(DOWN, buff=0.4)
        fit_within(self.text_group, config.frame_width - 3 if max_width is None else max_width,
                   config.frame_height - 2 * self.tightness - 0.4 if max_height is None else max_height)
        self.add_decorator(self.text_group)
