from ...my_imports import *
from ...other_objects import *
from ...graphing_objects import *
from ...text_and_organisation import *

beamer_blue = {
    "tex_temp": TexFontTemplates.droid_serif,  # font for Tex and Mathtex
    "bg_color": "#FFFFFF",  # background color
    "text_size": 30,  # font size
    "text_color": BLACK,  # font color
    "decorator_presence_1": "box",  # general decorator
    "decorator_presence_2": "back_frame",  # special decorator, focus on titles
    "decorator_presence_3": "no",  # unique decorator for references
    "decorator_color": "#003E7C",  # color of the decorator fill and frame
    "decorator_color_2": "#297ACB",  # color of the decorator fill and frame
    "decorator_color_3": "#A0CBFC",  # color of the decorator fill and frame
    "decorator_color_4": "#97DDF9",  # color of the decorator fill and frame
    "decorator_stroke_width": 0.5,  # width of decorator frame
    "corner_rad": 0.1,  # if there is decorator, how rounded corners are
    "corner_rad_direction": [1, 1, 1, 1],  # you can which corners get rounded [UL, UR, DR, DL]
    "fill_opa": 0.9,  # opacity of fill for decorators
    "tightness": 0.2,  # how close the decorator is to the tex
    "h_tightness": 0.5,
    "v_tightness": 0.5,
    "stroke_opa": 2,  # decorator stroke opacity
    "dot_scale": 1.5,  # for Bulleted List, how big dots are
    "direction": RIGHT,  # direction in which lists of strings for TextGeneral will organise themselves
    "aligned_direction_1": LEFT,  # edge with respect the previous organisation takes place
    "aligned_direction_2": [0, 0, 0],  # special for references
    "decorator_style": "techno",  # choice of frame for photos.
}

# Definition of Tex defaults. This will change font and its color.
# Carefull! It seems that there exist some FontTemplates which do not automatically scale the parenthesis. This drove me crazy for some hours. Be aware of what font you choose.

config.background_color = beamer_blue['bg_color']
Tex.set_default(tex_template=beamer_blue['tex_temp'], color= BLACK)
MathTex.set_default(tex_template=beamer_blue['tex_temp'])


# Definition of the attributes of each Class

Text_General.set_default(  # Be careful with general size
    text_size=beamer_blue['text_size'],
    text_color=beamer_blue['text_color'],
    decorator_presence=beamer_blue['decorator_presence_1'],
    decorator_color=beamer_blue['decorator_color'],
    decorator_stroke_width=beamer_blue['decorator_stroke_width'],
    corner_rad=beamer_blue['corner_rad'],
    corner_rad_direction=beamer_blue['corner_rad_direction'],
    fill_opa=beamer_blue['fill_opa'],
    tightness=beamer_blue['tightness'],
    stroke_opa=beamer_blue['stroke_opa'],
    dot_scale=beamer_blue['dot_scale'],
    direction=beamer_blue['direction'],
    aligned_direction=beamer_blue['aligned_direction_1']
)

Title_Presentation.set_default(
    decorator_presence="box",
    tightness=3*beamer_blue['tightness'],
    text_color=WHITE,
)

Title_Section.set_default(
    decorator_presence=beamer_blue['decorator_presence_2'],
    tightness=1.3*beamer_blue['tightness'],
    text_color=WHITE
    
)

BlB.set_default(
    fill_opa=0.1
)

Reference.set_default(
    text_size=0.5 * beamer_blue['text_size'],
    decorator_presence=beamer_blue['decorator_presence_3'],
    aligned_direction=beamer_blue['aligned_direction_2'],
    text_color=WHITE
)
# Any equation
Equation.set_default(
    aligned_direction=beamer_blue['aligned_direction_1'],
    fill_opa=0.1
)

Underbar.set_default(
    text_color= WHITE
)
# Any Table
Table.set_default(
    highlight_top="yes",
    text_size=beamer_blue['text_size'],
    text_color=beamer_blue['text_color'],
    decorator_presence="box",
    decorator_color=beamer_blue['decorator_color'],
    decorator_color_2=beamer_blue['decorator_color_2'],
    decorator_color_3=beamer_blue['decorator_color_3'],
    decorator_color_4=beamer_blue['decorator_color_4'],
    decorator_stroke_width=beamer_blue['decorator_stroke_width'],
    corner_rad=beamer_blue['corner_rad'],
    corner_rad_direction=beamer_blue['corner_rad_direction'],
    fill_opa=0.1,
    h_tightness=beamer_blue['h_tightness'],
    v_tightness=beamer_blue['v_tightness'],
    tightness=0,  # So the border of the table is the box without any extra space.
    stroke_opa=beamer_blue['stroke_opa'],
    stroke_color=beamer_blue['decorator_color_2']
)


# Photo Frame
Photo.set_default(
    decorator_style=beamer_blue['decorator_style'],
    decorator_color=beamer_blue['decorator_color'],
    text_size=0.75 * beamer_blue['text_size'],
    text_color=beamer_blue['text_size'],
    pin_color=beamer_blue['text_color'],
    corner_rad=beamer_blue['corner_rad'],
    decorator_stroke_w=beamer_blue['decorator_stroke_width']
)

# Post-it
Post_It.set_default(
    text_color=beamer_blue['text_color'],
    text_size=beamer_blue['text_size'],
    pin_color=beamer_blue['text_color']
)
