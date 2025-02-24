from manim import *

from beanim import *


class Example_Table_Summary_Bubble_and_Scales(Scene):
    def construct(self):
        gp = (
            VGroup(Table_Summary_Induce(), Table_Energy_Scales())
            .arrange(RIGHT)
            .scale_to_fit_width(config.frame_width - 1)
        )
        self.add(gp)


class Example_Table_Bh_Embedding(Scene):
    def construct(self):
        together = (
            Table_Bh_Embedding(type="together")
            .scale_to_fit_width(config.frame_width - 1)
            .shift(UP)
        )
        split = (
            Table_Bh_Embedding(type="split", chosen_position=RIGHT)
            .scale_to_fit_width(config.frame_width - 1)
            .next_to(together, DOWN, buff=0.2)
        )
        self.add(together, split)
        self.play(
            AnimationGroup(
                together.move_all(), split.move_non_compact(), split.move_compact()
            )
        )


class Example_Plot_Instanton(Scene):
    def construct(self):
        p_ins = Plot_Instanton().to_corner(DL)
        self.add(p_ins[0])
        self.play(p_ins.fade_in_field_position())
        self.play(p_ins.decay())


class Example_Plot_Q(Scene):
    def construct(self):
        gq = Plot_Quantum().scale(0.4).to_corner(DL)
        self.add(gq[0])
        self.play(gq.create_wave_functions())
        self.play(gq.animate.shift(UP))


class Example_Plot_Induced_Potential(Scene):
    def construct(self):
        plot_pot = Plot_Induced_Potential()
        plot_pot.scale(0.3, about_point=plot_pot.ax_4D_cosmos.get_origin()).to_corner(
            LEFT
        )
        self.add(plot_pot[0])
        self.play(plot_pot.show_potential())
        self.play(plot_pot.show_jc())
        self.play(plot_pot.nucleate_brane())
        self.wait()
        self.play(plot_pot.accelerate())
        self.play(plot_pot.bounce())
        self.play(plot_pot.add_cc_and_expand())
        self.play(FadeOut(plot_pot))
        self.play(Wait())


class Example_Plot_Tension(Scene):
    def construct(self):
        p_tension = Plot_Lambda_Tension()
        p_tension.scale(
            0.3, about_point=p_tension.ax_tension_DB.get_origin()
        ).to_corner(LEFT)
        self.play(FadeIn(p_tension[0]))
        self.play(p_tension.create_function())
