"""Verify Sphinx/Furo artifact or live Pages site, including deployed commit."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.parse import unquote, urljoin, urlsplit
from urllib.request import Request, urlopen

from docs_support import gallery_names, legacy_routes, validate_sha

REQUIRED = ('index.html', 'api.html', 'installation.html', 'examples.html', '.nojekyll',
            'build-info.json', '_static/styles/furo.css', '_static/styles/furo-extensions.css')
API_MARKER = 'manim_beanim.apply_theme'

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.styles = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get('id'):
            self.ids.add(attributes['id'])
        for field in ('href', 'src'):
            if attributes.get(field):
                self.links.append(attributes[field])
        if tag == 'link' and attributes.get('rel') == 'stylesheet':
            self.styles.append(attributes.get('href', ''))


def check_info(data: dict, sha: str) -> None:
    if not isinstance(data, dict) or data.get('commit') != validate_sha(sha):
        raise ValueError(f'Documentation commit does not match {sha}')
    if data.get('gallery') != list(gallery_names()):
        raise ValueError('Documentation gallery manifest differs from package presets')


def check_local_link(root: Path, source: Path, link: str) -> None:
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return
    relative = unquote(parsed.path)
    if relative.startswith('/'):
        if not relative.startswith('/beanim/'):
            raise ValueError(f'Unexpected absolute site path: {link}')
        target = root / relative.removeprefix('/beanim/')
    else:
        target = source.parent / relative
    target = target.resolve()
    if not target.is_relative_to(root):
        raise ValueError(f'Link escapes artifact: {source.name}: {link}')
    if target.is_dir():
        target /= 'index.html'
    if not target.is_file():
        raise ValueError(f'Missing local asset: {source.relative_to(root)}: {link}')


def verify_artifact(root: Path, sha: str) -> None:
    root = root.resolve()
    for name in (*REQUIRED, *legacy_routes()):
        if not (root / name).is_file():
            raise ValueError(f'Missing documentation file: {name}')
    check_info(json.loads((root / 'build-info.json').read_text()), sha)
    for css in ('_static/styles/furo.css', '_static/styles/furo-extensions.css'):
        if not (root / css).read_text().strip():
            raise ValueError(f'Empty Furo stylesheet: {css}')
    gallery = root / '_static/media/images'
    actual = {p.name for p in gallery.iterdir() if p.is_file()}
    if actual != set(gallery_names()):
        raise ValueError(f'Gallery files differ: {actual.symmetric_difference(gallery_names())}')
    for name in gallery_names():
        if not (gallery / name).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError(f'Invalid gallery image: {name}')
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Pages artifact contains symlink: {path}')
        relative = path.relative_to(root)
        if set(relative.parts) & {'Tex', 'texts', '__pycache__', 'partial_movie_files', '.doctrees'}:
            raise ValueError(f'Generated cache entered artifact: {relative}')
        if path.suffix.lower() in {'.mp4', '.mov', '.webm', '.pyc', '.pyo', '.doctree', '.pickle', '.tex'}:
            raise ValueError(f'Unapproved generated media: {relative}')
        if not path.is_file():
            continue
        if path.suffix == '.html':
            parser = Links()
            parser.feed(path.read_text(encoding='utf-8'))
            for link in parser.links:
                check_local_link(root, path, link)
        elif path.suffix == '.css':
            for url in re.findall(r'url\(([^)]+)\)', path.read_text(encoding='utf-8')):
                check_local_link(root, path, url.strip(' \t\r\n\'"'))
    parser = Links()
    parser.feed((root / 'api.html').read_text())
    if API_MARKER not in parser.ids:
        raise ValueError('New apply_theme API entry is missing')
    parser = Links()
    parser.feed((root / 'index.html').read_text())
    if not any('furo.css' in link for link in parser.styles):
        raise ValueError('Homepage does not load Furo stylesheet')
    for route in legacy_routes():
        content = (root / route).read_text()
        if 'url=../api.html' not in content:
            raise ValueError(f'Invalid legacy redirect: {route}')


def fetch(base: str, path: str, sha: str) -> tuple[bytes, str]:
    url = urljoin(base.rstrip('/') + '/', path)
    url += f'?commit={sha}&verify={time.time_ns()}'
    request = Request(url, headers={'Cache-Control': 'no-cache', 'User-Agent': 'Beanim-Pages-verify'})
    with urlopen(request, timeout=10) as response:
        return response.read(), response.headers.get_content_type()


def verify_live_once(base: str, sha: str) -> None:
    parsed = urlsplit(base)
    if parsed.scheme not in {'http', 'https'} or not parsed.netloc:
        raise ValueError('Live URL must be an HTTP(S) site URL')
    data, _ = fetch(base, 'build-info.json', sha)
    check_info(json.loads(data), sha)
    for page in ('index.html', 'api.html', 'installation.html', 'examples.html'):
        data, mime = fetch(base, page, sha)
        if mime != 'text/html':
            raise ValueError(f'Unexpected HTML content type: {page}: {mime}')
        parser = Links()
        parser.feed(data.decode('utf-8'))
        if page == 'api.html' and API_MARKER not in parser.ids:
            raise ValueError('Live apply_theme API entry is missing')
        if page == 'index.html' and not any('furo.css' in link for link in parser.styles):
            raise ValueError('Live homepage does not load Furo stylesheet')
    for css in ('_static/styles/furo.css', '_static/styles/furo-extensions.css'):
        data, mime = fetch(base, css, sha)
        if not data.strip() or mime != 'text/css':
            raise ValueError(f'Live stylesheet unavailable: {css}: {mime}')
    for name in gallery_names():
        data, mime = fetch(base, '_static/media/images/' + name, sha)
        if mime != 'image/png' or not data.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError(f'Live gallery image unavailable: {name}')
    for route in legacy_routes():
        data, _ = fetch(base, route, sha)
        if b'url=../api.html' not in data:
            raise ValueError(f'Live legacy redirect unavailable: {route}')


def verify_live(base: str, sha: str, *, attempts: int = 6, delay: float = 5) -> None:
    validate_sha(sha)
    if attempts < 1 or delay < 0:
        raise ValueError('Retry attempts must be positive and delay nonnegative')
    for attempt in range(attempts):
        try:
            verify_live_once(base, sha)
            return
        except (OSError, ValueError) as error:
            print(f'Live verification {attempt + 1}/{attempts}: {error}', flush=True)
            if attempt + 1 == attempts:
                raise
            time.sleep(delay)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--artifact', type=Path)
    mode.add_argument('--url')
    parser.add_argument('--sha', required=True)
    args = parser.parse_args()
    if args.artifact:
        verify_artifact(args.artifact, args.sha)
    else:
        verify_live(args.url, args.sha)
    print('Documentation verification passed')

if __name__ == '__main__':
    main()
