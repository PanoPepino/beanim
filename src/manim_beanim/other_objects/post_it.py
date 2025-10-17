from ..my_imports import *
__all__ = ["Post_It"]


class Post_It(Group):
    """
    Create a Post-it sticker graphic with a bullet list and pin decoration.

    :param to_dos: List of bullet points to display on the Post-it.
    :type to_dos: list[str]

    :param text_color: Color of the to-do text. Default is ``BLACK``.
    :type text_color: ParsableManimColor

    :param text_size: Font size for the to-do text. Default is ``35``.
    :type text_size: float

    :param pin_color: Color of the pin graphic. Default is ``WHITE``.
    :type pin_color: ParsableManimColor

    :param kwargs: Additional arguments passed to :class:`Group`.

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_beanim import Post_It

        class PostItScene(Scene):
            def construct(self):
                p_it = Post_It(to_dos=["Task 1", "Task 2"], text_color=BLACK, pin_color=RED)
                self.add(p_it)
    """

    def __init__(
        self,
        to_dos: list,
        text_color: ParsableManimColor = BLACK,
        text_size: float = 35,
        pin_color: ParsableManimColor = WHITE,
        **kwargs
    ):
        super().__init__(**kwargs)

        # postit
        get_post_it_path = path.join(path.dirname(__file__), "../figures/post_it.svg")
        post = SVGMobject(get_post_it_path).set(z_index=-1).scale(2)

        get_pin_path = path.join(
            path.dirname(__file__), "../figures/pin.svg"
        )
        # This gets the svg path in the package, wherever the package is (I hope it still works when transformed into a pip package) and then add the desired svg. Observe that path.dirname gets the path where this file is located. I then go back to the parent directory, where the figure folder is.

        pin = (
            SVGMobject(get_pin_path)
            .scale(0.2)
            .next_to(post, UP, buff=-0.1)
            .shift(0.2 * RIGHT)
            .set(color=pin_color)
        )

        # text
        td = BulletedList(
            *to_dos, color=text_color, font_size=text_size, buff=0.3, dot_scale_factor=2)
        td.set(color=text_color)
        td.next_to(post.get_left(), RIGHT, aligned_edge=LEFT, buff=0.2).shift(0.5 * UP)

        self.post_it = Group(post, td, pin)
        self.add(self.post_it)
