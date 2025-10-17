from ..my_imports import *

__all__ = ["Text_General"]


class Text_General(VGroup):
    """
    Base class for all Beanim TeX-supporting rendering components.

    This class provides standardized behavior and styling for any derived classes that generate
    LaTeX-rendered content using Manim. It arranges and optionally decorates text content, with
    support for loading content from string literals or from dictionary sources.

    Subclasses may override rendering behavior while keeping the base logic for positioning,
    styling, and decoration.

    :param content: The primary text to display. May be either a string or list of strings.
        Strings should contain valid LaTeX. Each list entry will be rendered individually.
    :type content: str or list[str]

    :param dictionary: Optional path to a dictionary file used to resolve content labels
        into LaTeX code. If set to ``"data_base"``, a built-in library dictionary is used.
    :type dictionary: str, optional

    :param direction: Direction in which multiple entries will be stacked (e.g., ``RIGHT``, ``DOWN``).
    :type direction: np.ndarray

    :param aligned_direction: Alignment edge for stacked/arranged objects (e.g., ``LEFT``, ``UP``).
    :type aligned_direction: np.ndarray or list

    :param text_size: Font size of the rendered text content.
    :type text_size: float

    :param text_color: Manim color of the LaTeX text.
    :type text_color: ParsableManimColor

    :param decorator_presence: Type of decoration to apply. Options include:
        ``"box"``, ``"box_long_left"``, ``"box_long_right"``, ``"back_frame"``, ``"no"``.
    :type decorator_presence: str

    :param decorator_color: Outline or fill color used in decoration elements.
    :type decorator_color: ParsableManimColor

    :param decorator_stroke_width: Stroke width of the decorative borders.
    :type decorator_stroke_width: float

    :param corner_rad: Scalar used in combination with ``corner_rad_direction`` to round rectangle corners.
    :type corner_rad: float

    :param corner_rad_direction: List controlling corner rounding; format: [top-left, top-right, bottom-right, bottom-left].
    :type corner_rad_direction: list[int]

    :param fill_opa: Opacity for backgrounds (e.g., for surround boxes or frames).
    :type fill_opa: float

    :param tightness: Buffer/margin around the decorated content.
    :type tightness: float

    :param stroke_opa: Opacity of the border stroke around decorations.
    :type stroke_opa: float

    :param dot_scale: Scale of bullet points (used in subclasses like bullet lists).
    :type dot_scale: float

    :param kwargs: Other keyword arguments passed to Manim's :class:`VGroup`.

    :raises FileNotFoundError: If the given dictionary file path is invalid.
    :raises KeyError: If requested keys are not found in the dictionary.

    .. note::

       This class is not intended to be used directly in scenes, but rather subclassed to create content
       blocks like paragraphs, bullet points, or formulas. See subclasses like :class:`Equation` or
       :class:`BlB` for examples of how this class is used.

       To create your own dictionaries for content control, see the functions in the ``tools`` package,
       such as ``extract_pieces_from_bib()``.

    :seealso:
        - :class:`Equation`
        - :class:`BlB`
        - :class:`VGroup`
    """

    def __init__(
            self,
            content=None,
            dictionary=None,
            direction: np.ndarray = RIGHT,
            aligned_direction: np.ndarray = [0, 0, 0],
            text_size: float = 35,
            text_color: ParsableManimColor = WHITE,
            decorator_presence: str = "no",
            decorator_color: ParsableManimColor = WHITE,
            decorator_stroke_width: float = 1,
            corner_rad: float = 0,
            corner_rad_direction: list = [0, 0, 0, 0],
            fill_opa: float = 0,
            tightness: float = 0.3,
            stroke_opa: float = 1,
            dot_scale: float = 1,
            **kwargs) -> VGroup:

        super().__init__(**kwargs)
        self.content = content
        self.dictionary = dictionary
        self.direction = direction
        self.aligned_direction = aligned_direction
        self.text_size = text_size
        self.text_color = text_color
        self.decorator_presence = decorator_presence
        self.decorator_color = decorator_color
        self.fill_opa = fill_opa
        self.tightness = tightness
        self.decorator_stroke_width = decorator_stroke_width
        self.stroke_opa = stroke_opa
        self.corner_rad = list(corner_rad * np.array(corner_rad_direction))
        self.crad = corner_rad  # Special for box with title
        self.dot_scale = dot_scale

    def handle_no_dictionary(self):
        """
        Handle rendering when no dictionary is provided.

        If ``content`` is provided directly as a string or list of strings, this method creates
        a Tex object (or a group of Tex objects) and arranges them visually. Each element is
        styled according to the object's text attributes and arranged using the specified direction
        and alignment.

        After rendering the Tex objects, this method applies any decorative box if defined by
        :attr:`decorator_presence`, using the :meth:`add_decorator` method.

        .. note::

           This method only processes direct input; if a dictionary path is provided instead,
           :meth:`handle_with_dictionary` is used.

        **Calls:**
            - :meth:`add_decorator` — applies a decorative box or frame to the rendered object(s).

        **Modifies:**
            - ``self.chosen_content`` — stores the generated content (either a single Tex or a VGroup of Tex).
            - Adds the content to the object hierarchy via ``self.add(...)``.
        """
        print('printing your manually input ' + self.__class__.__name__)

        if isinstance(self.content, (list, tuple)):
            self.chosen_content = VGroup(*[
                Tex(piece, font_size=self.text_size, color=self.text_color)
                for piece in self.content])
            self.chosen_content.arrange(self.direction, aligned_edge=self.aligned_direction, buff=0.2)
        else:
            print(self.content)
            self.chosen_content = Tex(self.content, font_size=self.text_size, color=self.text_color)
        self.add_decorator(self.chosen_content)

    def handle_with_dictionary(self, dic_in_data_base):
        """
        Handle LaTeX rendering when a dictionary file is provided.

        If a dictionary path is passed via the ``dictionary`` parameter, this method loads
        the corresponding key-to-LaTeX mapping from the file and uses it to render the specified
        equation(s). Keys are resolved using :meth:`load_dictionary`, and their values are converted
        into Tex objects using :meth:`get_tex_from_dict`.

        If ``dictionary == "data_base"``, an internal library dictionary is used by locating
        a predefined ``.txt`` file relative to the current module.

        **Steps performed:**
            1. The dictionary path is split into directory and filename using :meth:`split_dictionary_path`.
            2. The dictionary file is loaded into memory using :meth:`load_dictionary`.
            3. Each element in ``content`` is resolved to a LaTeX expression using :meth:`get_tex_from_dict`.
            4. All rendered content is arranged and passed through :meth:`add_decorator` to apply optional styling.

        :param dic_in_data_base: The base name of the dictionary file when using internal dictionaries.
        :type dic_in_data_base: str

        **Creates:**
            - ``self.chosen_content`` : Either a single Tex object or a VGroup of Tex objects built from the dictionary.

        :raises FileNotFoundError: If the dictionary path or file does not exist.
        :raises KeyError: If any key in ``content`` is not found in the loaded dictionary.

        :seealso:
            - :meth:`load_dictionary`
            - :meth:`get_tex_from_dict`
            - :meth:`add_decorator`
            - :meth:`split_dictionary_path`
        """
        if self.dictionary == "data_base":
            self.dictionary = path.join(path.dirname(__file__), "dictionary_text_organisation/"+dic_in_data_base+".txt")
            my_path = self.split_dictionary_path(self.dictionary)[0]
            my_file = self.split_dictionary_path(self.dictionary)[-1]
        else:
            my_path = self.split_dictionary_path(self.dictionary)[0]
            my_file = self.split_dictionary_path(self.dictionary)[-1]

        if not self.check_file_exists(my_path, my_file):
            print(
                "---------------------------------------------------\n"
                "Dictionary file not found. Please check the path or generate the dictionary.\n"
                "Consider running the function extract_pieces_from_bib provided in this library to create a .txt file containing the dictionary with the desired equations.\n"
                "---------------------------------------------------\n"
            )

        load_the_dic = self.load_dictionary()  # This loads the function of the dictionary. (See below)

        if isinstance(self.content, (list, tuple)):
            self.chosen_content = VGroup()
            for piece in self.content:
                print('printing piece: ' + piece + ' which is in file and dictionary: ' + my_path + ' '+my_file)
                tex_obj = self.get_tex_from_dict(piece, load_the_dic)
                self.chosen_content.add(tex_obj)
            self.chosen_content.arrange(self.direction, aligned_edge=self.aligned_direction, buff=0.1)

        else:  # for this to work for a single entry without [].
            self.chosen_content = self.get_tex_from_dict(self.content, load_the_dic)

        self.add_decorator(self.chosen_content)

    def load_dictionary(self):
        """
        Load the dictionary from the specified file.

        Opens and reads a dictionary file, then evaluates its contents as a Python dictionary.
        The file should contain a valid Python dictionary structure as a string.

        :return: The loaded dictionary containing key-value mappings.
        :rtype: dict

        :raises FileNotFoundError: If the dictionary file cannot be found.
        :raises SyntaxError: If the dictionary file contains invalid Python syntax.

        .. warning::

           This method uses ``eval()`` to parse the dictionary file contents, which can be
           a security risk if the file contains untrusted code. Ensure dictionary files
           contain only trusted data.
        """
        with open(self.dictionary, mode='r') as open_the_dic:
            read_the_dic = open_the_dic.read()
            load_the_dic = eval(read_the_dic)
            open_the_dic.close()

        return load_the_dic

    def get_tex_from_dict(self, the_piece, dictionary):
        """
        Create a Tex object for a given key from the dictionary.

        Looks up the provided key in the dictionary and creates a styled Tex object
        from the corresponding value. If the key is not found, creates a "Missing" placeholder.

        :param the_piece: The dictionary key to look up.
        :type the_piece: str

        :param dictionary: The dictionary containing key-value mappings.
        :type dictionary: dict

        :return: A Tex object containing either the dictionary value or a missing key message.
        :rtype: Tex
        """
        if the_piece in dictionary:
            return Tex(dictionary[the_piece], font_size=self.text_size, color=self.text_color)
        else:
            return Tex(f"Missing: {the_piece}", font_size=self.text_size, color=self.text_color)

    def add_decorator(self, mobject):
        """
        Add a decorative element around the mobject based on the decorator settings.

        Applies various types of decorative boxes or frames around the provided mobject
        according to the ``decorator_presence`` setting. Supports different box styles
        including standard boxes, extended boxes, and full-width frames.

        :param mobject: The Manim object to decorate.
        :type mobject: Mobject

        .. note::

           If ``decorator_presence`` is set to ``"no"`` or any unrecognized value,
           the mobject is added without decoration.
        """
        mobject.set_z_index(5)
        if getattr(self, "decorator_presence", None) == "box":
            box = SurroundingRectangle(
                mobject,
                corner_radius=self.corner_rad,
                buff=self.tightness,
                stroke_width=self.decorator_stroke_width,
                color=self.decorator_color,
                fill_opacity=self.fill_opa,
                stroke_opacity=self.stroke_opa)

            self.add(mobject, box)

        elif getattr(self, "decorator_presence", None) == "box_long_right":
            self.box_long = RoundedRectangle(
                height=mobject.get_height() + self.tightness,
                width=mobject.get_width() + 10,
                stroke_width=self.decorator_stroke_width,
                color=self.decorator_color,
                fill_opacity=self.fill_opa,
                corner_radius=self.corner_rad,
                stroke_opacity=self.stroke_opa,
            )
            self.box_long.next_to(
                mobject.get_left(),
                RIGHT,
                aligned_edge=LEFT,
                buff=-1/2*self.tightness,
            )
            t_sec = VGroup(mobject, self.box_long)
            self.add(t_sec)

        elif getattr(self, "decorator_presence", None) == "box_long_left":
            self.box_long = RoundedRectangle(
                height=mobject.get_height() + self.tightness,
                width=mobject.get_width() + 10,
                stroke_width=self.decorator_stroke_width,
                color=self.decorator_color,
                fill_opacity=self.fill_opa,
                corner_radius=self.corner_rad,
                stroke_opacity=self.stroke_opa,
            )
            self.box_long.flip()
            self.box_long.next_to(
                mobject.get_right(),
                LEFT,
                aligned_edge=RIGHT,
                buff=-self.tightness,
            )
            t_sec = VGroup(mobject, self.box_long)
            self.add(t_sec)

        elif getattr(self, "decorator_presence", None) == "back_frame":
            self.rectangle = RoundedRectangle(
                height=mobject.get_height() + 1.5*self.tightness,
                width=config.frame_width + 0.1,
                stroke_width=self.decorator_stroke_width,
                corner_radius=self.corner_rad,
                color=self.decorator_color,
                fill_opacity=self.fill_opa,
                stroke_opacity=self.stroke_opa
            )
            self.rectangle.move_to([0,mobject.get_y(),0])
            self.add(mobject, self.rectangle)

        else:
            self.add(mobject)

    def split_dictionary_path(self, input_string):
        """
        Split a string into two parts using the last ``"/"`` character as the separator.

        This is typically used to separate a full file path into its directory and filename components.

        :param input_string: The input path-like string to split.
        :type input_string: str

        :return: A list with two elements:
            1. The path leading up to the last slash,
            2. The remaining string after the last slash (typically the filename).
        :rtype: list[str]

        **Example:**

        .. code-block:: python

            >>> self.split_dictionary_path("some/path/to/file.txt")
            ['some/path/to', 'file.txt']
        """
        return input_string.rsplit("/", 1)

    def check_file_exists(self, directory, filename):
        """
        Check whether a file exists in the specified directory.

        :param directory: The directory path to search within.
        :type directory: str or Path

        :param filename: The name of the file to look for within the directory.
        :type filename: str

        :return: True if the file exists, False otherwise.
        :rtype: bool

        **Example:**

        .. code-block:: python

            >>> self.check_file_exists("path/to/dir", "file.txt")
            True
        """
        file_path = Path(directory) / filename
        return file_path.is_file()
