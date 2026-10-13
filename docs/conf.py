"""Read-only documentation configuration, independent of working directory."""
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
project='Beanim'
author='Pano'
copyright='2025, Pano'
extensions=['sphinx.ext.autodoc','sphinx.ext.viewcode','sphinx.ext.napoleon','sphinx.ext.mathjax']
exclude_patterns = [
    '_build', 'Thumbs.db', '.DS_Store',
    '**/Tex', '**/Tex/**', '**/texts', '**/texts/**',
    '**/videos', '**/videos/**', '**/partial_movie_files', '**/partial_movie_files/**',
    '**/__pycache__', '**/__pycache__/**', '**/*_ManimCE_v*.png',
]
html_theme='furo'
html_static_path=['_static']
html_baseurl='https://panopepino.github.io/beanim/'
html_extra_path=['.nojekyll']
add_module_names=False
autodoc_class_signature='separated'
autoclass_content='class'
autodoc_default_options={'members':True,'exclude-members':'__weakref__,__init__'}
