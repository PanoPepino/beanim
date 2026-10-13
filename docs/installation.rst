Installation
============

Beanim requires Python 3.11 or newer and Manim's system dependencies,
including Cairo, Pango, FFmpeg, LaTeX, and dvisvgm.

Ubuntu theme fonts require Greek font definitions even for English text:

.. code-block:: bash

   sudo apt-get install texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra texlive-lang-greek dvisvgm

Manim 0.18.1 uses ``numpy.trapz``, removed in NumPy 2.4. When retaining
that Manim version, install with a compatible NumPy range:

.. code-block:: bash

   python -m pip install "manim==0.18.1" "numpy>=2.0.2,<2.4" -e .

Current Manim 0.21 CI jobs also test newer NumPy releases.
Verify all theme fonts and geometry operations with
``python scripts/check_render_environment.py``. Failed compilations retain
diagnostic files in the reported temporary directory.

Install from checkout:

.. code-block:: bash

   python -m pip install -e .

For existing presentation examples using Manim-Slides:

.. code-block:: bash

   python -m pip install -e ".[examples]"

Select a presentation-wide theme before constructing objects:

.. code-block:: python

   from manim_beanim import apply_theme

   apply_theme("blue_ice")

Inside an existing Scene, use ``apply_theme("blue_ice", scene=self)``.
This updates its background. Existing objects keep their appearance.
Explicit constructor styling overrides theme defaults.

Legacy imports and ``import_template_beanim()`` remain supported.

Documentation
-------------

.. code-block:: bash

   python -m pip install -e ".[docs]"
   python -m sphinx -W --keep-going -b html docs docs/_build/html
   python -m http.server 8000 --directory docs/_build/html

Open ``http://localhost:8000/``.
