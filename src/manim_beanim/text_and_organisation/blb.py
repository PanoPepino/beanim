from ..my_imports import *
from .text_general import *

__all__ = ["BlB"]


class BlB(Text_General, Group):
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
        from beanim import *

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

    def __init__(self, the_title=None, **kwargs) -> VGroup:
        super().__init__(**kwargs)
        self.the_title = the_title

        # Geometry
        self.order_list = BulletedList(
            *self.content,
            font_size=self.text_size,
            buff=self.tightness,
            stroke_color=self.text_color,
            dot_scale_factor=self.dot_scale,
        )

        self.order_list.set_color(self.text_color)
        self.count = 0

        if self.the_title is None:
            self.add_decorator(self.order_list)
        else:
            self.add_title_and_box(self.the_title, self.order_list)

    def add_title_and_box(self, title_on_top, points):
        """
        Add both title box and bullet points with appropriate decorative styling.

        Creates a title box with rounded top corners and a points box with rounded bottom corners,
        positioning them to create a unified visual element.

        :param title_on_top: The title text to display above the bullet points.
        :type title_on_top: str

        :param points: The BulletedList object containing the bullet points.
        :type points: BulletedList
        """
        up_title = Tex(title_on_top, font_size=1.3 * self.text_size, color=self.text_color).set_z_index(5)

        title_box = SurroundingRectangle(
            up_title,
            corner_radius=[self.crad, 0, 0, self.crad],
            buff=0.7 * self.tightness,
            stroke_width=self.decorator_stroke_width,
            color=self.decorator_color,
            fill_opacity=self.fill_opa + 0.1,
            stroke_opacity=self.stroke_opa
        )

        points_box = SurroundingRectangle(
            points,
            corner_radius=[0, self.crad, self.crad, self.crad],
            buff=self.tightness,
            stroke_width=self.decorator_stroke_width,
            color=self.decorator_color,
            fill_opacity=self.fill_opa,
            stroke_opacity=self.stroke_opa)

        self.box_up = VGroup(up_title, title_box)
        self.box_up.next_to(points_box.get_corner(UL), aligned_edge=LEFT, buff=0).shift(1.2*(self.tightness + 0.1)*UP)
        self.add(up_title, title_box, points_box, points)

    def next_point(self, rf: float = linear, rt: float = 1) -> Succession:
        """
        Animate to the next bullet point, highlighting it while dimming others.

        Each call to this method advances through the bullet points sequentially, creating
        a presentation-style reveal effect. The final call restores all points to full opacity.

        :param rf: Rate function for the animation transition.
        :type rf: float

        :param rt: Duration of the animation in seconds.
        :type rt: float

        :return: Animation sequence for the bullet point transition.
        :rtype: Succession

        .. note::

           After all bullet points have been shown, subsequent calls will return a Wait() animation.
        """
        if self.count == 0:
            self.count += 1
            return Succession(
                self.order_list[1:].animate(run_time=rt, rate_func=rf).set_opacity(0.2)
            )

        if 0 < self.count < len(self.order_list):
            self.count += 1
            return Succession(
                self.order_list.animate(run_time=rt, rate_func=rf).set_opacity(0.2),
                self.order_list[self.count - 1]
                .animate(run_time=rt, rate_func=rf)
                .set_opacity(1),
            )

        if self.count == len(self.order_list):
            self.count += 1
            return Succession(
                self.order_list.animate(run_time=rt, rate_func=rf).set_opacity(1)
            )
        else:
            return Wait()
