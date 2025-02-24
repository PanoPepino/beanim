from manim import *
from manim.utils.testing.frames_comparison import frames_comparison

__module_test__ = "geometry"


class GrowingCircleScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(GrowFromCenter(circle))


@frames_comparison
def test_growing_circle(scene):
    circle = Circle()
    scene.play(GrowFromCenter(circle))
