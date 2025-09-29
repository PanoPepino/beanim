
# Configuration file for the Sphinx documentation builder.

import re
import os
import sys


# -- Path setup --------------------------------------------------------------

# Add the parent directory to sys.path to find your package
sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, os.path.abspath('../src/beanim'))


# -- Project information -----------------------------------------------------

project = 'Beanim'
copyright = '2025, Pano'
author = 'Pano'

# The short X.Y version

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',                       # Core autodoc functionality
    'sphinx.ext.autosummary',                   # Generate summary tables
    'sphinx.ext.viewcode',                      # Add source code links
    'sphinx.ext.napoleon',                      # Support for NumPy and Google style docstrings
    'sphinx.ext.intersphinx',                   # Link to other project's documentation
    'sphinx.ext.mathjax',                       # Render math expressions
    'sphinx_autodoc_typehints',
    'sphinx_copybutton',
    'myst_parser',
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
nitpicky = False


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'furo'


# Add any paths that contain custom static files (such as style sheets) here,
html_static_path = ['_static']
html_baseurl = 'https://yourusername.github.io/beanim/'

# Ensure proper file extensions for GitHub Pages
html_file_suffix = '.html'
html_link_suffix = '.html'

# Add a .nojekyll file to disable Jekyll processing
html_extra_path = ['.nojekyll']


# To modify apparence of modules inside the documentation
add_module_names = False                        # This avoids long names like beanim.text....class_name
toc_object_entries = True                       # This allows to show the table of content-list to the right of the screen
toc_object_entries_show_parents = "hide"        # This avoids showing the parents of each class or function
# This makes that the class name goes alongs, without any parameters inside. Everything is loaded in __init__.
autodoc_class_signature = "separated"


# This value selects what content will be inserted into the main body of an autoclass directive.
autoclass_content = 'class'  # Include both class docstring and __init__ docstring

# This value is a list of autodoc directive flags that should be automatically applied to all autodoc directives.
autodoc_default_options = {
    'members': True,
    # And this gets rid of the __init__ so the documentation is not oversaturated.
    'exclude-members': '__weakref__, __init__'
}


# Boolean indicating whether to scan all found documents for autosummary directives,
# and to generate stub pages for each.
autosummary_generate = False


# -- Options for mathjax extension -------------------------------------------

# Use MathJax to render math
mathjax_path = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'

# MathJax configuration
mathjax3_config = {
    'tex': {
        'inlineMath': [['$', '$'], ['\\(', '\\)']],
        'displayMath': [['$$', '$$'], ['\\[', '\\]']],
    }
}
