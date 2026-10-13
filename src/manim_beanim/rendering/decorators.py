"""Construct decorations without attaching children or mutating owner state."""
from manim import Mobject, SurroundingRectangle, RoundedRectangle, LEFT, RIGHT, config

def decorate(owner, mobject: Mobject) -> tuple[Mobject, ...]:
    mobject.set_z_index(5)
    mode = owner.decorator_presence
    settings = dict(stroke_width=owner.decorator_stroke_width, color=owner.decorator_color,
                    fill_opacity=owner.fill_opa, stroke_opacity=owner.stroke_opa,
                    corner_radius=owner.corner_rad)
    if mode == 'no':
        return (mobject,)
    if mode == 'box':
        box = SurroundingRectangle(mobject, buff=owner.tightness, **settings)
    elif mode in {'box_long_right', 'box_long_left'}:
        box = RoundedRectangle(height=mobject.height + owner.tightness,
                               width=mobject.width + 10, **settings)
        if mode == 'box_long_right':
            box.next_to(mobject.get_left(), RIGHT, aligned_edge=LEFT, buff=-0.5 * owner.tightness)
        else:
            box.flip().next_to(mobject.get_right(), LEFT, aligned_edge=RIGHT, buff=-owner.tightness)
    elif mode == 'back_frame':
        box = RoundedRectangle(height=mobject.height + 1.5 * owner.tightness,
                               width=config.frame_width + 0.1, **settings)
        box.move_to([0, mobject.get_y(), 0])
    else:
        raise ValueError(f'Unsupported decorator_presence: {mode!r}')
    return (mobject, box)
