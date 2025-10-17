from .text_general import *
from ..my_imports import *
from .relevant_functions import *

__all__ = ["Equation"]


class Equation(Text_General, VGroup):
    """
        Create one or more LaTeX-formatted equations as part of a scene.

        This class inherits from :class:`Text_General` and supports rendering equations provided directly as LaTeX strings or indirectly via references to an external equation dictionary.

        :param content: A LaTeX string or a list of strings. Each string can either be:
            1. A LaTeX expression input directly (e.g., ``"e^{i\\pi} = -1"``), or
            2. A key that refers to an expression defined within a dictionary file.
        :type content: str or list[str]

        :param the_dictionary: Optional path to a `.txt` file containing a dictionary
            mapping keys to LaTeX equations. If set to ``"data_base"``, the class will use
            a built-in Beanim equation dictionary.
        :type the_dictionary: str, optional

        :param the_direction: Direction in which multiple equations will be arranged,
            e.g., ``DOWN`` or ``RIGHT``.
        :type the_direction: np.ndarray, default=DOWN

        :raises FileNotFoundError: if the specified dictionary file cannot be found (when used).
        :raises KeyError: if a specified equation key is not found in the dictionary.

        :seealso: :class:`Text_General`

        .. note::

           - Dictionary-based expressions allow equation management via external .txt files.
           - For extracting LaTeX equations into dictionary files, see the ``tools`` package.

        **Example usage:**

        .. code-block:: python

            from manim import *
            from manim_beanim import *

            class Equation_Test(Scene):
                def construct(self):
                    eq_from_data_base = Equation(
                        content=["equation_data_base_1", "equation_data_base_3"],
                        the_dictionary="data_base",
                        text_size=30,
                        the_direction=DOWN,
                        aligned_direction=LEFT,
                    )

                    eq_from_extract = Equation(
                        content=["equation_extract_1", "equation_extract_3"],
                        the_dictionary="example_extract_ref_equation/dictionaries_extracted/equations.txt",
                        text_size=30,
                        the_direction=DOWN,
                        aligned_direction=LEFT,
                    )

                    eq_from_manual_input = Equation(
                        content=["x^{2}+y^{2} = R^{2}, \\quad", "e^{i \\pi} = -1"],
                        text_size=30,
                        the_direction=RIGHT,
                    )

                    self.add(VGroup(
                        eq_from_data_base,
                        eq_from_extract,
                        eq_from_manual_input
                    ))
        """

    def __init__(self,
                 **kwargs):
        super().__init__(**kwargs)

        # At this point, two paths open:
        # i) Dictionary is not provided -> the_equation is a string or list of string with direct inputs you add manually
        # ii) dictionary is provided/use of data_base command (the ref is a string or list of strings with keys of the dictionary located at the provided path)
        if self.dictionary is None:
            self.handle_no_dictionary()
        else:
            self.handle_with_dictionary("equations")

    # Text_General method overriden to change Tex to MathTex.

    def get_tex_from_dict(self, the_piece, dictionary):
        """
        Returns a Tex object for a given pieceerence key from the dictionary.
        """

        if the_piece in dictionary:
            return MathTex(dictionary[the_piece], font_size=self.text_size, color=self.text_color)

        else:
            return MathTex(f"Missing: {the_piece}", font_size=self.text_size, color=self.text_color)

    def handle_no_dictionary(self):
        """
        No dictionary is provided. This function checks if the_piece is a string or list of strings. If the latter, it will add one by one to a VGroup. It then calls method _add_decorator (see below)
        """

        print('OVERRIDE ' + self.__class__.__name__)

        if isinstance(self.content, (list, tuple)):
            self.chosen_content = VGroup(*[
                MathTex(piece, font_size=self.text_size, color=self.text_color)
                for piece in self.content])
            self.chosen_content.arrange(self.direction, buff=0.2)
        else:
            print(self.content)
            print(self.__class__.__name__)
            self.chosen_content = MathTex(self.content, font_size=self.text_size, color=self.text_color)
        self.add_decorator(self.chosen_content)
