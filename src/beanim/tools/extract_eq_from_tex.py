import re  # Some fancy libraries to find patterns. It seems so.

# The following code has been crafted with help of AI. Modifications introduced by not so intelligent human.

__all__ = ["extract_equations"]


def extract_equations(tex_file, output_file):
    """
    Extract labeled equations from a LaTeX file and save as a dictionary.

    This function parses a ``.tex`` file to find all labeled equations within
    ``\\begin{equation}...\\end{equation}`` environments and creates a dictionary
    mapping labels to equation content. The result is saved as a ``.txt`` file
    containing a Python dictionary format.

    :param tex_file: Path to the input LaTeX file to process.
    :type tex_file: str

    :param output_file: Path where the output dictionary file will be saved.
    :type output_file: str

    :return: Creates a ``.txt`` file containing a dictionary with equation labels as keys
        and cleaned equation content as values.
    :rtype: None

    :raises FileNotFoundError: If the input LaTeX file cannot be found.
    :raises IOError: If the output file cannot be written.

    .. note::

       - This function currently uses equation labels as dictionary keys, not equation numbers.
       - Equations containing ``align`` environments are automatically filtered out.
       - Commas and single backslashes are cleaned from equations for better slide display.

    .. warning::

       This function could be improved to reference equations by their displayed numbers
       in the paper rather than labels, but this requires further development.

    **Example usage:**

    .. code-block:: python

        from beanim import extract_equations

        extract_equations(
            tex_file="example_extract_ref_equation/latex_to_extract/latex_example.tex",
            output_file="example_extract_ref_equation/dictionaries_extracted/equations.txt"
        )

    **Output format:**

    The generated ``.txt`` file will contain a dictionary like:

    .. code-block:: python

        {
        'eq_label_1': 'E = mc^2',
        'eq_label_2': 'F = ma',
        }
    """
    with open(tex_file, "r", encoding="utf-8") as f:
        content = f.read()

    equation_dict = {}

    # Match equation environments (including starred versions)
    pattern = r"\\begin{equation\*?}(.*?)\\end{equation\*?}"

    for match in re.finditer(pattern, content, re.DOTALL):
        eq_content = match.group(1)

        # Filter out equations containing align environments
        if re.search(r"\\begin{align\b", eq_content):
            continue

        # Extract labels
        labels = re.findall(r"\\label{([^}]+)}", eq_content)

        if not labels:
            continue

        # Clean equation content
        cleaned = re.sub(r"\\(label|tag){[^}]+}|%.*", "", eq_content)
        cleaned = " ".join(cleaned.strip().split())

        equation_dict[labels[0]] = cleaned

    print(
        "---------------------------------------------------\n"
        "YOUR DICTIONARY OF EQUATIONS IS:\n"
        "---------------------------------------------------\n"
    )

    # Save to text file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("{\n")
        for label, eq in equation_dict.items():
            print(label + ": " + eq)
            # Majority of eqs. in papers end with stop or colon; In this way we get rid of them to display in slides.
            eq = eq.replace(",", "").replace("\\", "\\\\")
            f.write("'" + label + "'" + ": " + "'" + eq + "'" + ",\n")
        f.write("}\n")
