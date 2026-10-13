"""Render with: manim render -ql example_multi_template.py Multi_Template"""
from pathlib import Path

from manim import Scene, VGroup, DOWN, RIGHT, LEFT, UP, DL, DR
from manim_beanim import BlB, Equation, Reference, Table, Title_Section, Underbar, apply_theme
from manim_beanim.themes.presets import THEMES


DICTIONARIES = Path(__file__).resolve().parent / "example_extract_ref_equation" / "dictionaries_extracted"


class Multi_Template(Scene):
    """Show the same generic slide with every bundled template."""

    def construct(self):
        for template_name in sorted(THEMES):
            self.clear()
            # Apply before creating objects. Existing objects keep their theme.
            apply_theme(template_name, scene=self)
            display_name = template_name.replace("_", r"\_")
            slide_title = Title_Section(content=rf"Template: \texttt{{{display_name}}}")

            refs = VGroup(
                Reference(
                    dictionary=DICTIONARIES / "refs.txt",
                    content=["ref_extract_1", "ref_extract_2"],
                ),
                Reference(content="[This is a fake ref, PP, XXYYZZ]"),
            ).arrange(DOWN, buff=0.05).next_to(
                slide_title, DOWN, buff=0.15,
            ).to_edge(RIGHT, buff=0.2)

            important_points = BlB(content=[
                "This is Bulleted list boxed (BlB)",
                r"Use .next\_point() to iterate over points",
                "The final step restores all points",
            ]).to_corner(LEFT).shift(UP)

            my_table = Table(
                content="table_data_base_2", dictionary="data_base",
            ).to_corner(DL, buff=0.4)
            eq_show = Equation(
                dictionary=DICTIONARIES / "equations.txt",
                content="equation_extract_2",
            ).to_corner(DR, buff=0.4)
            footer = Underbar(content=[
                "Pano Pepino", "Some University", "Some Title", "Feb 2050",
            ])

            self.add(slide_title, refs, important_points, my_table, eq_show, footer)
            self.wait(3)
