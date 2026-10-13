"""Functional regression tests for public classes, themes and safe data handling."""
import ast
from dataclasses import replace
import importlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from manim import Tex, MathTex, Text, Scene, MathTable, config, tempconfig, RED, RIGHT
import manim_beanim as b
from manim_beanim.data.dictionaries import read_dictionary
from manim_beanim.data.equations import parse_equations
from manim_beanim.themes.provider import get_active_theme

ROOT = Path(__file__).resolve().parents[1]

class FunctionalTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory(prefix='beanim-tests-')
        cls.root = Path(cls.folder.name)
        cls.config = tempconfig({'media_dir': str(cls.root), 'tex_dir': str(cls.root / 'Tex'), 'text_dir': str(cls.root / 'texts'), 'pixel_width': 160, 'pixel_height': 90, 'verbosity': 'ERROR'})
        cls.config.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.config.__exit__(None, None, None)
        cls.folder.cleanup()

    def setUp(self):
        b.apply_theme('default_template')

    def test_public_exports_and_legacy_paths(self):
        paths = {'Title_Section': 'text_and_organisation.title_section', 'Title_Presentation': 'text_and_organisation.title_presentation', 'BlB': 'text_and_organisation.blb', 'Reference': 'text_and_organisation.ref', 'Equation': 'text_and_organisation.equation', 'Text_General': 'text_and_organisation.text_general', 'Underbar': 'text_and_organisation.underbar', 'Photo': 'other_objects.photo', 'Post_It': 'other_objects.post_it', 'Table': 'graphing_objects.table_general'}
        for name, module in paths.items():
            self.assertIs(getattr(b, name), getattr(importlib.import_module('manim_beanim.' + module), name))

    def test_imports_have_no_wildcards_and_pure_tools_do_not_load_manim(self):
        for p in (ROOT / 'src').rglob('*.py'):
            for node in ast.walk(ast.parse(p.read_text())):
                if isinstance(node, ast.ImportFrom):
                    self.assertNotIn('*', [item.name for item in node.names], str(p))
        code = "import sys; from manim_beanim import extract_equations; assert 'manim' not in sys.modules; assert 'pybtex' not in sys.modules"
        result = subprocess.run([sys.executable, '-c', code], env={**__import__('os').environ, 'PYTHONPATH': str(ROOT / 'src')}, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_theme_switch_reapplies_and_keeps_existing_objects(self):
        b.apply_theme('blue_ice')
        first = b.Reference(content='First')
        color = first.chosen_content.get_color()
        b.apply_theme('green_mint')
        b.apply_theme('blue_ice')
        second = b.Reference(content='Second')
        self.assertEqual(str(config.background_color), '#F1F8FF')
        self.assertEqual(first.chosen_content.get_color(), color)
        self.assertEqual(second.text_color, '#003E7C')
        self.assertEqual(first.tex_template, first.tex_template)

    def test_all_presets_construct_all_components(self):
        for name in ('default_template', 'blue_ice', 'green_mint', 'red_autumn', 'beamer_blue', 'beamer_green', 'quantum_dusk', 'dark_energy'):
            with self.subTest(theme=name):
                b.import_template_beanim(name)
                objects = [b.Title_Presentation(content=['Title', 'Institution', 'Author']), b.Title_Section(content='Section'), b.BlB(content=['First', 'Second'], the_title='List'), b.Reference(content='Citation'), b.Equation(content='x=1'), b.Underbar(content=['Author', 'Talk']), b.Table(content=[['1', '2'], ['3', '4']]), b.Photo(str(ROOT / 'examples/figures/pedro.png'), decorator_style='polaroid', caption='Photo'), b.Photo(str(ROOT / 'examples/figures/pedro.png')), b.Post_It(to_dos=['Task'])]
                self.assertTrue(all((obj.width > 0 and obj.height > 0 for obj in objects)))
                if name.startswith('beamer_'):
                    colors = [str(item.get_color()) for item in objects[3].chosen_content.family_members_with_points()]
                    self.assertTrue(all((color != '#FFFFFF' for color in colors)))

    def test_theme_styles_manim_and_explicit_options_win(self):
        b.apply_theme('blue_ice')
        for cls in (Tex, MathTex, Text):
            obj = cls('Test')
            self.assertTrue(all((str(item.get_color()) == '#003E7C' for item in obj.family_members_with_points())))
            self.assertAlmostEqual(obj.font_size, 35)
        obj = b.Reference(content='Citation', text_size=22, text_color=RED)
        self.assertAlmostEqual(obj.chosen_content.font_size, 22)
        self.assertEqual(obj.chosen_content.get_color(), RED)

    def test_theme_background_inside_existing_scene(self):
        scene = Scene()
        b.apply_theme('green_mint', scene=scene)
        self.assertEqual(str(scene.camera.background_color), '#F2FFFB')

    def test_invalid_theme_keeps_current_state(self):
        b.apply_theme('green_mint')
        with self.assertRaises(ValueError):
            b.apply_theme('missing')
        with self.assertRaises(ValueError):
            b.apply_theme(replace(b.get_theme('blue_ice'), text_size=-1))
        self.assertEqual(get_active_theme().name, 'green_mint')
        self.assertEqual(str(config.background_color), '#F2FFFB')

    def test_application_rolls_back_if_camera_fails(self):
        b.apply_theme('green_mint')
        scene = Scene()
        with patch.object(scene.camera, 'init_background', side_effect=RuntimeError('camera')):
            with self.assertRaisesRegex(RuntimeError, 'camera'):
                b.apply_theme('blue_ice', scene=scene)
        self.assertEqual(get_active_theme().name, 'green_mint')
        self.assertEqual(str(Tex('After').get_color()), '#006661')

    def test_theme_configuration_and_vectors_are_independent(self):
        with self.assertRaises(TypeError):
            b.get_theme('blue_ice').styles['text']['text_color'] = 'bad'
        a = b.Text_General()
        other = b.Text_General()
        a.direction[0] = 99
        self.assertNotEqual(other.direction[0], 99)
        self.assertEqual(RIGHT[0], 1)

    def test_table_font_highlight_flags_and_input_shapes(self):
        with patch.object(MathTable, 'add_highlighted_cell', autospec=True) as highlight:
            small = b.Table(content=[['1', '2']], text_size=10, highlight_top='no')
            large = b.Table(content=[['1', '2']], text_size=60, highlight_top=False)
        highlight.assert_not_called()
        self.assertAlmostEqual(small.chosen_content.get_entries()[0].font_size, 10)
        self.assertAlmostEqual(large.chosen_content.get_entries()[0].font_size, 60)
        for rows in ([], [['1'], ['2', '3']], None):
            with self.assertRaises(ValueError):
                b.Table(content=rows)
        self.assertGreater(b.Table(content=[['1']]).width, 0)

    def test_dictionary_paths_mapping_and_single_read(self):
        f = self.root / 'tables.txt'
        f.write_text("{'key': [['1','2'],['3','4']]}")
        original = b.Table.load_dictionary
        calls = []

        def count(owner):
            calls.append(owner)
            return original(owner)
        with patch.object(b.Table, 'load_dictionary', count):
            table = b.Table(content='key', dictionary=f)
        self.assertEqual(len(calls), 1)
        self.assertGreater(table.width, 0)
        self.assertEqual(b.Table.split_dictionary_path(table, 'tables.txt'), ['', 'tables.txt'])
        self.assertGreater(b.Equation(content='key', dictionary={'key': 'x=1'}).width, 0)
        self.assertGreater(b.Reference(content='key', the_dictionary={'key': 'Citation'}).width, 0)
        with self.assertRaises(KeyError):
            b.Reference(content='missing', dictionary={'key': 'Citation'})
        for kind, key in [('equations', 'equation_data_base_1'), ('refs', 'ref_data_base_1'), ('tables', 'table_data_base_1')]:
            self.assertIn(key, read_dictionary('data_base', kind))

    def test_dictionary_exec_rejected_cache_invalidated_and_copies_independent(self):
        f = self.root / 'malicious.txt'
        f.write_text("__import__('os').getcwd()")
        with self.assertRaises(ValueError):
            read_dictionary(f)
        f.write_text("{'key': ['old']}")
        a = read_dictionary(f)
        a['key'].append('mutated')
        self.assertEqual(read_dictionary(f), {'key': ['old']})
        f.write_text("{'key': ['new-value']}")
        self.assertEqual(read_dictionary(f), {'key': ['new-value']})

    def test_extractors_roundtrip_quotes_commas_and_backslashes(self):
        f = self.root / 'input.tex'
        f.write_text("\\begin{equation}\\label{eq}f'(x,y)=\\frac{x}{y}\\tag{\\mathrm{A}}\\end{equation}")
        expected = {'eq': "f'(x,y)=\\frac{x}{y}"}
        self.assertEqual(parse_equations(f), expected)
        for ext in ('txt', 'json'):
            out = self.root / ('eq.' + ext)
            self.assertIsNone(b.extract_equations(f, out))
            self.assertEqual(read_dictionary(out), expected)
        f = self.root / 'refs.bib'
        f.write_text("@article{one,author={O'Neil, Jane},year={2025},title={Test}}")
        out = self.root / 'refs.txt'
        b.extract_citation(f, 'Other', 'O', out)
        self.assertEqual(read_dictionary(out), {'one': "[O'Neil, 2025]"})

    def test_empty_inputs_and_bad_photo_styles_fail_clearly(self):
        for cls, kwargs in ((b.Underbar, {'content': []}), (b.BlB, {'content': []}), (b.Post_It, {'to_dos': []}), (b.Title_Presentation, {'content': []}), (b.Equation, {'content': None})):
            with self.assertRaises(ValueError):
                cls(**kwargs)
        with self.assertRaises(ValueError):
            b.Photo('missing.png', decorator_style='invalid')

    def test_bullets_animations_have_valid_lifecycle(self):
        obj = b.BlB(content=['First', 'Second'])
        scene = Scene()
        for _ in range(4):
            animation = obj.next_point()
            animation._setup_scene(scene)
            animation.begin()
            animation.finish()

    def test_themed_mobjects_can_copy_and_animate(self):
        b.apply_theme('blue_ice')
        objects = [b.Reference(content='Reference'), b.Table(content=[['1']]),
                   b.Photo(str(ROOT / 'examples/figures/pedro.png')), b.Post_It(to_dos=['Task'])]
        for obj in objects:
            with self.subTest(component=type(obj).__name__):
                copy = obj.copy()
                self.assertIs(copy.theme, obj.theme)
                self.assertIsNot(copy.style, obj.style)
                animation = obj.animate.shift(RIGHT).build()
                scene = Scene()
                animation._setup_scene(scene)
                animation.begin()
                animation.finish()
if __name__ == '__main__':
    unittest.main()
