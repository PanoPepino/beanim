Installation
============

- Assumption! The reader is slightly familiar with git and pip terminology. Were the reader not familiar, we recommend them to see:
`Manim Installation <https://docs.manim.community/en/stable/installation.html>`_

What is required?
-----------------

* Python 3.12+
* `Manim Community Edition <https://docs.manim.community/en/stable/index.html>`_
* `Manim-Slides <https://manim-slides.eertmans.be/latest/>`_
* NumPy
* Any other package required by previous ones

How to install?
--------------

.. code-block:: bash

   cd path/to/desired/location
   git clone https://github.com/PanoPepino/beanim.git
   cd beanim
   pip install -e .

In order to check that the installation was fruitful, you can just type:

.. code-block:: bash

   pip show manim_beanim

.. note::

   While the name of the repository remains as **Beanim**, note that the package you are installing will be called **manim_beanim**. This will group all your manim packages and addons in appropiate alphabetic order when using pip show.