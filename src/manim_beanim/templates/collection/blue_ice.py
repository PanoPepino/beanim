from ...my_imports import *
from ...other_objects import *
from ...graphing_objects import *
from ...text_and_organisation import *

blue_ice = {
    "tex_temp": TexFontTemplates.biolinum,  # font for Tex and Mathtex
    "bg_color": "#F1F8FF",  # background color
    "text_size": 35,  # font size
    "text_color": "#003E7C",  # font color
    "decorator_presence_1": "box",  # general decorator
    "decorator_presence_2": "back_frame",  # special decorator, focus on titles
    "decorator_presence_3": "no",  # unique decorator for references
    "decorator_color": "#003E7C",  # color of the decorator fill and frame
    "decorator_color_2": "#7973B8",  # color of the decorator fill and frame
    "decorator_color_3": "#A0BCFC",  # color of the decorator fill and frame
    "decorator_color_4": "#7CDAFF",  # color of the decorator fill and frame
    "decorator_stroke_width": 1,  # width of decorator frame
    "corner_rad": 0.05,  # if there is decorator, how rounded corners are
    "corner_rad_direction": [1, 1, 1, 1],  # you can which corners get rounded [UL, UR, DR, DL]
    "fill_opa": 0.05,  # opacity of fill for decorators
    "tightness": 0.2,  # how close the decorator is to the tex
    "h_tightness": 0.5,
    "v_tightness": 0.5,
    "stroke_opa": 1,  # decorator stroke opacity
    "dot_scale": 1.5,  # for Bulleted List, how big dots are
    "direction": RIGHT,  # direction in which lists of strings for TextGeneral will organise themselves
    "aligned_direction_1": LEFT,  # edge with respect the previous organisation takes place
    "aligned_direction_2": [0, 0, 0],  # special for references
    "decorator_style": "techno",  # choice of frame for photos.
}

# Definition of Tex defaults. This will change font and its color.
# Careful! It seems that there exist some FontTemplates which do not automatically scale the parenthesis. This drove me crazy for some hours. Be aware of what font you choose.

config.background_color = blue_ice['bg_color']
Tex.set_default(tex_template=blue_ice['tex_temp'])
MathTex.set_default(tex_template=blue_ice['tex_temp'])


# Definition of the attributes of each Class

Text_General.set_default(  # Be careful with general size
    text_size=blue_ice['text_size'],
    text_color=blue_ice['text_color'],
    decorator_presence=blue_ice['decorator_presence_1'],
    decorator_color=blue_ice['decorator_color'],
    decorator_stroke_width=blue_ice['decorator_stroke_width'],
    corner_rad=blue_ice['corner_rad'],
    corner_rad_direction=blue_ice['corner_rad_direction'],
    fill_opa=blue_ice['fill_opa'],
    tightness=blue_ice['tightness'],
    stroke_opa=blue_ice['stroke_opa'],
    dot_scale=blue_ice['dot_scale'],
    direction=blue_ice['direction'],
    aligned_direction=blue_ice['aligned_direction_1']
)

Title_Presentation.set_default(
    decorator_presence=blue_ice['decorator_presence_2'],
    tightness=3*blue_ice['tightness']
)

Title_Section.set_default(
    decorator_presence=blue_ice['decorator_presence_2'],
    tightness=1.3*blue_ice['tightness']
)

BlB.set_default()

Reference.set_default(
    text_size=0.5 * blue_ice['text_size'],
    decorator_presence=blue_ice['decorator_presence_3'],
    aligned_direction=blue_ice['aligned_direction_2']
)
# Any equation
Equation.set_default(
    aligned_direction=blue_ice['aligned_direction_1']
)

# Underbar
Underbar.set_default(
)

# Any Table
Table.set_default(
    highlight_top="yes",
    text_size=blue_ice['text_size'],
    text_color=blue_ice['text_color'],
    decorator_presence=blue_ice['decorator_presence_1'],
    decorator_color=blue_ice['decorator_color'],
    decorator_color_2=blue_ice['decorator_color_2'],
    decorator_color_3=blue_ice['decorator_color_3'],
    decorator_color_4=blue_ice['decorator_color_4'],
    decorator_stroke_width=blue_ice['decorator_stroke_width'],
    corner_rad=blue_ice['corner_rad'],
    corner_rad_direction=blue_ice['corner_rad_direction'],
    fill_opa=blue_ice['fill_opa'],
    h_tightness=blue_ice['h_tightness'],
    v_tightness=blue_ice['v_tightness'],
    tightness=0,  # So the border of the table is the box without any extra space.
    stroke_opa=blue_ice['stroke_opa']
)

Underbar.set_default(
  
)


# Photo Frame
Photo.set_default(
    decorator_style=blue_ice['decorator_style'],
    decorator_color=blue_ice['decorator_color'],
    text_size=0.75 * blue_ice['text_size'],
    text_color=blue_ice['text_size'],
    pin_color=blue_ice['text_color'],
    corner_rad=blue_ice['corner_rad'],
    decorator_stroke_w=blue_ice['decorator_stroke_width']
)

# Post-it
Post_It.set_default(
    text_color=blue_ice['text_color'],
    text_size=blue_ice['text_size'],
    pin_color=blue_ice['text_color']
)
