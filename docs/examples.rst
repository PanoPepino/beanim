Quick Guide
===========

This guide will walk you through creating a simple presentation with Beanim. By the end, you'll understand how to use templates, define slide objects, and create an animated presentation.

Available Templates
-------------------

Beanim comes equipped with six different templates to homogenise the look of your slides:

* 🎨 **default_template** - Clean and minimalist design
* 🧊 **blue_ice** - Cool blue color scheme
* 🍂 **red_autumn** - Warm autumn colors
* 🌿 **green_mint** - Fresh mint green theme
* 🟢 **beamer_green** - Classic Beamer style in green
* 🔵 **beamer_blue** - Classic Beamer style in blue

Template Gallery
^^^^^^^^^^^^^^^^

.. raw:: html

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
        <img src="_static/media/images/TST_dt.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
        <img src="_static/media/images/GST_dt.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
        
        <img src="_static/media/images/TST_ba.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
        <img src="_static/media/images/GST_ba.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
        
        <img src="_static/media/images/TST_fa.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
        <img src="_static/media/images/GST_fa.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
        
        <img src="_static/media/images/TST_fm.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
        <img src="_static/media/images/GST_fm.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
        
        <img src="_static/media/images/TST_bb.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
        <img src="_static/media/images/GST_bb.png" style="width:100%; border: 2px solid #000000ff; border-radius: 8px;"/>
    </div>


Step 1: Import and Setup
-------------------------

These templates can be called by importing them at the preamble of your ``file.py`` to compile with ``manim-slides``:

.. code-block:: python

    from manim import *
    from manim_slides import Slide
    from manim_beanim import * 
    
    # Choose your template
    import_template('default_template')

    class Your_Fancy_Presentation(Slide):
        def construct(self):
            # Your presentation code here
            pass


----

Step 2: Define Your Slide Objects
----------------------------------

Before building the presentation script, define all the objects (title slides, bullet points, equations, references) you'll use. This makes your code more organized and easier to maintain.

**Available Basic Object Types:**

* **Title_Presentation()** - Title slide with project name, affiliation, and author
* **Title_Section()** - Section header that appears at the top-left corner
* **BlB()** - Bulleted List Boxed with iterative animation support
* **Reference()** - Citations and references (manual or from .bib file)
* **Equation()** - LaTeX equations (manual or extracted from .tex file)

.. note::
   You can define all objects in a separate ``objects.py`` file and import them into your main script for better organization.

----

Step 3: Build Your Presentation
--------------------------------

Here's a complete example showing how to create a simple presentation:

.. code-block:: python

    from manim import *
    from manim_slides import Slide
    from manim_beanim import *

    import_template('default_template')

    class Quick_Presentation(Slide):
        def construct(self):

            # ============================================
            # SLIDE OBJECTS DEFINITION
            # ============================================
            
            # Title slide
            title_slide = Title_Presentation(
                content=[
                    "My Amazing Presentation",
                    "University Name",
                    "Your Name"
                ]
            )
            
            # Slide about the title slide structure
            slide_0_points = BlB(
                the_title="About Previous Slide",
                content=[
                    "Previous slide contained the Title of the Presentation",
                    "You call it with Title_Presentation() class",
                    "It has 3 entries: title, affiliation, author name"
                ]
            ).to_corner(LEFT)

            # Slide about sections and bullet lists
            slide_1_title = Title_Section(content="Using Title Sections")
            slide_1_points_1 = BlB(
                content=[
                    "What you see above is a Title_Section()",
                    "It is automatically placed in the upper-left corner"
                ]
            ).to_corner(LEFT)
            
            slide_1_points_2 = BlB(
                content=[
                    "This is a Bulleted List Boxed (BlB)",
                    "Use .next_point() to iterate over bullet points",
                    "Each point appears with an animation",
                    "Perfect for step-by-step explanations!"
                ]
            ).to_corner(LEFT)

            # Slide about references
            ref_1 = Reference(
                dictionary="path/to/refs.txt",
                content=['ref_key_1', 'ref_key_2']
            )
            ref_2 = Reference(content='[Manually Input Reference, 2025]')
            refs = VGroup(ref_1, ref_2).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
            
            slide_2_points_1 = BlB(
                content=[
                    "This demonstrates references/citations",
                    "Use the Reference() class",
                    "Option 1: Manually input references",
                    "Option 2: Extract from .bib file using dictionaries",
                    "See documentation/tools for extraction details"
                ]
            ).to_corner(LEFT).shift(UP)

            # Slide about equations
            eq_1 = Equation(
                content=["x^{2}+y^{2} = R^{2}, \quad", "e^{i \\pi} = -1"],
                text_size=30,
                direction=DOWN,
            ).shift(UP)
            
            eq_2 = Equation(
                dictionary="path/to/equations.txt",
                content="equation_key",
            ).shift(UP)
            
            slide_3_points_1 = BlB(
                content=[
                    "This demonstrates equation handling",
                    "Use the Equation() class",
                    "Option 1: Manually input LaTeX equations",
                    "Option 2: Extract from .tex file using dictionaries",
                    "See documentation/tools for extraction details"
                ]
            ).to_corner(DOWN)

            # ============================================
            # SLIDE ANIMATION SCRIPT
            # ============================================
            
            # Slide 0: Title
            self.play(FadeIn(title_slide))
            self.next_slide(notes='Introduction to title slide structure')
            
            # Slide 1: Explain title slide
            self.wipe(title_slide, slide_0_points)
            for _ in range(len(slide_0_points) + 1):
                self.next_slide()
                self.play(slide_0_points.next_point())
            
            # Slide 2: Section titles and bullet lists
            self.next_slide(notes='Demonstrate section titles and bullet lists')
            self.wipe(slide_0_points, slide_1_title)
            self.play(FadeIn(slide_1_points_1))
            self.next_slide()
            self.play(ReplacementTransform(slide_1_points_1, slide_1_points_2))
            for _ in range(len(slide_1_points_2) + 1):
                self.next_slide()
                self.play(slide_1_points_2.next_point())
            
            # Slide 3: References
            self.next_slide(notes='Show how to add references')
            self.wipe(Group(slide_1_title, slide_1_points_2), refs)
            self.play(Write(slide_2_points_1))
            
            # Slide 4: Equations
            self.next_slide(notes='Demonstrate equation handling')
            self.wipe(Group(slide_2_points_1, refs), Group(eq_1, slide_3_points_1))
            for _ in range(len(slide_3_points_1)):
                self.next_slide()
                self.play(slide_3_points_1.next_point())
            
            self.next_slide()
            self.play(ReplacementTransform(eq_1, eq_2))
            self.play(slide_3_points_1.next_point())
            
            # End
            self.next_slide(notes='End of presentation')
            self.play(FadeOut(slide_3_points_1, eq_2))

----

Step 4: Render Your Presentation
---------------------------------

Render the slides using the ``manim-slides`` command:

.. code-block:: bash

    manim-slides render example.py Quick_Presentation

After rendering, you can present your slides with:

.. code-block:: bash

    manim-slides present Quick_Presentation

----

Final Result
------------

Here's what the final presentation looks like:

.. raw:: html

    <div style="position:relative; padding-bottom:56.25%; margin: 20px 0;">
        <iframe
            loading="lazy"
            style="width:100%; height:100%; position:absolute; left:0px; top:0px; border: 2px solid #000000ff; border-radius: 8px;"
            frameborder="0"
            width="100%"
            height="100%"
            allowfullscreen
            allow="autoplay"
            src="https://panopepino.github.io/web_page/main_page/presentations/2025_09_docs/GP.html">
        </iframe>
    </div>

----

Next Steps
----------

Now that you've created your first presentation with Beanim, explore more advanced features:

* 🔧 Learn about extracting equations and references from files in the :doc:`api/modules` section
* 🎨 Experiment with different templates and customize your slides
* 💡 Visit the `Manim-Slides documentation <https://manim-slides.eertmans.be/latest/quickstart.html>`_ for additional animation techniques

.. tip::
   **Pro tip:** Start simple and gradually add complexity. Define all your objects first, then build the animation script step by step.
