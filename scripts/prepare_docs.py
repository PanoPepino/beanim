"""Add legacy redirects and deployment identity to an already-built artifact."""
import argparse
import json
import os
from pathlib import Path

from docs_support import gallery_names, legacy_routes, validate_sha

def prepare(root: Path, sha: str, repository: str) -> None:
    validate_sha(sha)
    if not (root / 'api.html').is_file():
        raise ValueError('Build Sphinx documentation before preparing artifact')
    for route in legacy_routes():
        output = root / route
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta http-equiv="refresh" content="0; url=../api.html">'
            '<title>Beanim API moved</title></head><body>'
            '<a href="../api.html">Beanim API reference</a></body></html>\n',
            encoding='utf-8',
        )
    (root / 'build-info.json').write_text(json.dumps({
        'commit': sha, 'repository': repository, 'gallery': list(gallery_names()),
    }, indent=2) + '\n', encoding='utf-8')

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact', type=Path)
    parser.add_argument('--sha', required=True)
    parser.add_argument('--repository', default=os.environ.get('GITHUB_REPOSITORY', 'PanoPepino/beanim'))
    args = parser.parse_args()
    prepare(args.artifact, args.sha, args.repository)

if __name__ == '__main__':
    main()
