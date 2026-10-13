"""Compatible file-writing entry point for equation extraction."""
from ..data.equations import parse_equations
from ..data.dictionaries import write_dictionary
__all__ = ['extract_equations']

def extract_equations(tex_file, output_file) -> None:
    """Write extracted equations as JSON (.json) or safe Python literals (.txt)."""
    write_dictionary(parse_equations(tex_file), output_file)
