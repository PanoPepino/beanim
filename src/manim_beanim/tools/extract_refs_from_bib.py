# The following code has been crafted with help of AI. Modifications introduced by not so intelligent human.

from pybtex.database import *  # libraries to manipulate references

__all__ = ["extract_citation"]


def extract_citation(bib_file, your_family_name, initials, output_file_name):
    """
    Build a citation dictionary from a BibTeX file with customizable author formatting.

    This function parses a ``.bib`` file and creates a dictionary keyed by BibTeX citation keys,
    with values containing formatted author lists. It allows for personal name substitution
    (e.g., replacing your full name with initials) and includes eprint numbers when available.

    :param bib_file: Path to the input BibTeX (``.bib``) file.
    :type bib_file: str

    :param your_family_name: Your family name to be replaced with initials in citations.
        This is common practice in theoretical physics publications.
    :type your_family_name: str

    :param initials: Your initials to substitute for your full name in citations.
    :type initials: str

    :param output_file_name: Path and filename for the output dictionary file.
    :type output_file_name: str

    :return: Creates a ``.txt`` file containing the citation dictionary and prints the results.
    :rtype: None

    :raises FileNotFoundError: If the input BibTeX file cannot be found.
    :raises IOError: If the output file cannot be written.

    .. note::

       - Entries without eprint numbers will be flagged with a warning message.
       - The function automatically strips quote marks from author names.
       - The output format is designed for easy integration with Beanim reference systems.

    **Example usage:**

    .. code-block:: python

        from manim_beanim import extract_citation

        extract_citation(
            bib_file="example_extract_ref_equation/latex_to_extract/refs_example.bib",
            your_family_name="Perico",
            initials="PP",
            output_file_name="example_extract_ref_equation/dictionaries_extracted/refs.txt"
        )

    **Output format:**

    The generated ``.txt`` file will contain a dictionary like:

    .. code-block:: python

        {
        "cite_key_1": ["Smith", "Jones", "PP", "1234.5678"],
        "cite_key_2": ["Brown", "Davis", "add manually"],
        }

    where each list contains author surnames, your initials (if applicable), and eprint numbers.
    """
    bib_data = parse_file(bib_file)
    author_dict = {}

    for entry_key, entry in bib_data.entries.items():
        authors = []

        for person in entry.persons.get("author", []):
            if person.last_names == [your_family_name]:
                authors.append(initials)
            else:
                authors.append(" ".join(person.last_names))

        if "year" in entry.fields:
            authors.append(entry.fields["year"].strip())
        else:
            print(f"⚠️ Entry \\cite{{{entry_key}}} has no eprint number. Please check it manually.")
            authors.append("add manually")

        authors = [author.strip("'") for author in authors]
        author_dict[entry_key] = authors

    # Print and save output
    print(
        "---------------------------------------------------\n"
        "YOUR DICTIONARY OF REFERENCES IS:\n"
        "---------------------------------------------------\n"
    )

    with open(output_file_name, "w") as f:
        f.write("{\n")
        for ref_id, authors in author_dict.items():
            author_list = [author for author in authors]
            new_authors = ", ".join(author_list)
            out_line = f'"{ref_id}": {"'[" + new_authors + "]'"},\n'
            f.write(out_line)
            print(out_line.strip())
        f.write("}\n")
