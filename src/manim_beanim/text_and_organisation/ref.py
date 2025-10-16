from .text_general import *
from ..my_imports import *

__all__ = ['Reference']


class Reference(Text_General):
    """
    Create academic-style citations and references formatted within brackets.

    This class inherits from :class:`Text_General` and generates references in the format
    ``[surname1, surname2, ..., ref]``. References can be provided directly as strings
    or retrieved from a dictionary file using lookup keys.

    :param content: Reference content to display. Can be either direct reference strings
        (e.g., ``"[Smith et al., 2023]"``) or dictionary keys that map to reference entries.
    :type content: str or list[str]

    :param the_dictionary: Optional path to a ``.txt`` file containing reference mappings.
        If set to ``"data_base"``, uses the built-in Beanim reference dictionary.
    :type the_dictionary: str, optional

    :param the_direction: Direction for arranging multiple references when content is a list.
    :type the_direction: np.ndarray, default=RIGHT

    :param kwargs: Additional parameters passed to :class:`Text_General`.

    .. note::

       Reference dictionaries should map keys to properly formatted citation strings,
       typically in the format ``[Author, Publication, Year]``.

    **Example usage:**

    .. code-block:: python

        from manim import *
        from beanim import *

        class Ref_Test(Scene):
            def construct(self):
                ref_from_data_base = Reference(
                    content=['ref_data_base_1', 'ref_data_base_2', 'ref_data_base_3'],
                    the_dictionary='data_base'
                )

                ref_from_extract = Reference(
                    the_dictionary="example_extract_ref_equation/dictionaries_extracted/refs.txt",
                    content=['ref_extract_1', 'ref_extract_2']
                )

                ref_from_manual_input = Reference(
                    content='[Manually input ref, PP, 2025]'
                )

                references = VGroup(
                    ref_from_data_base,
                    ref_from_extract,
                    ref_from_manual_input
                ).arrange(DOWN, aligned_edge=LEFT)

                self.add(references)

    :seealso: :class:`Text_General`
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Choose processing path based on dictionary availability
        if self.dictionary is None:
            self.handle_no_dictionary()
        else:
            self.handle_with_dictionary("refs")
