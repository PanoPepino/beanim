"""Shared static documentation manifest, independent of Manim imports."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LEGACY_MODULES = (
    'modules', 'manim_beanim', 'manim_beanim.figures',
    'manim_beanim.graphing_objects',
    'manim_beanim.graphing_objects.dictionary_graphing_objects',
    'manim_beanim.other_objects', 'manim_beanim.templates',
    'manim_beanim.templates.collection', 'manim_beanim.text_and_organisation',
    'manim_beanim.tools',
)

def gallery_names() -> tuple[str, ...]:
    presets = json.loads((ROOT / 'src/manim_beanim/themes/presets.json').read_text())
    return tuple(f'Generic_Slide_Test_{name}.png' for name in sorted(presets))

def legacy_routes() -> tuple[str, ...]:
    return tuple(f'api/{name}.html' for name in LEGACY_MODULES)

def validate_sha(sha: str) -> str:
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        raise ValueError('Commit must be a lowercase 40-character Git SHA')
    return sha
