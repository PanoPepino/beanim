from ...my_imports import *
from ...other_objects import *
from ...graphing_objects import *
from ...text_and_organisation import *

fmint = {
    "tex_temp": TexFontTemplates.droid_sans,  # font for Tex and Mathtex
    "bg_color": "#F2FFFB",  # background color
    "text_size": 35,  # font size
    "text_color": '#006661',  # font color
    "decorator_presence_1": "box",  # general decorator
    "decorator_presence_2": "box_long_right",  # special decorator, focus on titles
    "decorator_presence_3": "no",  # unique decorator for references
    "decorator_color": '#006661',  # color of the decorator fill and frame
    "decorator_color_2": "#7DB873",  # color of the decorator fill and frame
    "decorator_color_3": "#0AD46C",  # color of the decorator fill and frame
    "decorator_color_4": "#C6FF7C",  # color of the decorator fill and frame
    "h_tightness": 0.5,
    "v_tightness": 0.5,
    "decorator_stroke_width": 0.5,  # width of decorator frame
    "corner_rad": 0.2,  # if there is decorator, how rounded corners are
    "corner_rad_direction": [1, 1, 0, 0],  # you can which corners get rounded [UL, UR, DR, DL]
    "fill_opa": 0.1,  # opacity of fill for decorators
    "tightness": 0.2,  # how close the decorator is to the tex
    "stroke_opa": 0.5,  # decorator stroke opacity
    "dot_scale": 1.5,  # for Bulleted List, how big dots are
    "direction": RIGHT,  # direction in which lists of strings for TextGeneral will organise themselves
    "aligned_direction_1": LEFT,  # edge with respect the previous organisation takes place
    "aligned_direction_2": [0, 0, 0],  # special for references
    "decorator_style": "techno",  # choice of frame for photos.
}

# Definition of Tex defaults. This will change font and its color.
# Carefull! It seems that there exist some FontTemplates which do not automatically scale the parenthesis. This drove me crazy for some hours. Be aware of what font you choose.

config.background_color = fmint['bg_color']
Tex.set_default(tex_template=fmint['tex_temp'])
MathTex.set_default(tex_template=fmint['tex_temp'])


# Definition of the attributes of each Class

Text_General.set_default(  # Be careful with general size
    text_size=fmint['text_size'],
    text_color=fmint['text_color'],
    decorator_presence=fmint['decorator_presence_1'],
    decorator_color=fmint['decorator_color'],
    decorator_stroke_width=fmint['decorator_stroke_width'],
    corner_rad=fmint['corner_rad'],
    corner_rad_direction=fmint['corner_rad_direction'],
    fill_opa=fmint['fill_opa'],
    tightness=fmint['tightness'],
    stroke_opa=fmint['stroke_opa'],
    dot_scale=fmint['dot_scale'],
    direction=fmint['direction'],
    aligned_direction=fmint['aligned_direction_1']
)

Title_Presentation.set_default(
    decorator_presence=fmint['decorator_presence_2'],
    tightness=3*fmint['tightness']
)

Title_Section.set_default(
    decorator_presence=fmint['decorator_presence_2']
)

BlB.set_default()

Reference.set_default(
    text_size=0.5 * fmint['text_size'],
    decorator_presence=fmint['decorator_presence_3'],
    aligned_direction=fmint['aligned_direction_2']
)
# Any equation
Equation.set_default(
    aligned_direction=fmint['aligned_direction_1']
)

# Any Table
Table.set_default(
    highlight_top="yes",
    text_size=fmint['text_size'],
    text_color=fmint['text_color'],
    decorator_presence=fmint['decorator_presence_1'],
    decorator_color=fmint['decorator_color'],
    decorator_color_2=fmint['decorator_color_2'],
    decorator_color_3=fmint['decorator_color_3'],
    decorator_color_4=fmint['decorator_color_4'],
    decorator_stroke_width=fmint['decorator_stroke_width'],
    corner_rad=fmint['corner_rad'],
    corner_rad_direction=fmint['corner_rad_direction'],
    fill_opa=fmint['fill_opa'],
    h_tightness=fmint['h_tightness'],
    v_tightness=fmint['v_tightness'],
    tightness=0,  # So the border of the table is the box without any extra space.
    stroke_opa=fmint['stroke_opa']
)


# Photo Frame
Photo.set_default(
    decorator_style=fmint['decorator_style'],
    decorator_color=fmint['decorator_color'],
    text_size=0.75 * fmint['text_size'],
    text_color=fmint['text_size'],
    pin_color=fmint['text_color'],
    corner_rad=fmint['corner_rad'],
    decorator_stroke_w=fmint['decorator_stroke_width']
)

# Post-it
Post_It.set_default(
    text_color=fmint['text_color'],
    text_size=fmint['text_size'],
    pin_color=fmint['text_color']
)
