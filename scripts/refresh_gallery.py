"""Refresh curated gallery using the unchanged multi-template example."""
import subprocess
import sys
import tempfile
from pathlib import Path

from docs_support import ROOT, gallery_names


def main() -> None:
    import av
    with tempfile.TemporaryDirectory(prefix='beanim-gallery-') as folder:
        media = Path(folder)
        subprocess.run([
            sys.executable, '-m', 'manim', 'render', '-ql', '--fps', '5',
            '--disable_caching', '--format', 'mp4', '--media_dir', str(media),
            str(ROOT / 'examples/example_multi_template.py'), 'Multi_Template',
        ], cwd=ROOT, check=True)
        videos = list(media.rglob('Multi_Template.mp4'))
        if len(videos) != 1:
            raise ValueError('Expected one multi-template video')
        names = gallery_names()
        output = ROOT / 'docs/_static/media/images'
        with av.open(str(videos[0])) as video:
            stream = video.streams.video[0]
            if video.duration is None:
                raise ValueError('Rendered video has no duration')
            duration = video.duration / av.time_base
            captures = [(index + 0.5) * duration / len(names) for index in range(len(names))]
            captured = []
            for frame in video.decode(stream):
                if frame.time is not None and len(captured) < len(names) and frame.time >= captures[len(captured)]:
                    destination = media / names[len(captured)]
                    frame.to_image().save(destination)
                    captured.append(destination)
            if len(captured) != len(names):
                raise ValueError('Could not extract all template previews')
        output.mkdir(parents=True, exist_ok=True)
        for image in captured:
            (output / image.name).write_bytes(image.read_bytes())
        print(f'Refreshed {len(names)} gallery images; temporary renders removed')

if __name__ == '__main__':
    main()
