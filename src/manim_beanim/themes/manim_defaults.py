"""Manim default-constructor compatibility boundary.

Manim exposes set_default but cannot retrieve previously configured defaults.
Keep descriptor access here so application code does not depend on that detail.
"""
from manim import Tex, MathTex, Text

CLASSES = (Tex, MathTex, Text)

def snapshot() -> dict:
    return {cls: cls.__dict__.get('__init__') for cls in CLASSES}

def restore(constructors: dict) -> None:
    for cls, constructor in constructors.items():
        if constructor is None:
            if '__init__' in cls.__dict__:
                delattr(cls, '__init__')
        else:
            cls.__init__ = constructor
