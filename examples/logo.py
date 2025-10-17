from manim import *
from manim_beanim import *
from manim_mobject_svg import *

import_template("beamer_blue")


class My_Logo_3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = None
        o_slide = RoundedRectangle(color=GREY, height=3, width=6,
                                   fill_opacity=0.15, stroke_opacity=0.3, stroke_width=0, corner_radius=[0.1, 0, 0, 0.1])
        o_underbar = Underbar(content=["Pano Pepino", "Beanim", "2025"], text_color=WHITE, text_size=70
                              ).scale_to_fit_width(o_slide.get_width())
        titlebar_counter = ["First Slide", "Second Slide", "Third Slide", "Last Slide"]
        o_titlebar = VGroup(*[Title_Section(content=titlebar_counter[i], text_color=WHITE, text_size=30)
                              for i in range(len(titlebar_counter))]).scale_to_fit_width(o_slide.get_width())
        o_titlebar.move_to(o_slide.get_corner(UP), aligned_edge=UP).set_opacity(0.6)

        o_underbar.move_to(o_slide.get_corner(DOWN), aligned_edge=DOWN).set_opacity(0.6)
        o_banner = VGroup(ManimBanner()[0][0], ManimBanner()[0][1], ManimBanner()[0][2], ManimBanner()[1][0].set_color(WHITE)).scale_to_fit_width(
            o_slide.get_width()/3)
        o_banner.arrange(RIGHT, buff=-0.2).move_to(o_slide.get_center()).set_opacity(0.6)

        slides = VGroup(*[VGroup(o_slide.copy().set_z_index(i), o_underbar.copy(), o_banner[i].shift(i*0.2*DOWN), o_titlebar[i]
                                 ).move_to([0.2*i, -0.5*i, 0.9*i]) for i in range(4)])
        # 0.2*i, -0.5*i, 0.9*i
        slides.rotate(PI/4, axis=[0, 1, 0]).move_to([0, 0, 0])

        self.add(slides)
        slides.to_svg("slides.svg")


class My_Logo_2D(Scene):
    def construct(self):
        self.camera.background_color = None
        o_slide = RoundedRectangle(color=WHITE, height=4, width=6,
                                   fill_opacity=0.15, stroke_opacity=0.3, stroke_width=0, corner_radius=[0.1, 0, 0, 0.1])
        o_underbar = Underbar(content=["Pano Pepino", "Beanim", "2025"], text_color=WHITE, text_size=70
                              ).scale_to_fit_width(o_slide.get_width())
        o_titlebar = Title_Section(content="Beanim = Beamer + Manim", text_color=WHITE,
                                   text_size=30).scale_to_fit_width(o_slide.get_width())
        o_titlebar.move_to(o_slide.get_corner(UP), aligned_edge=UP).set_opacity(0.6)

        o_underbar.move_to(o_slide.get_corner(DOWN), aligned_edge=DOWN).set_opacity(0.6)
        o_banner = ManimBanner().scale_to_fit_width(o_slide.get_width()/2).move_to(o_slide.get_center()).set_opacity(0.6)

        slide = VGroup(o_slide, o_underbar, o_titlebar, o_banner)

        self.add(slide)
        slide.to_svg("slide.svg")
