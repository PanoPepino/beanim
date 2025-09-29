Quick Guide
=========

This package comes equipped with different templates to homogenise the look of the slides.

* default_template
* blue_autumn
* fire_autumn
* fancy_mint

.. raw:: html

    <table style="width:100%; table-layout: fixed;">
      <tr>
        <td><img src="_static/media/images/TST_dt.png" style="width:100%;"/></td>
        <td><img src="_static/media/images/GST_dt.png" style="width:100%;"/></td>
      </tr>
      <tr>
        <td><img src="_static/media/images/TST_ba.png" style="width:100%;"/></td>
        <td><img src="_static/media/images/GST_ba.png" style="width:100%;"/></td>
      </tr><tr>
        <td><img src="_static/media/images/TST_fa.png" style="width:100%;"/></td>
        <td><img src="_static/media/images/GST_fa.png" style="width:100%;"/></td>
      </tr><tr>
        <td><img src="_static/media/images/TST_fm.png" style="width:100%;"/></td>
        <td><img src="_static/media/images/GST_fm.png" style="width:100%;"/></td>
      </tr>
    </table>


These templates can be called by importing them at the preamble of the file.py to compile with manim-slides as:

.. code-block:: python

    from manim import *
    from manim-slides import *

    import_template('fire_autumn')

    class Your_Fancy_Presentation(Slides):
        ....

Then, let us build our presentation. We will first define the characters of the presentation (the `objects <https://github.com/PanoPepino/beanim/issues>`_. we are going to use through the slides). After this, one can include the script of the slides with the commands provided in `Manim-Slides <https://manim-slides.eertmans.be/latest/quickstart.html>`_. Alternatively, you can define all the objects in a file.py and import all them into the script.py to run with Manim-Slides.


.. code-block:: python

    from manim import *
    from manim-slides import *

    import_template('fire_autumn')

    class Quick_Presentation(Slide):
    def construct(self):

        # Objects definition
        title_slide = Title_Presentation(content=[title_of_project, affiliation, author])
        slide_0_points = BlB(the_title="About previous slide",
                             content=[
                                 "Previous slide contained the Title of the Presentation",
                                 "You call it with Title\\_Presentation() class",
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
                "This is a reference/citation",
                "Its class is Reference()",
                "You can manually input your references...",
                "... Or you can extract references from a .bib file and call them from a dictionary",
                "Check documentation/tools for more information on this"
            ]).to_corner(LEFT).shift(UP)

        eq_1 = Equation(
            content=["x^{2}+y^{2} = R^{2}, \quad", "e^{i \pi} = -1"],
            text_size=30,
            direction=DOWN,
        ).shift(UP)
        eq_2 = Equation(
            dictionary="example_extract_ref_equation/dictionaries_extracted/equations.txt",
            content="equation_extract_2",
        ).shift(UP)
        slide_3_points_1 = BlB(
            content=[
                "This is a equation",
                "Its class is Equation()",
                "You can manually input your equations...",
                "... Or you can extract equations from a .tex file and call them from a dictionary",
                "Check documentation/tools for more information on this"
            ]).to_corner(DOWN)

        # Slide Manipulation
        self.play(FadeIn(title_slide))
        self.next_slide(notes='to slide about title')
        self.wipe(title_slide, slide_0_points)
        for _ in range(len(slide_0_points) + 3):
            self.next_slide()
            self.play(slide_0_points.next_point())
        self.next_slide(notes='to slide about section and bulleted list')
        self.wipe(slide_0_points, slide_1_title)
        self.play(FadeIn(slide_1_points_1))
        self.play(ReplacementTransform(slide_1_points_1, slide_1_points_2))
        for _ in range(len(slide_1_points_2) + 3):
            self.next_slide()
            self.play(slide_1_points_2.next_point())
        self.next_slide(notes='to slide about refs')
        self.wipe(Group(slide_1_title, slide_1_points_2), refs)
        self.play(Write(slide_2_points_1))
        self.next_slide(notes='to slide about equations')
        self.wipe(Group(slide_2_points_1, refs), Group(eq_1, slide_3_points_1))
        for _ in range(len(slide_3_points_1) + 1):
            self.next_slide()
            self.play(slide_3_points_1.next_point())
        self.next_slide()
        self.play(ReplacementTransform(eq_1, eq_2))
        self.play(slide_3_points_1.next_point())
        self.next_slide(notes='to end')
        self.play(FadeOut(slide_3_points_1, eq_2))

We then render the slides with:

.. code-block:: bash

    manim-slides render example.py Quick_Presentation

The final result of this quick guide is:

.. raw:: html

    <div style="position:relative;padding-bottom:56.25%;">
        <iframe
            loading="lazy"
            style="width:100%;height:100%;position:absolute;left:0px;top:0px;"
            frameborder="0"
            width="100%"
            height="100%"
            allowfullscreen
            allow="autoplay"
            src="https://panopepino.github.io/web_page/main_page/presentations/2025_09_docs/GP.html">
        </iframe>
    </div>

