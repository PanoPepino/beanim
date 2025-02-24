from manim import *

from beanim import *

import_template("fancy_mint")


class Example_AdS_Jc(Scene):
    def construct(self):
        show_db = AdS_Jc(vacua_type="DB")
        show_rs = AdS_Jc(vacua_type="RS")
        show = (
            VGroup(show_db, show_rs)
            .arrange(RIGHT, aligned_edge=DOWN, buff=0.2)
            .scale_to_fit_width(config.frame_width - 2)
        )

        self.play(AnimationGroup(map(lambda x: x.fade_in(), show)))
        self.play(AnimationGroup(map(lambda x: x.fade_in_arrow(), show)))
        self.play(show[1].show_symmetry(rt=5))
        self.play(show[1].restore_symmetry())
        self.play(
            AnimationGroup(
                show[0].show_n_vector_db(rt=5), show[1].show_n_vector_rs(rt=5)
            )
        )
        self.play(show.animate.shift(2 * UP))
        self.play(FadeOut(show))


class Example_Photo_Post_it(Scene):
    def construct(self):
        photo_1 = Photo(
            "figures/pedro.png", decorator_style="polaroid", caption="Perro Xanxe"
        )
        photo_2 = Photo(
            "figures/pedro.png", decorator_style="techno", caption="Perro Xanxe"
        )
        p_it = Post_It(to_dos=["Random example", "Just Do It!"]).scale(0.9)
        self.add(
            Group(photo_1, photo_2, p_it)
            .arrange(RIGHT, buff=0.2)
            .scale_to_fit_width(config.frame_width - 1)
        )


class Example_Black_Hole(Scene):
    def construct(self):
        bh_sp = Black_Hole(bh_type="spinning")
        bh_frag = Black_Hole(bh_type="fragmentation")
        bh = Black_Hole()
        bh_group = (
            VGroup(bh_sp, bh_frag, bh)
            .arrange(RIGHT, buff=3)
            .scale_to_fit_width(config.frame_width - 1)
        )
        self.add(bh_group)
        self.play(AnimationGroup(map(lambda x: x.nucleate(), bh_group)))
        self.play(AnimationGroup(map(lambda x: x.expand(), bh_group)))


class Example_Bubble(Scene):
    def construct(self):
        bubble_types = ["empty", "radiation", "em", "strings", "GW"]
        bubble_group = Group(
            *[Bubble(bubble_type=my_type).scale(0.4) for my_type in bubble_types]
        ).arrange_in_grid(2, 3)

        # self.add(bubble_group)
        self.play(AnimationGroup(map(lambda x: x.fade_in_bulk(), bubble_group)))
        self.play(AnimationGroup(map(lambda x: x.create_bubble(), bubble_group)))
        self.play(AnimationGroup(map(lambda x: x.expand_bubble(), bubble_group)))


class Example_Energy_Discussion(Scene):
    def construct(self):
        bub = Bubble(bubble_type="energy_discussion").scale(0.8)
        self.play(bub.fade_in_bulk())
        self.play(bub.fail_creation())
        self.play(bub.create_bubble())
        self.play(bub.expand_bubble())
        self.play(FadeOut(bub))
