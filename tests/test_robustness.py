"""Edge cases missed by happy-path rendering examples."""
from copy import deepcopy
from dataclasses import replace
import pickle
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from manim import Annulus, Circle, ImageMobject, PI, Rectangle, Scene, Succession, VMobject, config, tempconfig
import manim_beanim as b
from manim_beanim.rendering.images import clip_image_to_mobject
from manim_beanim.themes.provider import get_active_theme
from manim_beanim.data.dictionaries import read_dictionary, _read_builtin

ROOT = Path(__file__).resolve().parents[1]

class RobustnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory(prefix='beanim-robustness-')
        cls.config = tempconfig({'media_dir': cls.folder.name, 'tex_dir': cls.folder.name + '/Tex',
            'pixel_width': 160, 'pixel_height': 90, 'verbosity': 'ERROR'})
        cls.config.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.config.__exit__(None, None, None)
        cls.folder.cleanup()

    def setUp(self):
        b.apply_theme('default_template')

    def test_rebuild_replaces_owned_children_and_preserves_external_children_and_position(self):
        for obj in (b.Equation(content='x=1'), b.Reference(content='Citation'), b.Table(content=[['1','2']])):
            extra = Circle(radius=.1)
            obj.add(extra)
            obj.shift([2, 1, 0])
            previous = obj.chosen_content
            center = obj.get_center().copy()
            count = len(obj.submobjects)
            for _ in range(3):
                obj.handle_no_dictionary()
                self.assertEqual(len(obj.submobjects), count)
                self.assertIn(extra, obj.submobjects)
            self.assertNotIn(previous, obj.submobjects)
            np.testing.assert_allclose(obj.get_center(), center)

    def test_failed_rebuild_keeps_visible_content_and_table_rows(self):
        obj = b.Equation(content='x=1')
        content, children = obj.chosen_content, obj.submobjects.copy()
        with patch('manim_beanim.components.base.render_text', side_effect=RuntimeError('TeX failed')):
            with self.assertRaisesRegex(RuntimeError, 'TeX failed'):
                obj.handle_no_dictionary()
        self.assertIs(obj.chosen_content, content)
        self.assertEqual(obj.submobjects, children)
        table = b.Table(content='key', dictionary={'key':[['1']]})
        rows, old = table._rows, table.chosen_content
        table.dictionary['key'] = [['1'], ['2','3']]
        with self.assertRaises(ValueError):
            table.handle_with_dictionary()
        self.assertEqual(table._rows, rows)
        self.assertIs(table.chosen_content, old)

    def test_dictionary_mapping_is_owned_and_missing_key_is_contextual(self):
        source = {'key':'x=1'}
        obj = b.Equation(content='key', dictionary=source)
        source['key'] = 'x=2'
        self.assertEqual(obj.dictionary['key'], 'x=1')
        with self.assertRaisesRegex(KeyError, 'Missing dictionary key: missing'):
            b.Text_General().get_tex_from_dict('missing', {})

    def test_bullets_queue_discard_duration_and_end_state(self):
        for size in (1, 3):
            obj = b.BlB(content=[f'Bullet {n}' for n in range(size)])
            obj.next_point()  # discarded animation
            self.assertEqual(obj.count, 0)
            steps = [obj.next_point(rt=3) for _ in range(size + 2)]
            self.assertEqual(obj.count, 0)
            self.assertTrue(all(step.run_time == 3 for step in steps))
            scene = Scene()
            succession = Succession(*steps)
            succession._setup_scene(scene)
            succession.begin()
            succession.finish()
            self.assertEqual(obj.count, size + 1)
            for point in obj.order_list:
                for glyph in point.family_members_with_points():
                    self.assertAlmostEqual(glyph.get_fill_opacity(), 1)
            for value in (-1, 0, float('nan'), True, '1'):
                with self.assertRaises(ValueError):
                    obj.next_point(rt=value)
            with self.assertRaises(ValueError):
                obj.next_point(rf=2)

    def test_bullets_counter_commits_at_finish_only_once(self):
        obj = b.BlB(content=['One','Two'])
        anim = obj.next_point()
        anim._setup_scene(Scene())
        anim.begin()
        self.assertEqual(obj.count, 0)
        anim.finish()
        anim.finish()
        self.assertEqual(obj.count, 1)
        for index, opacity in ((0,1),(1,.2)):
            for glyph in obj.order_list[index].family_members_with_points():
                self.assertAlmostEqual(glyph.get_fill_opacity(), opacity)

    def test_invalid_style_inputs_fail_early(self):
        invalid = [dict(dot_scale=0), dict(corner_rad=-.1), dict(corner_rad_direction=[1,1]),
            dict(corner_rad_direction=[1,1,-1,0]), dict(decorator_stroke_width=float('nan')),
            dict(decorator_presence='typo'), dict(direction=[0,0,0]), dict(text_size=True)]
        for kwargs in invalid:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                b.Text_General(**kwargs)

    def test_theme_validation_precedes_mutation(self):
        before = get_active_theme()
        background = str(config.background_color)
        for styles in ({'text':{'direction':(1,2)}}, {'typo':{}}, {'text':{'text_sze':25}},
                       {'table':{'highlight_top':1}}, {'text':{'corner_rad':-.1}}):
            theme = replace(b.get_theme('blue_ice'), styles=styles)
            with self.subTest(styles=styles), self.assertRaises(ValueError):
                b.apply_theme(theme)
            self.assertIs(get_active_theme(), before)
            self.assertEqual(str(config.background_color), background)
        with self.assertRaises(ValueError):
            replace(before, text_font=[])
        with self.assertRaises(ValueError):
            b.apply_theme(replace(before, tex_font='__dict__'))

    def test_camera_failure_restores_buffers_and_references(self):
        scene = Scene()
        camera = scene.camera
        pixels = camera.pixel_array
        background = camera.background
        old_pixels, old_background = pixels.copy(), background.copy()
        color = str(camera.background_color)
        def fail():
            pixels[:] = 17
            background[:] = 29
            camera.pixel_array_to_cairo_context.clear()
            raise RuntimeError('camera reset failed')
        with patch.object(camera, 'reset', side_effect=fail), self.assertRaises(RuntimeError):
            b.apply_theme('blue_ice', scene=scene)
        self.assertIs(camera.pixel_array, pixels)
        self.assertIs(camera.background, background)
        np.testing.assert_array_equal(pixels, old_pixels)
        np.testing.assert_array_equal(background, old_background)
        self.assertEqual(str(camera.background_color), color)
        self.assertEqual(get_active_theme().name, 'default_template')

    def test_style_snapshot_properties_copy_and_pickle(self):
        obj = b.Equation(content='x=1')
        with self.assertRaises(TypeError):
            obj.style['text_size'] = 10
        obj.text_size = 20
        self.assertEqual(obj.style['text_size'], 20)
        obj.crad = .3
        obj.corner_rad_direction = (1,0,1,0)
        self.assertEqual(obj.corner_rad, [.3,0,.3,0])
        snapshot = obj.style
        with self.assertRaises(ValueError):
            obj.text_size = -2
        self.assertIs(obj.style, snapshot)
        copy = deepcopy(obj)
        copy.text_size = 30
        self.assertEqual(obj.text_size, 20)
        restored = pickle.loads(pickle.dumps(obj))
        self.assertEqual(dict(restored.style), dict(obj.style))
        self.assertEqual(restored.theme.name, obj.theme.name)

    def test_copied_bullets_keep_independent_playback_state(self):
        original = b.BlB(content=['One','Two'])
        copied = original.copy()
        step = copied.next_point()
        step._setup_scene(Scene())
        step.begin()
        step.finish()
        self.assertEqual(original.count, 0)
        self.assertEqual(copied.count, 1)
        for glyph in original.order_list[1].family_members_with_points():
            self.assertAlmostEqual(glyph.get_fill_opacity(), 1)

    def test_table_flags_rows_and_repeated_highlights(self):
        for value, expected in ((True, True), (False, False), ('yes', True), ('no', False), (np.bool_(True),True)):
            table = b.Table(content=[['1','2']], highlight_top=value)
            self.assertIs(table.highlight_top, expected)
            row = table.filter_type()
            row.append('extra')
            self.assertEqual(len(table.filter_type()), 2)
            count = len(table.chosen_content.submobjects)
            if expected:
                table.add_highlight_top_row()
                self.assertEqual(len(table.chosen_content.submobjects), count)
        for value in (1, 0, 'true', None):
            if value is not None:
                with self.assertRaises(ValueError):
                    b.Table(content=[['1']],highlight_top=value)
        for cell in (float('nan'), float('inf'), True, {}):
            with self.assertRaises(ValueError):
                b.Table(content=[[cell]])

    def test_layout_bounds_and_title_font_size(self):
        small = b.Title_Presentation(content=['Short'], text_size=20)
        large = b.Title_Presentation(content=['Short'], text_size=40)
        self.assertAlmostEqual(small.text_group[0].font_size, 40)
        self.assertAlmostEqual(large.text_group[0].font_size, 80)
        self.assertLess(small.text_group.width, large.text_group.width)
        section = b.Title_Section(content='Long section '*20)
        self.assertLessEqual(section.title.width + 2*section.tightness, config.frame_width)
        title = b.Title_Presentation(content=['Long heading '*10]*8)
        self.assertLessEqual(title.text_group.height + 2*title.tightness, config.frame_height)
        note = b.Post_It(to_dos=['Long task '*15]*10)
        paper, tasks, _ = note.post_it
        self.assertLess(tasks.width, paper.width)
        self.assertLess(tasks.height, paper.height)
        for cls, args in ((b.Title_Presentation, {'content':['Title']}), (b.Title_Section,{'content':'Title'}),
                          (b.Post_It, {'to_dos':['Task']})):
            with self.assertRaises(ValueError):
                cls(max_width=-1, **args)

    def test_builtin_dictionary_cache_remains_independent(self):
        _read_builtin.cache_clear()
        first = read_dictionary('data_base','equations')
        first.clear()
        self.assertTrue(read_dictionary('data_base','equations'))
        self.assertEqual(_read_builtin.cache_info().hits, 1)

    @staticmethod
    def image(alpha=255):
        array = np.full((200,300,4),255,dtype=np.uint8)
        array[:,:,0] = np.linspace(0,255,300,dtype=np.uint8)
        array[:,:,3] = alpha
        return ImageMobject(array).stretch_to_fit_width(3).stretch_to_fit_height(2)

    def test_clipping_rotated_texture_and_alpha(self):
        image = self.image(alpha=128).rotate(PI/4)
        mask = Rectangle(width=3,height=2).rotate(PI/4)
        clipped = clip_image_to_mobject(image,mask)
        np.testing.assert_allclose(clipped.points, image.points)
        np.testing.assert_array_equal(clipped.pixel_array, image.pixel_array)
        transparent = clip_image_to_mobject(self.image(alpha=128), Circle(radius=.6))
        self.assertEqual(int(transparent.pixel_array[:,:,3].max()),128)
        self.assertTrue(np.any((transparent.pixel_array[:,:,3]>0)&(transparent.pixel_array[:,:,3]<128)))

    def test_clipping_holes_disconnected_paths_and_failures(self):
        ring = clip_image_to_mobject(self.image(),Annulus(inner_radius=.4,outer_radius=.8))
        h,w = ring.pixel_array.shape[:2]
        self.assertEqual(int(ring.pixel_array[h//2,w//2,3]),0)
        shapes = VMobject().set_points(np.concatenate([Circle(radius=.25).shift([-.6,0,0]).points,
                                                      Circle(radius=.25).shift([.6,0,0]).points]))
        clipped = clip_image_to_mobject(self.image(),shapes)
        h,w = clipped.pixel_array.shape[:2]
        self.assertTrue(np.all(clipped.pixel_array[:,w//2,3]==0))
        for mask in (VMobject(),Circle().shift([10,0,0]),Circle().shift([0,0,1])):
            with self.assertRaises(ValueError):
                clip_image_to_mobject(self.image(),mask)
        with self.assertRaises(ValueError):
            clip_image_to_mobject(self.image().stretch_to_fit_width(0),Circle())

if __name__ == '__main__':
    unittest.main()
