from ...my_imports import *
from ...other_objects import *
from ...graphing_objects import *
from ...text_and_organisation import *

fautumn = {
    "tex_temp": TexFontTemplates.helvetica_fourier_it,  # font for Tex and Mathtex
    "bg_color": "#FAF9F5",  # background color
    "text_size": 35,  # font size
    "text_color": "#81331B",  # font color
    "decorator_presence_1": "no",  # general decorator
    "decorator_presence_2": "box_long_right",  # special decorator, focus on titles
    "decorator_presence_3": "no",  # unique decorator for references
    "decorator_color": "#81331B",  # color of the decorator fill and frame
    "decorator_color_2": "#B87390",  # color of the decorator fill and frame
    "decorator_color_3": "#F49191",  # color of the decorator fill and frame
    "decorator_color_4": "#FFC67C",  # color of the decorator fill and frame
    "h_tightness": 0.5,
    "v_tightness": 0.5,
    "decorator_stroke_width": 1,  # width of decorator frame
    "corner_rad": -0.05,  # if there is decorator, how rounded corners are
    "corner_rad_direction": [1, 0, 0, 0],  # you can which corners get rounded [UL, UR, DR, DL]
    "fill_opa": 0.1,  # opacity of fill for decorators
    "tightness": 0.3,  # how close the decorator is to the tex
    "stroke_opa": 2,  # decorator stroke opacity
    "dot_scale": 1.5,  # for Bulleted List, how big dots are
    "direction": RIGHT,  # direction in which lists of strings for TextGeneral will organise themselves
    "aligned_direction_1": LEFT,  # edge with respect the previous organisation takes place
    "aligned_direction_2": [0, 0, 0],  # special for references
    "decorator_style": "techno",  # choice of frame for photos.
}

# Definition of Tex defaults. This will change font and its color.
# Carefull! It seems that there exist some FontTemplates which do not automatically scale the parenthesis. This drove me crazy for some hours. Be aware of what font you choose.

config.background_color = fautumn['bg_color']
Tex.set_default(tex_template=fautumn['tex_temp'])
MathTex.set_default(tex_template=fautumn['tex_temp'])


# Definition of the attributes of each Class

Text_General.set_default(  # Be careful with general size
    text_size=fautumn['text_size'],
    text_color=fautumn['text_color'],
    decorator_presence=fautumn['decorator_presence_1'],
    decorator_color=fautumn['decorator_color'],
    decorator_stroke_width=fautumn['decorator_stroke_width'],
    corner_rad=fautumn['corner_rad'],
    corner_rad_direction=fautumn['corner_rad_direction'],
    fill_opa=fautumn['fill_opa'],
    tightness=fautumn['tightness'],
    stroke_opa=fautumn['stroke_opa'],
    dot_scale=fautumn['dot_scale'],
    direction=fautumn['direction'],
    aligned_direction=fautumn['aligned_direction_1']
)

Title_Presentation.set_default(
    decorator_presence=fautumn['decorator_presence_2'],
    tightness=3*fautumn['tightness']
)

Title_Section.set_default(
    decorator_presence=fautumn['decorator_presence_2']
)

BlB.set_default(
    decorator_presence=fautumn['decorator_presence_2']
)

Reference.set_default(
    text_size=0.5 * fautumn['text_size'],
    decorator_presence=fautumn['decorator_presence_3'],
    aligned_direction=fautumn['aligned_direction_2']
)
# Any equation
Equation.set_default(
    aligned_direction=fautumn['aligned_direction_1']
)

# Any Table
Table.set_default(
    highlight_top="yes",
    text_size=fautumn['text_size'],
    text_color=fautumn['text_color'],
    decorator_presence=fautumn['decorator_presence_1'],
    decorator_color=fautumn['decorator_color'],
    decorator_color_2=fautumn['decorator_color_2'],
    decorator_color_3=fautumn['decorator_color_3'],
    decorator_color_4=fautumn['decorator_color_4'],
    decorator_stroke_width=fautumn['decorator_stroke_width'],
    corner_rad=fautumn['corner_rad'],
    corner_rad_direction=fautumn['corner_rad_direction'],
    fill_opa=fautumn['fill_opa'],
    h_tightness=fautumn['h_tightness'],
    v_tightness=fautumn['v_tightness'],
    tightness=0,  # So the border of the table is the box without any extra space.
    stroke_opa=fautumn['stroke_opa']
)


# Photo Frame
Photo.set_default(
    decorator_style=fautumn['decorator_style'],
    decorator_color=fautumn['decorator_color'],
    text_size=0.75 * fautumn['text_size'],
    text_color=fautumn['text_size'],
    pin_color=fautumn['text_color'],
    corner_rad=fautumn['corner_rad'],
    decorator_stroke_w=fautumn['decorator_stroke_width']
)

# Post-it
Post_It.set_default(
    text_color=fautumn['text_color'],
    text_size=fautumn['text_size'],
    pin_color=fautumn['text_color']
)
