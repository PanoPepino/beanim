from beanim import *
from manim import *

# This method will import your desired template: [fancy_mint, blue_ice, fire_autumn, default_template]
import_template('fancy_mint')


class Title_Slide_Test(Scene):  #  A simple title slide
    def construct(self):
        tp = Title_Presentation(
            content=["This is a Title\\_Presentation", "Your institution", "Your name"])
        self.add(tp)


class Generic_Slide_Test(Scene):
    def construct(self):
        slide_title = Title_Section(content="This a Title\\_Section to Show")  # A simple title section
        ref1 = Reference(dictionary="example_extract_ref_equation/dictionaries_extracted/refs.txt",
                         # You can import references from a dictionary in a relative directory
                         content=['ref_extract_1', 'ref_extract_2'])
        ref2 = Reference(content='[This is a fake ref, PP, XXYYZZ]')  # Or create your manually input references
        refs = VGroup(ref1, ref2).arrange(DOWN, buff=0.05).to_corner(UR)

        important_points = BlB(  # This is a simple Bulleted List with a Box
            content=[
                "This is Bulleted list boxed (BlB)",
                "Use .next\\_point() to iterate over points",
                "... And for the last point you can recover all points in the initial color",
            ]).to_corner(LEFT).shift(UP)

        # You can even import tables, references or equations from a dictionary in a data_base include in the package.
        # If you want/need to add extra content, you can do it by yourself in the pip library.
        my_table = Table(content="table_data_base_1", dictionary="data_base").to_corner(DL)

        eq_show = Equation(
            dictionary="example_extract_ref_equation/dictionaries_extracted/equations.txt",
            content="equation_extract_2",
        ).to_corner(DR)

        self.add(refs, slide_title, important_points, my_table, eq_show)

        # The bulleted list comes equipped with a way to iterate over points.
        for _ in range(len(important_points) + 3):
            self.play(important_points.next_point())
