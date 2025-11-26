from ..my_imports import *
__all__ = ["Table"]


class Table(VGroup):
    """
    Simplify creation and decoration of tables in Manim, with optional dictionary loading and styling.

    This class supports manual content input (a list of table rows) or dictionary-based loading of structured content (e.g., mathematical expressions). It offers extensive customization options, including color themes, corner radii, decorative borders, and row highlighting.

    :param content: Table content as a list of rows (each row is a list of elements), or a dictionary key.
    :type content: list[list] or str

    :param dictionary: Optional path to a dictionary file for loading content. If ``"data_base"``, uses the built-in Beanim table dictionary.
    :type dictionary: str, optional

    :param highlight_top: Whether to highlight the top row. Use ``"yes"`` (default) to enable.
    :type highlight_top: str

    :param text_size: Font size for each table cell. Default is ``55``.
    :type text_size: float

    :param text_color: Color of text in the table. Default is ``WHITE``.
    :type text_color: ParsableManimColor

    :param decorator_presence: Type of decoration to apply. Use ``"box"`` to wrap content in a frame.
    :type decorator_presence: str

    :param decorator_color: Primary color for the decorator. Default is ``WHITE``.
    :type decorator_color: ParsableManimColor

    :param decorator_color_2: Highlight color for top row cell 1. Default is ``RED``.
    :type decorator_color_2: ParsableManimColor

    :param decorator_color_3: Highlight color for top row cell 2. Default is ``BLUE``.
    :type decorator_color_3: ParsableManimColor

    :param decorator_color_4: Highlight color for top row cell 3. Default is ``GREEN``.
    :type decorator_color_4: ParsableManimColor

    :param decorator_stroke_width: Stroke width for decorator borders. Default is ``1``.
    :type decorator_stroke_width: float

    :param corner_rad: Corner radius for decorator boxes. Default is ``0.1``.
    :type corner_rad: float

    :param corner_rad_direction: List of four ints controlling which corners are rounded:
        [top-left, top-right, bottom-right, bottom-left]. Default is ``[1, 1, 1, 1]``.
    :type corner_rad_direction: list[int]

    :param fill_opa: Fill opacity for decorative backgrounds. Default is ``0.1``.
    :type fill_opa: float

    :param h_tightness: Horizontal padding inside table cells. Default is ``0.5``.
    :type h_tightness: float

    :param v_tightness: Vertical padding inside table cells. Default is ``0.5``.
    :type v_tightness: float

    :param tightness: Padding around the decorator box. Default is ``0``.
    :type tightness: float

    :param stroke_opa: Opacity of table/border strokes. Default is ``1``.
    :type stroke_opa: float

    :param kwargs: Additional keyword arguments passed to :class:`VGroup`.

    .. note::

       When using dictionary content, the dictionary file should map keys to row data lists.
       See :meth:`handle_with_dictionary` for details.

    **Example usage:**

    .. code-block:: python

        from manim import *
        from manim_beanim import Table

        class Example_Table(Scene):
            def construct(self):
                table1 = Table(content=[["1", "2"], ["3", "4"]])
                table2 = Table(content="table_key", dictionary="data_base")
                self.add(VGroup(table1, table2).arrange(DOWN))
    """

    def __init__(
        self,
        content=None,
        dictionary=None,
        highlight_top="yes",
        text_size: float = 55,
        text_color: ParsableManimColor = WHITE,
        decorator_presence: str = "box",
        decorator_color: ParsableManimColor = WHITE,
        decorator_color_2: ParsableManimColor = RED,
        decorator_color_3: ParsableManimColor = BLUE,
        decorator_color_4: ParsableManimColor = GREEN,
        decorator_stroke_width: float = 1,
        corner_rad: float = 0.1,
        corner_rad_direction: list = [1, 1, 1, 1],
        fill_opa: float = 0.1,
        h_tightness: float = 0.5,
        v_tightness: float = 0.5,
        tightness: float = 0,
        stroke_opa: float = 1,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.content = content
        self.dictionary = dictionary
        self.highlight_top = highlight_top
        self.text_size = text_size
        self.text_color = text_color
        self.decorator_presence = decorator_presence
        self.decorator_color = decorator_color
        self.decorator_color_2 = decorator_color_2
        self.decorator_color_3 = decorator_color_3
        self.decorator_color_4 = decorator_color_4
        self.decorator_stroke_width = decorator_stroke_width
        self.corner_rad = corner_rad
        self.corner_rad_all = list(corner_rad * np.array(corner_rad_direction))
        self.crad = corner_rad  # Special for box with title
        self.fill_opa = fill_opa
        self.h_tightness = h_tightness
        self.v_tightness = v_tightness
        self.tightness = tightness
        self.stroke_opa = stroke_opa

        if self.dictionary is None:
            self.handle_no_dictionary()
        else:
            self.handle_with_dictionary("tables")

    def handle_no_dictionary(self):
        """
        Render table directly from manually provided content.

        Creates a :class:`MathTable` from the provided content list and applies decoration.

        **Calls:**
            - :meth:`add_decorator`
        """
        self.chosen_content = MathTable(
            self.content,
            line_config={"stroke_width": self.decorator_stroke_width,
                         "color": self.text_color},
            include_outer_lines=False,
            v_buff=self.v_tightness,
            h_buff=self.h_tightness,
            stroke_opacity=self.stroke_opa,
        ).set(color=self.text_color)
        self.add_decorator(self.chosen_content)

    def handle_with_dictionary(self, dic_in_data_base):
        """
        Render table by loading content from a dictionary file.

        If ``dictionary == "data_base"``, uses the built-in table dictionary. Otherwise
        loads from the provided path, splits directory and filename, and then constructs
        a :class:`MathTable` from the retrieved data.

        :param dic_in_data_base: Base name for built-in dictionary files.
        :type dic_in_data_base: str
        """
        if self.dictionary == "data_base":
            self.dictionary = path.join(
                path.dirname(__file__),
                "dictionary_graphing_objects/" + dic_in_data_base + ".txt"
            )
        my_path, my_file = self.split_dictionary_path(self.dictionary)

        if not self.check_file_exists(my_path, my_file):
            print("Dictionary file not found; generating manually may be required.")

        chosen_dic = self.load_dictionary()
        data = chosen_dic[self.content]
        self.chosen_content = MathTable(
            data,
            line_config={"stroke_width": self.decorator_stroke_width,
                         "color": self.text_color},
            include_outer_lines=False,
            v_buff=self.v_tightness,
            h_buff=self.h_tightness,
            stroke_opacity=self.stroke_opa,
        ).set(color=self.text_color)
        self.add_decorator(self.chosen_content)

    def load_dictionary(self):
        """
        Load and parse a dictionary file containing table data.

        :return: Parsed dictionary mapping content keys to table rows.
        :rtype: dict
        """
        with open(self.dictionary, mode='r') as f:
            text = f.read()
            return ast.literal_eval(text)

    def add_highlight_top_row(self):
        """
        Highlight the top row of the table using specified decorator colors.
        """
        row = self.filter_type()
        colors = [self.decorator_color_2, self.decorator_color_3, self.decorator_color_4]
        for i in range(1, len(row) + 1):
            corner = [1, 0, 0, 0] if i == 1 else ([0, 0, 0, 1] if i == len(row) else [0, 0, 0, 0])
            self.chosen_content.add_highlighted_cell((1, i), color=colors[i % len(
                colors)], corner_radius=list(self.corner_rad * np.array(corner)))

    def filter_type(self):
        """
        Determine the top row data regardless of content type.

        :return: The first row of the table content.
        :rtype: list
        """
        if isinstance(self.content, str):
            return self.load_dictionary()[self.content][0]
        return self.content[0]

    def add_decorator(self, mobject):
        """
        Add decorators (highlight row and optional box) around the table.

        This method first calls :meth:`add_highlight_top_row`, then wraps the
        table in a box if ``decorator_presence == "box"``.
        """
        self.add_highlight_top_row()
        if self.decorator_presence == "box":
            box = SurroundingRectangle(
                mobject,
                corner_radius=self.corner_rad_all,
                buff=4*self.tightness,
                stroke_width=self.decorator_stroke_width,
                color=self.decorator_color,
                fill_opacity=self.fill_opa,
                stroke_opacity=self.stroke_opa
            )
            self.add(mobject, box)
        else:
            self.add(mobject)

    def split_dictionary_path(self, input_string):
        """
        Split a path string at the last slash into directory and filename.

        :param input_string: The full path to split.
        :type input_string: str

        :return: [directory, filename]
        :rtype: list[str]

        **Example:**

        .. code-block:: python

            >>> self.split_dictionary_path("path/to/file.txt")
            ['path/to', 'file.txt']
        """
        return input_string.rsplit("/", 1)

    def check_file_exists(self, directory, filename):
        """
        Check if a file exists in the given directory.

        :param directory: Directory path to check.
        :type directory: str or Path

        :param filename: Filename to look for.
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
