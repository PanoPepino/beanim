from ..rendering.text import render_text, text_pieces
from manim import Animation, BulletedList, LEFT, Transform, SurroundingRectangle, UL, UP, VGroup, linear
from collections.abc import Callable
from numbers import Integral
from ..themes.styles import finite_number
from ..rendering.layout import replace_rendered
from .base import Text_General
__all__ = ['BlB']

class BlB(Text_General):
    """
    Create a styled bulleted list with optional title and animation features.

    This class inherits from :class:`Text_General` and allows creation of animated bulleted lists for use in Manim scene constructions. Each bullet point can be highlighted individually using the :meth:`next_point` method.

    :param content: List of bullet points to display.
    :type content: list[str]

    :param the_title: Optional title displayed above the bulleted list.
    :type the_title: str, optional

    :param kwargs: Additional arguments passed to :class:`Text_General`.

    .. note::

       Use :meth:`next_point` to iterate through bullet points with animation effects.
       Each call highlights the current point and dims the others.

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_beanim import *

        class BlB_Test(Scene):
            def construct(self):
                important_points = BlB(
                    content=[
                        "This is a bulleted list with a title",
                        "Use .next_point() to iterate over points",
                        "The final point restores all to original color"
                    ],
                    the_title="This is a title for the bulleted list"
                ).to_corner(LEFT).shift(UP)

                important_points_2 = BlB(
                    content=[
                        "This is a bulleted list without a title",
                        "Use .next_point() to iterate",
                        "Observe the different corner style"
                    ]
                ).next_to(important_points, DOWN, aligned_edge=LEFT)

                self.add(important_points, important_points_2)
                for _ in range(len(important_points) + 3):
                    self.play(important_points.next_point())

    :seealso: :class:`Text_General`
    """
    theme_role = 'bullets'

    def __init__(self, the_title: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.content = text_pieces(self.content)
        self.the_title = the_title
        self.order_list = BulletedList(*self.content, font_size=self.text_size, buff=self.tightness, stroke_color=self.text_color, dot_scale_factor=self.dot_scale, **{'tex_template': self.tex_template.copy()} if self.tex_template is not None else {})
        self.order_list.set_color(self.text_color)
        self.count = 0
        if self.the_title is None:
            self.add_decorator(self.order_list)
        else:
            self.add_title_and_box(self.the_title, self.order_list)

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, Integral) or value < 0:
            raise ValueError("count must be a nonnegative integer")
        self._count = int(value)

    def add_title_and_box(self, title_on_top: str, points: BulletedList) -> None:
        """
        Add both title box and bullet points with appropriate decorative styling.

        Creates a title box with rounded top corners and a points box with rounded bottom corners,
        positioning them to create a unified visual element.

        :param title_on_top: The title text to display above the bullet points.
        :type title_on_top: str

        :param points: The BulletedList object containing the bullet points.
        :type points: BulletedList
        """
        up_title = render_text(title_on_top, self, size=1.3 * self.text_size).set_z_index(5)
        title_box = SurroundingRectangle(up_title, corner_radius=[self.crad, 0, 0, self.crad], buff=0.7 * self.tightness, stroke_width=self.decorator_stroke_width, color=self.decorator_color, fill_opacity=min(1, self.fill_opa + 0.1), stroke_opacity=self.stroke_opa)
        points_box = SurroundingRectangle(points, corner_radius=[0, self.crad, self.crad, self.crad], buff=self.tightness, stroke_width=self.decorator_stroke_width, color=self.decorator_color, fill_opacity=self.fill_opa, stroke_opacity=self.stroke_opa)
        box_up = VGroup(up_title, title_box)
        box_up.next_to(points_box.get_corner(UL), aligned_edge=LEFT, buff=0).shift(1.2 * (self.tightness + 0.1) * UP)
        replace_rendered(self, (up_title, title_box, points_box, points))
        self.box_up = box_up

    def next_point(self, rf: Callable[[float], float] = linear, rt: float = 1) -> Animation:
        """Highlight next bullet, then restore all. Every step lasts ``rt`` seconds.

        Building an animation never advances count. Queued steps choose their
        bullet on begin and advance count after successful completion. Exhausted
        steps retain appearance for the requested duration.
        """
        rt = finite_number(rt, 'rt', positive=True)
        if not callable(rf):
            raise ValueError('rf must be a callable rate function')
        return _BulletStep(self, run_time=rt, rate_func=rf)

class _BulletStep(Transform):
    """Resolve target at playback, allowing steps to be queued or discarded."""

    def __init__(self, owner: BlB, **kwargs) -> None:
        self.owner = owner
        self._step = None
        self._committed = False
        super().__init__(owner.order_list, **kwargs)

    def create_target(self) -> BulletedList:
        self._step = self.owner.count
        target = self.mobject.copy()
        if self._step < len(target):
            target.set_opacity(0.2)
            target[self._step].set_opacity(1)
        elif self._step == len(target):
            target.set_opacity(1)
        return target

    def finish(self) -> None:
        super().finish()
        if not self._committed and self._step is not None and self._step <= len(self.mobject):
            self.owner.count = self._step + 1
            self._committed = True
