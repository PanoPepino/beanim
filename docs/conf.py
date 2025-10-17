# Configuration file for the Sphinx documentation builder.

import re
import os
import sys

# To update or create new documentation, do as follows:
# 1) Navigate to your package (not the src folder) and create a docs folder.
# 2) In docs folder, run sphinx-apidoc -o ./api ../src/name_pkg. This will load all modules information inside the folder api, for simplicity and clean set up when creating html
# 3) Modify your conf.py file to the right path. Copy and paste this conf.py file. It is quite complete.
# 4) Modify your index.rst to include a nice presentation and stuff. You can create additional .rst files in other folders or ar the same level. In the ..toctree of index.rst, you can just add those files with extra info. This ..toctree will include an api/modules reference.
# 5) Go to api/modules.rst and modify it so that it display your desired modules.
# 6) Go to each module and remove those parts/headings you do not like (i.e. Submodules, Module contents, etc)
# 7) Using vscode or any other tool, remove all :undoc-members: in all .rst files. This will help you to get rid of methods that are inherited.
# 8) Run make clean html. The inbuilt functions in conf.py will get rid of annoying naming (i.e. package.module.submodule.class -> class) and also will remove __init__ or similar documentation.
# 9) Double check everything makes sense. Run make clean html again and evaluate result.

# -- Path setup --------------------------------------------------------------

# Add the parent directory to sys.path to find your package
sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, os.path.abspath('../src/manim_beanim'))


# -- Project information -----------------------------------------------------

project = 'Beanim'
copyright = '2025, Pano'
author = 'Pano'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',                       # Core autodoc functionality
    'sphinx.ext.autosummary',                   # Generate summary tables
    'sphinx.ext.viewcode',                      # Add source code links
    'sphinx.ext.napoleon',                      # Support for NumPy and Google style docstrings
    'sphinx.ext.intersphinx',                   # Link to other project's documentation
    'sphinx.ext.mathjax',                       # Render math expressions
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
nitpicky = False

html_static_path = ['_static']
html_logo = "_static/media/slide.svg"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'furo'


# Add any paths that contain custom static files (such as style sheets) here,
html_static_path = ['_static']
html_baseurl = 'https://panopepino.github.io/beanim/'

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


def clean_api_titles(api_dir="docs/source/api"):
    """
    Change .rst file titles to use only the leaf name (shortest part after last dot),
    with underscores not escaped, and remove any trailing 'package' or 'module'.
    """
    for fname in os.listdir(api_dir):
        if fname.endswith(".rst"):
            path = os.path.join(api_dir, fname)
            with open(path, "r", encoding="utf8") as f:
                lines = f.readlines()
            # Sphinx-apidoc escapes _ as \_ in headings, so match either
            title_line = lines[0].strip()
            # Unescape underscores for processing
            decoded_title = title_line.replace("\\_", "_")
            # Match: e.g. beanim.text_and_organisation.blb module
            found = re.match(r"^([\w\.]+) (package|module)$", decoded_title)
            if found:
                leaf = found.group(1).split(".")[-1]
                # Write unescaped clean title
                new_title = leaf + "\n"
                lines[0] = new_title
                lines[1] = "=" * len(leaf) + "\n"
                with open(path, "w", encoding="utf8") as f:
                    f.writelines(lines)


clean_api_titles("api")

# To remove documentation on functions that do not belong to the package


def skip_inherited_members(app, what, name, obj, skip, options):
    if hasattr(obj, "__objclass__") and obj.__objclass__ is not None:
        currentclass = options.get("class", None)
        print(f"Checking {name}: objclass={obj.__objclass__.__name__} currentclass={currentclass}")
        if currentclass and obj.__objclass__.__name__ != currentclass:
            print(f"Skipping {name} because inherited")
            return True
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip_inherited_members)


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
