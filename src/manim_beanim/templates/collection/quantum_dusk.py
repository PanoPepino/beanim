from ...my_imports import *
from ...other_objects import *
from ...graphing_objects import *
from ...text_and_organisation import *

# QUANTUM DUSK TEMPLATE
# Deep purples and blues representing quantum phenomena and twilight string landscapes

quantum_dusk = {
    "tex_temp": TexFontTemplates.biolinum,
    "bg_color": "#F1EFF7",  # Light lavender background
    "text_size": 35,
    "text_color": "#1A1033",  # Deep purple-black for text
    "decorator_presence_1": "box",
    "decorator_presence_2": "back_frame",
    "decorator_presence_3": "no",
    "decorator_color": "#6B4C9A",  # Royal purple (primary decorator)
    "decorator_color_2": "#2A1F5C",  # Deep space purple
    "decorator_color_3": "#8B72C2",  # Medium purple
    "decorator_color_4": "#F0EDF5",  # Light lavender accent
    "decorator_stroke_width": 1,
    "corner_rad": 0,
    "corner_rad_direction": [1, 1, 0, 0],
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

config.background_color = quantum_dusk['bg_color']
Tex.set_default(tex_template=quantum_dusk['tex_temp'])
MathTex.set_default(tex_template=quantum_dusk['tex_temp'])


# Definition of the attributes of each Class

Text_General.set_default(  # Be careful with general size
    text_size=quantum_dusk['text_size'],
    text_color=quantum_dusk['text_color'],
    decorator_presence=quantum_dusk['decorator_presence_1'],
    decorator_color=quantum_dusk['decorator_color'],
    decorator_stroke_width=quantum_dusk['decorator_stroke_width'],
    corner_rad=quantum_dusk['corner_rad'],
    corner_rad_direction=quantum_dusk['corner_rad_direction'],
    fill_opa=quantum_dusk['fill_opa'],
    tightness=quantum_dusk['tightness'],
    stroke_opa=quantum_dusk['stroke_opa'],
    dot_scale=quantum_dusk['dot_scale'],
    direction=quantum_dusk['direction'],
    aligned_direction=quantum_dusk['aligned_direction_1']
)

Title_Presentation.set_default(
    decorator_presence=quantum_dusk['decorator_presence_2'],
    tightness=3*quantum_dusk['tightness']
)

Title_Section.set_default(
    decorator_presence=quantum_dusk['decorator_presence_2'],
    tightness=1.3*quantum_dusk['tightness']
)

BlB.set_default()

Reference.set_default(
    text_size=0.5 * quantum_dusk['text_size'],
    decorator_presence=quantum_dusk['decorator_presence_3'],
    aligned_direction=quantum_dusk['aligned_direction_2']
)
# Any equation
Equation.set_default(
    aligned_direction=quantum_dusk['aligned_direction_1']
)

# Underbar
Underbar.set_default(
)

# Any Table
Table.set_default(
    highlight_top="yes",
    text_size=quantum_dusk['text_size'],
    text_color=quantum_dusk['text_color'],
    decorator_presence=quantum_dusk['decorator_presence_1'],
    decorator_color=quantum_dusk['decorator_color'],
    decorator_color_2=quantum_dusk['decorator_color_2'],
    decorator_color_3=quantum_dusk['decorator_color_3'],
    decorator_color_4=quantum_dusk['decorator_color_4'],
    decorator_stroke_width=quantum_dusk['decorator_stroke_width'],
    corner_rad=quantum_dusk['corner_rad'],
    corner_rad_direction=quantum_dusk['corner_rad_direction'],
    fill_opa=quantum_dusk['fill_opa'],
    h_tightness=quantum_dusk['h_tightness'],
    v_tightness=quantum_dusk['v_tightness'],
    tightness=0,  # So the border of the table is the box without any extra space.
    stroke_opa=quantum_dusk['stroke_opa']
)

Underbar.set_default(
  
)


# Photo Frame
Photo.set_default(
    decorator_style=quantum_dusk['decorator_style'],
    decorator_color=quantum_dusk['decorator_color'],
    text_size=0.75 * quantum_dusk['text_size'],
    text_color=quantum_dusk['text_size'],
    pin_color=quantum_dusk['text_color'],
    corner_rad=quantum_dusk['corner_rad'],
    decorator_stroke_w=quantum_dusk['decorator_stroke_width']
)

# Post-it
Post_It.set_default(
    text_color=quantum_dusk['text_color'],
    text_size=quantum_dusk['text_size'],
    pin_color=quantum_dusk['text_color']
)
