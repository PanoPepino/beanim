from ..my_imports import *
from .text_general import *

__all__ = ["Title_Section"]


class Title_Section(Text_General, VGroup):
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
        from beanim import *

        class Title_Section_Test(Scene):
            def construct(self):
                title_section = Title_Section(
                    content='This is a title section test'
                )
                self.add(title_section)

    :seealso: :class:`Text_General`
    """

    def __init__(self, **kwargs) -> VGroup:
        super().__init__(**kwargs)

        self.title = Tex(self.content, font_size=1.5 * self.text_size, color=self.text_color)
        self.title.to_corner(UL)
        self.add_decorator(self.title)
