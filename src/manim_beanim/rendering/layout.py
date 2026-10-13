"""Bounded layout and replacement of component-owned render objects."""
from collections.abc import Sequence
from manim import Group, Mobject
from ..themes.styles import finite_number

def fit_within(mobject: Mobject, width: float, height: float) -> Mobject:
    """Shrink overflowing content; never enlarge it or distort aspect ratio."""
    width = finite_number(width, 'max_width', positive=True)
    height = finite_number(height, 'max_height', positive=True)
    if mobject.width > 0 and mobject.height > 0:
        scale = min(1, width / mobject.width, height / mobject.height)
        if scale < 1:
            mobject.scale(scale)
    return mobject

def replace_rendered(owner: Mobject, objects: Sequence[Mobject]) -> None:
    """Replace owned children while preserving external children and current position."""
    previous = getattr(owner, '_rendered_objects', ())
    objects = tuple(objects)
    if previous:
        Group(*objects).shift(Group(*previous).get_center() - Group(*objects).get_center())
    children = owner.submobjects.copy()
    try:
        owner.remove(*previous)
        owner.add(*objects)
    except Exception:
        owner.submobjects = children
        raise
    owner._rendered_objects = objects
