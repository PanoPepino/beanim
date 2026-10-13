API reference
=============

Themes
------

.. autofunction:: manim_beanim.apply_theme
.. autofunction:: manim_beanim.get_theme
.. autoclass:: manim_beanim.Theme

Components
----------

.. autoclass:: manim_beanim.Title_Presentation
.. autoclass:: manim_beanim.Title_Section
.. autoclass:: manim_beanim.BlB
.. autoclass:: manim_beanim.Reference
.. autoclass:: manim_beanim.Equation
.. autoclass:: manim_beanim.Underbar
.. autoclass:: manim_beanim.Table
.. autoclass:: manim_beanim.Photo
.. autoclass:: manim_beanim.Post_It
.. autoclass:: manim_beanim.Text_General

Compatibility and extraction
----------------------------

.. autofunction:: manim_beanim.import_template_beanim
.. autofunction:: manim_beanim.extract_equations
.. autofunction:: manim_beanim.extract_citation

Rendering and styling contracts
-------------------------------

``BlB.next_point(rt=seconds)`` uses that duration for every step, including
steps after all bullets have been shown. Constructing an animation does not
advance the counter; completion does. Queued steps can be played in a Manim
``Succession``.

Component ``style`` mappings are immutable snapshots. Assign compatibility
attributes such as ``component.text_size = 24`` to update the snapshot.
Direction getters return independent arrays; assign a new direction to update
it. Styling changes affect subsequent rebuilds, rather than existing geometry.

Text and table rebuild methods replace their rendered children. User-added
children remain attached. Failed builds retain the previously rendered content.

``Title_Presentation``, ``Title_Section``, and ``Post_It`` accept optional
``max_width`` and ``max_height`` in Manim scene units. Fitting only shrinks
content. It preserves aspect ratio and never enlarges a short title.

Image clipping preserves planar rotation and shear, disconnected vector paths,
holes, and source transparency. Nonplanar masks and singular image transforms
raise ``ValueError``.
