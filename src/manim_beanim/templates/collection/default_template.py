from ...my_imports import *
from ...other_objects import *
from ...graphing_objects import *
from ...text_and_organisation import *

deftemp = {
    "tex_temp": TexFontTemplates.latin_modern_tw,  # font for Tex and Mathtex
    "bg_color": WHITE,  # background color
    "text_size": 35,  # font size
    "text_color": BLACK,  # font color
    "decorator_presence_1": "box",  # general decorator
    "decorator_presence_2": "back_frame",  # special decorator, focus on titles
    "decorator_presence_3": "no",  # unique decorator for references
    "decorator_color": BLACK,  # color of the decorator fill and frame
    "decorator_color_2": GREY_A,  # color of the decorator fill and frame
    "decorator_color_3": GREY_B,  # color of the decorator fill and frame
    "decorator_color_4": GREY_C,  # color of the decorator fill and frame
    "h_tightness": 0.5,
    "v_tightness": 0.5,
    "decorator_stroke_width": 1,  # width of decorator frame
    "corner_rad": 0,  # if there is decorator, how rounded corners are
    "corner_rad_direction": [0, 0, 0, 0],  # you can which corners get rounded [UL, UR, DR, DL]
    "fill_opa": 0.1,  # opacity of fill for decorators
    "tightness": 0.3,  # how close the decorator is to the tex
    "stroke_opa": 1,  # decorator stroke opacity
    "dot_scale": 1,  # for Bulleted List, how big dots are
    "direction": RIGHT,  # direction in which lists of strings for TextGeneral will organise themselves
    "aligned_direction_1": LEFT,  # edge with respect the previous organisation takes place
    "aligned_direction_2": [0, 0, 0],  # special for references
    "decorator_style": "techno",  # choice of frame for photos.
}

# Definition of Tex defaults. This will change font and its color.
# Carefull! It seems that there exist some FontTemplates which do not automatically scale the parenthesis. This drove me crazy for some hours. Be aware of what font you choose.

config.background_color = deftemp['bg_color']
Tex.set_default(tex_template=deftemp['tex_temp'])
MathTex.set_default(tex_template=deftemp['tex_temp'])


# Definition of the attributes of each Class

Text_General.set_default(  # Be careful with general size
    text_size=deftemp['text_size'],
    text_color=deftemp['text_color'],
    decorator_presence=deftemp['decorator_presence_1'],
    decorator_color=deftemp['decorator_color'],
    decorator_stroke_width=deftemp['decorator_stroke_width'],
    corner_rad=deftemp['corner_rad'],
    corner_rad_direction=deftemp['corner_rad_direction'],
    fill_opa=deftemp['fill_opa'],
    tightness=deftemp['tightness'],
    stroke_opa=deftemp['stroke_opa'],
    dot_scale=deftemp['dot_scale'],
    direction=deftemp['direction'],
    aligned_direction=deftemp['aligned_direction_1']
)

Title_Presentation.set_default(
    decorator_presence=deftemp['decorator_presence_2'],
    tightness=3*deftemp['tightness']
)

Title_Section.set_default(
    decorator_presence=deftemp['decorator_presence_2']
)

BlB.set_default()

Reference.set_default(
    text_size=0.5 * deftemp['text_size'],
    decorator_presence=deftemp['decorator_presence_3'],
    aligned_direction=deftemp['aligned_direction_2']
)
# Any equation
Equation.set_default(
    aligned_direction=deftemp['aligned_direction_1']
)

# Any Table
Table.set_default(
    highlight_top="yes",
    text_size=deftemp['text_size'],
    text_color=deftemp['text_color'],
    decorator_presence=deftemp['decorator_presence_1'],
    decorator_color=deftemp['decorator_color'],
    decorator_color_2=deftemp['decorator_color_2'],
    decorator_color_3=deftemp['decorator_color_3'],
    decorator_color_4=deftemp['decorator_color_4'],
    decorator_stroke_width=deftemp['decorator_stroke_width'],
    corner_rad=deftemp['corner_rad'],
    corner_rad_direction=deftemp['corner_rad_direction'],
    fill_opa=deftemp['fill_opa'],
    h_tightness=deftemp['h_tightness'],
    v_tightness=deftemp['v_tightness'],
    tightness=0,  # So the border of the table is the box without any extra space.
    stroke_opa=deftemp['stroke_opa']
)


# Photo Frame
Photo.set_default(
    decorator_style=deftemp['decorator_style'],
    decorator_color=deftemp['decorator_color'],
    text_size=0.75 * deftemp['text_size'],
    text_color=deftemp['text_size'],
    pin_color=deftemp['text_color'],
    corner_rad=deftemp['corner_rad'],
    decorator_stroke_w=deftemp['decorator_stroke_width']
)

# Post-it
Post_It.set_default(
    text_color=deftemp['text_color'],
    text_size=deftemp['text_size'],
    pin_color=deftemp['text_color']
)
