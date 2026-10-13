"""Documentation integrity, publication filtering, redirects and live identity."""
import io
from email.message import Message
import mimetypes
import json
from pathlib import Path
import sys
import tempfile
from urllib.error import HTTPError
from urllib.parse import urlsplit
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from docs_support import gallery_names, legacy_routes
from prepare_docs import prepare
from verify_docs import verify_artifact, verify_live, verify_live_once

ROOT = Path(__file__).resolve().parents[1]

SHA = 'a' * 40

class DocumentationTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory(prefix='beanim-docs-tests-')
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        (self.root / '_static/styles').mkdir(parents=True)
        (self.root / '_static/styles/furo.css').write_text('body {color: black;}')
        (self.root / '_static/styles/furo-extensions.css').write_text('code {color: black;}')
        (self.root / 'index.html').write_text('<link rel="stylesheet" href="_static/styles/furo.css"><a href="api.html">API</a>')
        (self.root / 'api.html').write_text('<div id="manim_beanim.apply_theme">apply_theme</div>')
        for page in ('installation.html','examples.html'):
            (self.root / page).write_text('<a href="index.html">Home</a>')
        (self.root / '.nojekyll').touch()
        gallery = self.root / '_static/media/images'
        gallery.mkdir(parents=True)
        for name in gallery_names():
            (gallery / name).write_bytes(b'\x89PNG\r\n\x1a\n')
        prepare(self.root, SHA, 'PanoPepino/beanim')

    def test_artifact_and_legacy_redirects(self):
        verify_artifact(self.root, SHA)
        self.assertEqual(len(legacy_routes()), 10)
        self.assertTrue(all((self.root / route).is_file() for route in legacy_routes()))
        info = json.loads((self.root / 'build-info.json').read_text())
        self.assertEqual(info['commit'], SHA)

    def test_reject_missing_assets_and_empty_styles(self):
        path = self.root / '_static/styles/furo.css'
        path.write_text('')
        with self.assertRaisesRegex(ValueError, 'Empty Furo'):
            verify_artifact(self.root, SHA)
        path.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing documentation file'):
            verify_artifact(self.root, SHA)

    def test_reject_generated_cache_and_unapproved_media(self):
        for filename in ('_static/media/Tex/cache.svg','_static/media/videos/movie.mp4','_static/media/images/extra.png'):
            file = self.root / filename
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_bytes(b'generated')
            with self.subTest(filename=filename), self.assertRaises(ValueError):
                verify_artifact(self.root, SHA)
            file.unlink()
            if file.parent.name in {'Tex','videos'}:
                file.parent.rmdir()

    def test_reject_broken_links_wrong_commit_and_missing_api(self):
        (self.root / 'examples.html').write_text('<img src="_static/missing.png">')
        with self.assertRaisesRegex(ValueError, 'Missing local asset'):
            verify_artifact(self.root, SHA)
        (self.root / 'examples.html').write_text('<p>Examples</p>')
        with self.assertRaisesRegex(ValueError, 'commit does not match'):
            verify_artifact(self.root, 'b' * 40)
        (self.root / 'api.html').write_text('<p>Old API</p>')
        with self.assertRaisesRegex(ValueError, 'apply_theme API entry'):
            verify_artifact(self.root, SHA)

    def test_css_asset_paths_are_verified(self):
        (self.root / '_static/styles/furo.css').write_text('body {background:url("missing.svg")}')
        with self.assertRaisesRegex(ValueError, 'Missing local asset'):
            verify_artifact(self.root, SHA)

    def test_live_check_accepts_http_responses_and_rejects_stale_release(self):
        def response(request, timeout):
            self.assertEqual(timeout, 10)
            self.assertEqual(request.get_header('Cache-control'), 'no-cache')
            parsed = urlsplit(request.full_url)
            self.assertIn('commit=', parsed.query)
            file = self.root / parsed.path.removeprefix('/beanim/')
            if not file.is_file():
                raise HTTPError(request.full_url, 404, 'Not found', {}, None)
            result = io.BytesIO(file.read_bytes())
            result.headers = Message()
            result.headers['Content-Type'] = mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
            return result
        with patch('verify_docs.urlopen', side_effect=response):
            base = 'https://example.com/beanim/'
            verify_live_once(base, SHA)
            with self.assertRaisesRegex(ValueError, 'commit does not match'):
                verify_live_once(base, 'b' * 40)
            (self.root / '_static/styles/furo.css').write_text('')
            with self.assertRaisesRegex(ValueError, 'stylesheet unavailable'):
                verify_live_once(base, SHA)

    def test_retries_are_bounded(self):
        with patch('verify_docs.verify_live_once', side_effect=[ValueError('stale'),None]) as check:
            verify_live('https://example.com/', SHA, attempts=2, delay=0)
            self.assertEqual(check.call_count,2)
        with patch('verify_docs.verify_live_once', side_effect=ValueError('stale')) as check:
            with self.assertRaisesRegex(ValueError, 'stale'):
                verify_live('https://example.com/', SHA, attempts=2, delay=0)
            self.assertEqual(check.call_count,2)

if __name__ == '__main__':
    unittest.main()
