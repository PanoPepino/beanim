from manim import *

from beanim import *

# import_template('fancy_mint')
# import_template("dark_depths")


class Title_Slide(Scene):
    def construct(self):
        self.add(
            Title_Presentation(
                "This is a Title\_Presentation",
                "Your institution",
                author="Your name",
            )
        )


class Generic_Slide(Scene):
    def construct(self):
        slide_title = Title_Section("This a Title\_Section")
        ref1 = Ref(
            the_dictionary="example_refeq/dictionaries/test_ref.txt", the_ref="RS1"
        ).to_corner(UR)
        important_points = BlB(
            [
                "This is Bulleted list boxed (BlB)",
                "Use .next\\_point() to iterate over points",
                "... And for the last point you can recover all points in the initial color",
            ]
        ).to_corner(LEFT)
        eq_show = Eq_General(
            the_dictionary="example_refeq/dictionaries/eq_test_file.txt",
            the_equation="my_other_eq_2",
        ).to_corner(DOWN)
        self.play(slide_title.show_title())
        self.play(FadeIn(ref1, important_points))
        for point in range(len(important_points) + 3):
            self.play(important_points.next_point())
        self.play(FadeIn(eq_show))


class Example_Equation(Scene):
    def construct(self):
        eq_show = Eq_General(
            the_dictionary="example_refeq/dictionaries/eq_test_file.txt",
            the_equation="my_other_eq_2",
        )
        self.add(eq_show)
