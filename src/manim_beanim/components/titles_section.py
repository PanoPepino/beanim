from ..rendering.text import render_text
from manim import UL, config
from .base import Text_General
from ..rendering.layout import fit_within
__all__ = ['Title_Section']

class Title_Section(Text_General):
    """
    Create section titles positioned in the upper-left corner.

    This class generates section headers that are automatically positioned in the
    upper-left corner of the frame, typically used for slide section breaks or
    chapter headings in presentations.

    :param content: The section title text to display.
    :type content: str

    :param kwargs: Additional parameters passed to :class:`Text_General`.

    .. note::

       The title is automatically positioned using ``.to_corner(UL)`` and scaled
       to 1.5 times the base text size for emphasis.

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_beanim import *

        class Title_Section_Test(Scene):
            def construct(self):
                title_section = Title_Section(
                    content='This is a title section test'
                )
                self.add(title_section)

    :seealso: :class:`Text_General`
    """
    theme_role = 'section_title'

    def __init__(self, *, max_width: float | None = None, max_height: float | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.title = render_text(self.content, self, size=1.5 * self.text_size)
        fit_within(self.title, config.frame_width - 2 * self.tightness - 0.4 if max_width is None else max_width,
                   config.frame_height - 2 * self.tightness - 0.4 if max_height is None else max_height)
        self.title.to_corner(UL, buff=self.tightness + 0.2)
        self.add_decorator(self.title)
