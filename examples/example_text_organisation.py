from manim import *
from manim_beanim import *

import_template_beanim('blue_ice')


class Title_Slide_Test(Scene):
    def construct(self):
        tp = Title_Presentation(
            content=["This is a Title\\_Presentation", "Your institution", "Your name"])
        self.add(tp)


class Title_Section_Test(Scene):
    def construct(self):
        title_section = Title_Section(content='This is a title section test')
        self.add(title_section)


class BlB_Test(Scene):
    def construct(self):
        important_points = BlB(
            content=[
                "This is Bulleted list boxed (BlB) with a title",
                "Use .next\\_point() to iterate over points",
                "... And for the last point you can recover all points in the initial color",
            ], the_title="This is a title for the bulleted list").to_corner(LEFT).shift(UP)
        important_points_2 = BlB(
            content=[
                "This is Bulleted list boxed without a title",
                "Use .next\\_point() to iterate over points",
                "Observe that the corners are different",
            ]).next_to(important_points, DOWN, aligned_edge=LEFT)

        self.add(important_points, important_points_2)
        for _ in range(len(important_points) + 3):
            self.play(important_points.next_point())


class Ref_Test(Scene):
    def construct(self):
        ref_from_data_base = Reference(
            content=['ref_data_base_1',
                     'ref_data_base_2',
                     'ref_data_base_3'],
            dictionary='data_base')
        ref_from_extract = Reference(dictionary="example_extract_ref_equation/dictionaries_extracted/refs.txt",
                                     content=['ref_extract_1', 'ref_extract_2'])
        ref_from_extract_2 = Reference(
            dictionary="example_extract_ref_equation/dictionaries_extracted/refs.txt", content='ref_extract_3')
        ref_from_manual_input = Reference(content='[Manually input ref, PP, 2025]')
        references = VGroup(ref_from_data_base, ref_from_extract, ref_from_extract_2,
                            ref_from_manual_input).arrange(DOWN, aligned_edge=LEFT)
        self.add(references)


class Equation_Test(Scene):
    def construct(self):
        eq_from_data_base = Equation(
            content=["equation_data_base_1",
                     "equation_data_base_3"],
            dictionary="data_base",
            text_size=30,
            direction=DOWN,
            aligned_direction=LEFT
        )
        eq_from_extract = Equation(
            content=["equation_extract_1",
                     "equation_extract_3"],
            dictionary="example_extract_ref_equation/dictionaries_extracted/equations.txt",
            text_size=30,
            direction=DOWN,
            aligned_direction=LEFT
        )
        eq_from_manual_input = Equation(
            content=["x^{2}+y^{2} = R^{2}, \\quad", "e^{i \\pi} = -1"],
            text_size=30,
            direction=RIGHT
        )
        self.add(VGroup(eq_from_data_base, eq_from_extract, eq_from_manual_input).arrange(DOWN))


class Generic_Slide_Test(Scene):
    def construct(self):
        slide_title = Title_Section(content="This a Title\\_Section to Show")
        ref1 = Reference(dictionary="example_extract_ref_equation/dictionaries_extracted/refs.txt",
                         content=['ref_extract_1',
                                  'ref_extract_2'])
        ref2 = Reference(content='[This is a fake ref, PP, XXYYZZ]')
        refs = VGroup(ref1, ref2).arrange(DOWN, buff=0.05).to_corner(UR, buff=0.2)

        important_points = BlB(
            content=[
                "This is Bulleted list boxed (BlB)",
                "Use .next\\_point() to iterate over points",
                "... And for the last point you can recover all points in the initial color",
            ]).to_corner(LEFT).shift(UP)

        my_table = Table(content="table_data_base_2",
                         dictionary="data_base").to_corner(DL, buff=0.4)
        tt = Underbar(content=["Pano Pepino",
                               "Some University",
                               "Some Title",
                               "Feb 2050"])

        eq_show = Equation(
            dictionary="example_extract_ref_equation/dictionaries_extracted/equations.txt",
            content="equation_extract_2",
        ).to_corner(DR, buff=0.4)

        self.add(refs, slide_title, important_points, my_table, eq_show, tt)

#        for point in range(len(important_points) + 3):
#           self.play(important_points.next_point())
#         self.play(FadeIn(eq_show))


class Underbar_Test(Scene):
    def construct(self):
        under = Underbar(content=["Pano Pepino", "Some University", "My talk in the Mooon",
                                  "30th February 2050"])
        self.add(under)
