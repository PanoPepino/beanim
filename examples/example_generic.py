from beanim import *
from manim import *
from manim_slides import Slide

# This method will import your desired template: [fancy_mint, blue_ice, fire_autumn, default_template]
import_template('default_template')

title_of_project = "A quick guide to Beanim"
affiliation = "University of mars"
author = "PanoPepino"


class Generic_Presentation(Slide):
    def construct(self):

        # Objects definition
        title_slide = Title_Presentation(content=[title_of_project, affiliation, author])
        slide_0_points = BlB(the_title="About previous slide",
                             content=[
                                 "Previous slide contained the Title of the Presentation",
                                 "You call it wit Title\\_Presentation() class",
                                 "It has 3 entries: title of slides, your affiliation, your name"
                             ]).to_corner(LEFT)

        slide_1_title = Title_Section(content="This a Title\\_Section to Show")
        slide_1_points_1 = BlB(
            content=[
                "What you see upstairs is a Title\\_Section()",
                "It is defined so that it will always be placed to the UL corner"
            ]).to_corner(LEFT)
        slide_1_points_2 = BlB(
            content=[
                "This is Bulleted list boxed",
                "Its class is BlB()",
                "Use its inbuilt function .next\\_point() to iterate over points",
                "... And for the last point you can recover all points in the initial color",
            ]).to_corner(LEFT)

        ref_1 = Reference(dictionary="example_extract_ref_equation/dictionaries_extracted/refs.txt",
                          content=['ref_extract_1', 'ref_extract_2'])
        ref_2 = Reference(content='[Manually input ref, 2025]')
        refs = VGroup(ref_1, ref_2).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
        slide_2_points_1 = BlB(
            content=[
                "This is a reference/citation (Look up-right)",
                "Its class is Reference()",
                "You can manually input your references...",
                "... Or you can extract references from a .bib file and call them from a dictionary",
                "Check documentation/tools for more information on this"
            ]).to_corner(LEFT)

        eq_1 = Equation(
            content=["x^{2}+y^{2} = R^{2}, \quad", "e^{i \pi} = -1"],
            text_size=30,
            direction=DOWN,
        ).shift(1.5*UP)
        eq_2 = Equation(
            dictionary="example_extract_ref_equation/dictionaries_extracted/equations.txt",
            content="equation_extract_2",
        ).shift(1.5*UP)
        slide_3_points_1 = BlB(
            content=[
                "This is an equation",
                "Its class is Equation()",
                "You can manually input your equations...",
                "... Or you can extract equations from a .tex file and call them from a dictionary",
                "Check documentation/tools for more information on this"
            ]).to_corner(DOWN)

        # Slide Manipulation
        self.play(FadeIn(title_slide))
        self.next_slide(notes='to slide about title')
        self.wipe(title_slide, slide_0_points)
        for _ in range(len(slide_0_points.content) + 1):
            self.next_slide()
            self.play(slide_0_points.next_point())
        self.next_slide(notes='to slide about section and bulleted list')
        self.wipe(slide_0_points, slide_1_title)
        self.play(FadeIn(slide_1_points_1))
        self.next_slide(notes='to slide about section and bulleted list')
        self.play(ReplacementTransform(slide_1_points_1, slide_1_points_2))
        for _ in range(len(slide_1_points_2.content) + 3):
            self.next_slide()
            self.play(slide_1_points_2.next_point())
        self.next_slide(notes='to slide about refs')
        self.wipe(Group(slide_1_title, slide_1_points_2), refs)
        self.play(Write(slide_2_points_1))
        self.next_slide(notes='to slide about equations')
        self.wipe(Group(slide_2_points_1, refs), Group(eq_1, slide_3_points_1))
        for _ in range(len(slide_3_points_1.content)-1):
            self.next_slide()
            self.play(slide_3_points_1.next_point())
        self.next_slide()
        self.play(ReplacementTransform(eq_1, eq_2))
        self.play(slide_3_points_1.next_point())
        self.next_slide(notes='to end')
        self.play(slide_3_points_1.next_point())
        self.play(FadeOut(slide_3_points_1, eq_2))


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
        # my_table = Table(table="table_data_base_1", dictionary="data_base").to_corner(DL)

        eq_show = Equation(
            dictionary="example_extract_ref_equation/dictionaries_extracted/equations.txt",
            content="equation_extract_2",
        ).to_corner(DR)

        self.add(refs, slide_title, important_points, eq_show)

        # The bulleted list comes equipped with a way to iterate over points.
        for _ in range(len(important_points) + 3):
            self.play(important_points.next_point())
