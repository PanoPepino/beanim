from ...my_imports import *
from ...other_objects import *
from ...graphing_objects import *
from ...text_and_organisation import *

# DARK ENERGY TEMPLATE
# Dark backgrounds with vibrant energy-themed accents for modern cosmology presentations

dark_energy = {
    "tex_temp": TexFontTemplates.latin_modern_tw,
    "bg_color": "#0D1B2A",  # Deep space blue-black background
    "text_size": 35,
    "text_color": "#E0E1DD",  # Light gray for text
    "decorator_presence_1": "box",
    "decorator_presence_2": "box_long_left",
    "decorator_presence_3": "no",
    "decorator_color": "#00D9FF",  # Bright cyan (primary decorator)
    "decorator_color_2": "#00FFC6",  # Bright teal (secondary)
    "decorator_color_3": "#1B263B",  # Space blue (accent)
    "decorator_color_4": "#E0E1DD",  # Light gray (lightest accent)
    "decorator_stroke_width": 1,
    "corner_rad": 0.05,
    "corner_rad_direction": [1, 1, 1, 1],
    "fill_opa": 0.05,
    "tightness": 0.2,
    "h_tightness": 0.5,
    "v_tightness": 0.5,
    "stroke_opa": 1,
    "dot_scale": 1.5,
    "direction": RIGHT,
    "aligned_direction_1": LEFT,
    "aligned_direction_2": [0, 0, 0],
    "decorator_style": "techno",
}


# Definition of Tex defaults. This will change font and its color.
# Careful! It seems that there exist some FontTemplates which do not automatically scale the parenthesis. This drove me crazy for some hours. Be aware of what font you choose.

config.background_color = dark_energy['bg_color']
Tex.set_default(tex_template=dark_energy['tex_temp'])
MathTex.set_default(tex_template=dark_energy['tex_temp'])


# Definition of the attributes of each Class

Text_General.set_default(  # Be careful with general size
    text_size=dark_energy['text_size'],
    text_color=dark_energy['text_color'],
    decorator_presence=dark_energy['decorator_presence_1'],
    decorator_color=dark_energy['decorator_color'],
    decorator_stroke_width=dark_energy['decorator_stroke_width'],
    corner_rad=dark_energy['corner_rad'],
    corner_rad_direction=dark_energy['corner_rad_direction'],
    fill_opa=dark_energy['fill_opa'],
    tightness=dark_energy['tightness'],
    stroke_opa=dark_energy['stroke_opa'],
    dot_scale=dark_energy['dot_scale'],
    direction=dark_energy['direction'],
    aligned_direction=dark_energy['aligned_direction_1']
)

Title_Presentation.set_default(
    decorator_presence=dark_energy['decorator_presence_2'],
    tightness=3*dark_energy['tightness']
)

Title_Section.set_default(
    decorator_presence=dark_energy['decorator_presence_2'],
    tightness=1.3*dark_energy['tightness']
)

BlB.set_default()

Reference.set_default(
    text_size=0.5 * dark_energy['text_size'],
    decorator_presence=dark_energy['decorator_presence_3'],
    aligned_direction=dark_energy['aligned_direction_2']
)
# Any equation
Equation.set_default(
    aligned_direction=dark_energy['aligned_direction_1']
)

# Underbar
Underbar.set_default(
)

# Any Table
Table.set_default(
    highlight_top="yes",
    text_size=dark_energy['text_size'],
    text_color=dark_energy['text_color'],
    decorator_presence=dark_energy['decorator_presence_1'],
    decorator_color=dark_energy['decorator_color'],
    decorator_color_2=dark_energy['decorator_color_2'],
    decorator_color_3=dark_energy['decorator_color_3'],
    decorator_color_4=dark_energy['decorator_color_4'],
    decorator_stroke_width=dark_energy['decorator_stroke_width'],
    corner_rad=dark_energy['corner_rad'],
    corner_rad_direction=dark_energy['corner_rad_direction'],
    fill_opa=dark_energy['fill_opa'],
    h_tightness=dark_energy['h_tightness'],
    v_tightness=dark_energy['v_tightness'],
    tightness=0,  # So the border of the table is the box without any extra space.
    stroke_opa=dark_energy['stroke_opa']
)

Underbar.set_default(
  
)


# Photo Frame
Photo.set_default(
    decorator_style=dark_energy['decorator_style'],
    decorator_color=dark_energy['decorator_color'],
    text_size=0.75 * dark_energy['text_size'],
    text_color=dark_energy['text_size'],
    pin_color=dark_energy['text_color'],
    corner_rad=dark_energy['corner_rad'],
    decorator_stroke_w=dark_energy['decorator_stroke_width']
)

# Post-it
Post_It.set_default(
    text_color=dark_energy['text_color'],
    text_size=dark_energy['text_size'],
    pin_color=dark_energy['text_color']
)
