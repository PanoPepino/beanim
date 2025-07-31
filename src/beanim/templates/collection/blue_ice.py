from ...my_imports import *
from ...other_objects import *
from ...graphing_objects import *
from ...text_and_organisation import *

bice = {
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
    "tightness": 0.3,  # how close the decorator is to the tex
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
# Carefull! It seems that there exist some FontTemplates which do not automatically scale the parenthesis. This drove me crazy for some hours. Be aware of what font you choose.

config.background_color = bice['bg_color']
Tex.set_default(tex_template=bice['tex_temp'])
MathTex.set_default(tex_template=bice['tex_temp'])


# Definition of the attributes of each Class

Text_General.set_default(  # Be careful with general size
    text_size=bice['text_size'],
    text_color=bice['text_color'],
    decorator_presence=bice['decorator_presence_1'],
    decorator_color=bice['decorator_color'],
    decorator_stroke_width=bice['decorator_stroke_width'],
    corner_rad=bice['corner_rad'],
    corner_rad_direction=bice['corner_rad_direction'],
    fill_opa=bice['fill_opa'],
    tightness=bice['tightness'],
    stroke_opa=bice['stroke_opa'],
    dot_scale=bice['dot_scale'],
    direction=bice['direction'],
    aligned_direction=bice['aligned_direction_1']
)

Title_Presentation.set_default(
    decorator_presence=bice['decorator_presence_2'],
    tightness=3*bice['tightness']
)

Title_Section.set_default(
    decorator_presence=bice['decorator_presence_2']
)

BlB.set_default()

Reference.set_default(
    text_size=0.5 * bice['text_size'],
    decorator_presence=bice['decorator_presence_3'],
    aligned_direction=bice['aligned_direction_2']
)
# Any equation
Equation.set_default(
    aligned_direction=bice['aligned_direction_1']
)

# Any Table
Table.set_default(
    highlight_top="yes",
    text_size=bice['text_size'],
    text_color=bice['text_color'],
    decorator_presence=bice['decorator_presence_1'],
    decorator_color=bice['decorator_color'],
    decorator_color_2=bice['decorator_color_2'],
    decorator_color_3=bice['decorator_color_3'],
    decorator_color_4=bice['decorator_color_4'],
    decorator_stroke_width=bice['decorator_stroke_width'],
    corner_rad=bice['corner_rad'],
    corner_rad_direction=bice['corner_rad_direction'],
    fill_opa=bice['fill_opa'],
    h_tightness=bice['h_tightness'],
    v_tightness=bice['v_tightness'],
    tightness=0,  # So the border of the table is the box without any extra space.
    stroke_opa=bice['stroke_opa']
)


# Photo Frame
Photo.set_default(
    decorator_style=bice['decorator_style'],
    decorator_color=bice['decorator_color'],
    text_size=0.75 * bice['text_size'],
    text_color=bice['text_size'],
    pin_color=bice['text_color'],
    corner_rad=bice['corner_rad'],
    decorator_stroke_w=bice['decorator_stroke_width']
)

# Post-it
Post_It.set_default(
    text_color=bice['text_color'],
    text_size=bice['text_size'],
    pin_color=bice['text_color']
)
