from ...my_imports import *
from ...other_objects import *
from ...graphing_objects import *
from ...text_and_organisation import *

green_mint = {
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
    "decorator_stroke_width": 1,  # width of decorator frame
    "corner_rad": 0.1,  # if there is decorator, how rounded corners are
    "corner_rad_direction": [1, 1, 0, 1],  # you can which corners get rounded [UL, DL, DR, UR]
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

config.background_color = green_mint['bg_color']
Tex.set_default(tex_template=green_mint['tex_temp'])
MathTex.set_default(tex_template=green_mint['tex_temp'])


# Definition of the attributes of each Class

Text_General.set_default(  # Be careful with general size
    text_size=green_mint['text_size'],
    text_color=green_mint['text_color'],
    decorator_presence=green_mint['decorator_presence_1'],
    decorator_color=green_mint['decorator_color'],
    decorator_stroke_width=green_mint['decorator_stroke_width'],
    corner_rad=green_mint['corner_rad'],
    corner_rad_direction=green_mint['corner_rad_direction'],
    fill_opa=green_mint['fill_opa'],
    tightness=green_mint['tightness'],
    stroke_opa=green_mint['stroke_opa'],
    dot_scale=green_mint['dot_scale'],
    direction=green_mint['direction'],
    aligned_direction=green_mint['aligned_direction_1']
)

Title_Presentation.set_default(
    decorator_presence=green_mint['decorator_presence_2'],
    tightness=3*green_mint['tightness']
)

Title_Section.set_default(
    decorator_presence=green_mint['decorator_presence_2']
)

BlB.set_default()

Reference.set_default(
    text_size=0.5 * green_mint['text_size'],
    decorator_presence=green_mint['decorator_presence_3'],
    aligned_direction=green_mint['aligned_direction_2']
)
# Any equation
Equation.set_default(
    aligned_direction=green_mint['aligned_direction_1']
)

Underbar.set_default(
  
)

# Any Table
Table.set_default(
    highlight_top="yes",
    text_size=green_mint['text_size'],
    text_color=green_mint['text_color'],
    decorator_presence=green_mint['decorator_presence_1'],
    decorator_color=green_mint['decorator_color'],
    decorator_color_2=green_mint['decorator_color_2'],
    decorator_color_3=green_mint['decorator_color_3'],
    decorator_color_4=green_mint['decorator_color_4'],
    decorator_stroke_width=green_mint['decorator_stroke_width'],
    corner_rad=green_mint['corner_rad'],
    corner_rad_direction=green_mint['corner_rad_direction'],
    fill_opa=green_mint['fill_opa'],
    h_tightness=green_mint['h_tightness'],
    v_tightness=green_mint['v_tightness'],
    tightness=0,  # So the border of the table is the box without any extra space.
    stroke_opa=green_mint['stroke_opa']
)


# Photo Frame
Photo.set_default(
    decorator_style=green_mint['decorator_style'],
    decorator_color=green_mint['decorator_color'],
    text_size=0.75 * green_mint['text_size'],
    text_color=green_mint['text_size'],
    pin_color=green_mint['text_color'],
    corner_rad=green_mint['corner_rad'],
    decorator_stroke_w=green_mint['decorator_stroke_width']
)

# Post-it
Post_It.set_default(
    text_color=green_mint['text_color'],
    text_size=green_mint['text_size'],
    pin_color=green_mint['text_color']
)
