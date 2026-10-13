"""Validated, transactional theme application for future objects."""
from manim import Tex, MathTex, Text, TexFontTemplates, TexTemplate, ManimColor, config
from .models import Theme
from .presets import get_theme
from .provider import get_active_theme, set_active_theme
from .styles import normalize_style
from . import manim_defaults
_baseline = None

def validate_theme(theme: Theme) -> None:
    for color in (theme.background_color, theme.text_color):
        try:
            ManimColor(color)
        except (TypeError, ValueError) as error:
            raise ValueError(f'Invalid theme color: {color!r}') from error
    if not isinstance(getattr(TexFontTemplates, theme.tex_font, None), TexTemplate):
        raise ValueError(f'Unknown TeX font preset: {theme.tex_font}')
    for role, style in theme.styles.items():
        normalize_style(style, role=role)

class _CameraState:
    """Restore Cairo buffers in place, retaining references held by Cairo contexts."""
    def __init__(self, camera):
        self.camera = camera
        self.values = {name: getattr(camera, name) for name in
            ('_background_color', '_background_opacity', 'background', 'pixel_array',
             'pixel_array_to_cairo_context') if hasattr(camera, name)}
        self.arrays = {name: value.copy() for name, value in self.values.items()
                       if name in {'background', 'pixel_array'}}
        self.contexts = dict(self.values.get('pixel_array_to_cairo_context', {}))

    def restore(self) -> None:
        for name, value in self.values.items():
            if name in self.arrays:
                value[...] = self.arrays[name]
            if name == 'pixel_array_to_cairo_context':
                value.clear()
                value.update(self.contexts)
            setattr(self.camera, name, value)

def _set_background(camera, color: str) -> None:
    camera.background_color = ManimColor(color)
    if hasattr(camera, 'reset'):
        camera.reset()

def apply_theme(name_or_theme: str | Theme, *, scene=None) -> Theme:
    """Style future Beanim/Manim text; explicit constructor options override theme.

    Existing objects retain their appearance. Optional scene receives new camera
    background. Invalid themes leave defaults, active theme and camera unchanged.
    """
    global _baseline
    theme = get_theme(name_or_theme)
    validate_theme(theme)
    template = getattr(TexFontTemplates, theme.tex_font).copy()
    before = manim_defaults.snapshot()
    baseline = _baseline if _baseline is not None else before
    background = config.background_color
    active = get_active_theme()
    camera = scene.camera if scene is not None else None
    camera_state = _CameraState(camera) if camera is not None else None
    try:
        manim_defaults.restore(baseline)
        Tex.set_default(tex_template=template.copy(), color=theme.text_color, font_size=theme.text_size)
        MathTex.set_default(tex_template=template.copy(), color=theme.text_color, font_size=theme.text_size)
        text = {'color': theme.text_color, 'font_size': theme.text_size}
        if theme.text_font:
            text['font'] = theme.text_font
        Text.set_default(**text)
        config.background_color = theme.background_color
        if camera is not None:
            _set_background(camera, theme.background_color)
        set_active_theme(theme)
    except Exception:
        manim_defaults.restore(before)
        config.background_color = background
        set_active_theme(active)
        if camera_state is not None:
            camera_state.restore()
        raise
    if _baseline is None:
        _baseline = before
    return theme
