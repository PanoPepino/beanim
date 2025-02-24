## ABOUT BEANIM
- This repository contains v1.0 of beanim (Beamer + Manim) libraries. It is an improved version of the old mtheoretical, with more straightforward commands and a better folder and files organisation, with more optional parameters and the cleanest documentation I am able to achieve.

- These libraries are supposed to be used with [manim-slides](https://manim-slides.eertmans.be/latest/) and [manim](https://www.manim.community).

- The main idea of this package is to offer a beamer-like experience, with more freedom, less annoying commands and possibility to loop animations.

- These files contain a set of tools:
    - To extract equations and references from .tex and .bib files.
    - To organise your slides with Titles, bulleted lists, general equations, etc in a similar fashion than beamer one.
    - My personal animations to generate slides to present my scientific research.

You can find examples of the overall results [here](https://panopepino.github.io/web_page/main_page/slides.html).

- The [documentation webpage](https://panopepino.github.io/beanim/) includes information about the characteristics and examples of each of the classes and their methods included in these libraries. The main reason of its existence is to easily access all objects of these libraries when crafting slides.

-----------------------------------------------------------------------

## Installation

In order to **install** this library, do the following:

```bash
git clone https://github.com/PanoPepino/beanim

pip install .

```

## Usage

To **use** it in your manim files, call it with:

```python
from beanim import *
```

-----------------------------------------------------------------------

## TO DO

- Include old animations:
    - Diagrams (gravity and EM)
    - Pulling strings and bending branes.

- Code new animations:
    - (Non)-Normalisable modes and the bubble expanding.
    - Smooth transition between global and Poincaré coordinates for the bubble.
    - Method in title_section to display title at center, shrink and place UR.

- General Python code to write:
    - Rewrite code to extract all the equations of a .tex file in the form of a dictionary {eq_label: 'equation'}, but taking into account
    things like \begin{split}, \begin{aligned} and so on. At the moment it only works with regular \begin{equation} enviroment.
    - Think how to choose among equations in the package and equations from outside.
    - Two more templates
    - Allow choosing upper title for bulleted lists.

- Changes to make for webpage deploy:

    - Add required configuration in the conf.py file to automatically remove Submodule headings, Module contents at the end of the page, and any name displayed as pkg.sub_pkg.module.
    - Fix issue with sphinxcontrib.video, so that videos can be deploy in sphinx.
        - Add videos for each big class, specifying the commands.
    - Think how to add miniature slides as Manimslides webpage.

- Changes to make the Github deploy more professional:

    - Add tests for each of the modules in the package
    - Make the precommit work, as it currently does not detect manim nor beanim and everything is a whole error.
    
