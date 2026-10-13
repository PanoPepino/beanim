"""Compatible file-writing entry point for BibTeX citations."""
from ..data.citations import parse_citations
from ..data.dictionaries import write_dictionary
__all__ = ['extract_citation']

def extract_citation(bib_file, your_family_name, initials, output_file_name) -> None:
    """Write author/year citations while preserving names and quotation marks."""
    write_dictionary(parse_citations(bib_file, your_family_name, initials), output_file_name)
