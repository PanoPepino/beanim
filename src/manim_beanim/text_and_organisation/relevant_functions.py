from ..my_imports import *

__all__ = ["split_dictionary_path", "check_file_exists"]


def split_dictionary_path(input_string):
    """
    Split a file path string at the last forward slash separator.

    This utility function separates a full file path into its directory component
    and filename component, which is useful for handling dictionary file paths.

    :param input_string: The file path string to split.
    :type input_string: str

    :return: A list containing two elements:
        1. The directory path (everything before the last ``/``)
        2. The filename (everything after the last ``/``)
    :rtype: list[str]

    **Example:**

    .. code-block:: python

        >>> split_dictionary_path("path/to/equations.txt")
        ['path/to', 'equations.txt']

        >>> split_dictionary_path("refs.txt")
        ['', 'refs.txt']
    """
    return input_string.rsplit("/", 1)


def check_file_exists(directory, filename):
    """
    Verify whether a specified file exists within a given directory.

    This function constructs a file path from the directory and filename components
    and checks for the file's existence using pathlib.

    :param directory: The directory path where the file should be located.
    :type directory: str or Path

    :param filename: The name of the file to check for.
    :type filename: str

    :return: True if the file exists at the specified location, False otherwise.
    :rtype: bool

    **Example:**

    .. code-block:: python

        >>> check_file_exists("./dictionaries", "equations.txt")
        True

        >>> check_file_exists("/nonexistent", "missing.txt")
        False
    """
    file_path = Path(directory) / filename
    return file_path.is_file()
