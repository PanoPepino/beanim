"""Text validation and rendering independent of concrete components."""
from manim import Mobject, Tex, MathTex, TexFontTemplates
from ..themes.styles import normalize_style, finite_number

def template_for(theme):
    return getattr(TexFontTemplates, theme.tex_font).copy() if theme else None

def text_pieces(content) -> list[str]:
    pieces = list(content) if isinstance(content, (list, tuple)) else [content]
    if not pieces or not all((isinstance(piece, str) and piece.strip() for piece in pieces)):
        raise ValueError('Content must be a nonempty string or sequence of nonempty strings')
    return pieces

def validate_style(values, *, role=None) -> None:
    normalize_style(values, role=role)

def render_text(content: str, owner, *, math: bool = False, size: float | None = None) -> Mobject:
    text_pieces(content)
    font_size = owner.text_size if size is None else finite_number(size, 'text_size', positive=True)
    kwargs = {'font_size': font_size, 'color': owner.text_color}
    if owner.tex_template is not None:
        kwargs['tex_template'] = owner.tex_template.copy()
    return (MathTex if math else Tex)(content, **kwargs)
