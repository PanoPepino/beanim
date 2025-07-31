from manim import *
from beanim import *

import_template('fancy_mint')


class Example_Table(Scene):
    def construct(self):
        table = Table(
            content=[["1", "2"], ["3", "4"]])
        table_2 = Table(content="table_data_base_2", dictionary="data_base")
        self.add(VGroup(table, table_2).arrange(DOWN))


class Example_Photo_Post_it(Scene):
    def construct(self):
        photo_1 = Photo("figures/pedro.png", decorator_style="polaroid", caption="Perro Xanxe")
        photo_2 = Photo("figures/pedro.png", decorator_style="techno").scale_to_fit_height(photo_1.get_height())
        p_it = Post_It(to_dos=["Random example", "Just Do It!"]).scale_to_fit_height(photo_1.get_height())
        my_group = Group(photo_1, photo_2, p_it).arrange(RIGHT).scale_to_fit_width(config.frame_width - 1)

        self.add(my_group)
        self.play(my_group.animate.arrange(LEFT))
