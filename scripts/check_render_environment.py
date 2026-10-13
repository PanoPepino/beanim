"""Compile every theme in a fresh directory; retain TeX logs for CI diagnosis."""
import argparse
from importlib.metadata import version
from pathlib import Path
import shutil
import subprocess
import tempfile


def check_prerequisites():
    """Fail before rendering when executable or Greek font resources are absent."""
    for executable in ('latex', 'dvisvgm', 'kpsewhich'):
        if shutil.which(executable) is None:
            raise RuntimeError(f'Missing {executable}; install Manim rendering prerequisites.')
    for resource in ('lgrenc.def', 'lgrcmr.fd', 'lgrlmtt.fd'):
        result = subprocess.run(['kpsewhich', resource], capture_output=True, text=True,
                                check=False, timeout=15)
        if result.returncode or not result.stdout.strip():
            raise RuntimeError(f'Missing {resource}; on Ubuntu install texlive-lang-greek.')


def verify_rendering(output):
    """Exercise real text, Greek math and geometry operations across all presets."""
    from manim import Cutout, MathTex, Rectangle, Tex, tempconfig
    from manim_beanim import apply_theme
    from manim_beanim.themes.presets import THEMES

    print(f'Manim {version("manim")}; NumPy {version("numpy")}', flush=True)
    with tempconfig({'media_dir': str(output), 'tex_dir': str(output / 'Tex')}):
        # Old Manim calls numpy.trapz here, which NumPy 2.4 removed.
        Cutout(Rectangle(width=3, height=2), Rectangle(width=1, height=1))
        for name in sorted(THEMES):
            apply_theme(name)
            Tex('Theme preflight')
            MathTex(r'\alpha + \beta = \varepsilon')
            print(f'Render prerequisites OK: {name}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(tempfile.gettempdir()))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    # A unique directory prevents a cached SVG from hiding a broken LaTeX setup.
    output = Path(tempfile.mkdtemp(prefix='beanim-preflight-', dir=args.output))
    try:
        check_prerequisites()
        verify_rendering(output)
    except Exception:
        print(f'Render preflight failed. Diagnostic files: {output}', flush=True)
        raise
    else:
        shutil.rmtree(output)


if __name__ == '__main__':
    main()
