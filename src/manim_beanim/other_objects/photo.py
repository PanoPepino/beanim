from ..my_imports import *
__all__ = ['Photo']


def clip_image_to_mobject(image, mobj):
    """
    Crop an ImageMobject into the shape of another mobject.

    This utility captures a snapshot of `image`, then masks it with `mobj` to produce
    a clipped image in the shape of the given mobject.

    :param image: The ImageMobject to crop.
    :type image: ImageMobject

    :param mobj: The shape mobject used as a cropping mask.
    :type mobj: Mobject

    :return: A new ImageMobject cropped to the shape of `mobj`.
    :rtype: ImageMobject
    """
    scene = Scene()
    render = scene.renderer

    aux = Image.fromarray(render.camera.pixel_array)
    bg = Image.new("RGBA", aux.size, (0, 0, 0, 0))

    render.camera.set_pixel_array(np.zeros_like(render.camera.pixel_array))
    render.camera.capture_mobjects([image])
    img = Image.fromarray(render.camera.pixel_array.copy())

    render.camera.set_pixel_array(np.zeros_like(render.camera.pixel_array))
    render.camera.capture_mobjects([mobj])
    mask = Image.fromarray(render.camera.pixel_array.copy())

    result = Image.composite(img, bg, mask)
    cropped = result.crop(result.getbbox())
    return ImageMobject(cropped)


class Photo(Group):
    """
    Represent and decorate a photograph with optional polaroid or frame styling.

    :param photo: Path to the image file.
    :type photo: str

    :param decorator_style:
        Style of decoration. Options:
          - ``"polaroid"``: Photo with a pin and caption.
          - ``"techno"``: Photo with a simple colored frame.
    :type decorator_style: str, optional

    :param caption: Text caption under the polaroid photo (only for ``polaroid`` style).
    :type caption: str, optional

    :param text_size: Font size for caption text. Default is ``35``.
    :type text_size: float

    :param text_color: Color of caption text. Default is ``WHITE``.
    :type text_color: ParsableManimColor

    :param decorator_color: Color for the frame or pin. Default is ``WHITE``.
    :type decorator_color: ParsableManimColor

    :param pin_color: Color for the pin on the polaroid. Default is ``WHITE``.
    :type pin_color: ParsableManimColor

    :param corner_rad: Corner radius for frames. Default is ``0``.
    :type corner_rad: float

    :param decorator_stroke_w: Stroke width for frames. Default is ``1``.
    :type decorator_stroke_w: float

    :param kwargs: Additional arguments passed to :class:`Group`.

    .. note::

       Captions apply only when ``decorator_style == "polaroid"``.

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_beanim import Photo

        class Example_Photo(Scene):
            def construct(self):
                photo1 = Photo("figures/pic.png", decorator_style="polaroid", caption="My Photo")
                photo2 = Photo("figures/pic.png", decorator_style="techno")
                self.add(photo1, photo2)
    """

    def __init__(
        self,
        photo,
        decorator_style: str = "techno",
        caption: str = "",
        text_size: float = 35,
        text_color: ParsableManimColor = WHITE,
        decorator_color: ParsableManimColor = WHITE,
        pin_color: ParsableManimColor = WHITE,
        corner_rad: float = 0,
        decorator_stroke_w: float = 1,
        **kwargs
    ):
        super().__init__(**kwargs)

        # This gets the svg path in the package, wherever the package is and then add the desired svg. Observe that path.dirname gets the path where this file is located. I then go back to the parent directory, where the figure folder is.

        get_svg_path = path.join(path.dirname(__file__), '../figures/pin.svg')

        # Polaroid
        if decorator_style == "polaroid":
            r1 = RoundedRectangle(width=2, height=2.9, corner_radius=corner_rad/2)
            r2 = RoundedRectangle(width=1.8, height=2.1, corner_radius=corner_rad /
                                  2).move_to(r1.get_center()).shift(0.3*UP)
            polaroid = Cutout(r1, r2, fill_opacity=1, color=WHITE,
                              stroke_color=decorator_color, stroke_width=3*decorator_stroke_w)
            image = ImageMobject(photo).set(z_index=-1)
            frame = SurroundingRectangle(r2, color=decorator_color, stroke_width=decorator_stroke_w, buff=0.0)
            mask = frame.copy().set_fill(BLACK, 1).set_stroke(width=5)
            clip = clip_image_to_mobject(image, mask)
            clip.move_to(mask).scale_to_fit_width(mask.width).set_z_index(-10)
            pin = SVGMobject(get_svg_path).scale(0.2).next_to(polaroid, UP, buff=-0.05).shift(0.2*RIGHT)
            pin.set_color(pin_color)

        # Text under polaroid
            texto = Tex(caption, font_size=text_size, color=text_color).next_to(clip, DOWN, buff=0.2).set(z_index=4)

            self.chosen_photo = Group(polaroid, clip, texto, pin)
            self.add(self.chosen_photo)

        # Technophoto
        if decorator_style == "techno":
            image = ImageMobject(photo).scale_to_fit_height(config['frame_height'])
            frame = SurroundingRectangle(image, corner_radius=corner_rad, color=decorator_color,
                                         stroke_width=3*decorator_stroke_w, buff=-0.2)
            mask = frame.copy().set_fill(WHITE, 1).set_stroke(width=0)
            clip = clip_image_to_mobject(image, mask)
            clip.move_to(mask).scale_to_fit_width(mask.width)
            self.chosen_photo = Group(clip, frame)
            self.add(self.chosen_photo)
