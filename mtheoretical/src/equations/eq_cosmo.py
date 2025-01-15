from manim import *
from .eq_general import *

class Eq_Cosmo(Eq_General, VGroup):
    """Class to create equations related to cosmology. It has a dictionary built in.
  
    """
    def __init__(self,
                 the_equation,
                 **kwargs):
        
        super().__init__(**kwargs)
        
        # To split the dictionary, use {{}} on each element you want to separate.
        self.eq_cosmo_refs= {
            
            'fried ind': '\\left(\\frac{\\dot{a}}{a}\\right)^{2}= -\\frac{1}{a^{2}} + \\frac{8 \\pi}{3} 2  \\left(\\frac{1}{k_{-}}-\\frac{1}{k_{+}}\\right)^{-1} G_{5} \\left(\\sigma_{cr}- \\sigma\\right) + \\mathcal{O}(\\epsilon^{2})',
            'fried ind usual': '\\left(\\frac{\\dot{a}}{a}\\right)^{2}= -\\frac{1}{a^{2}} + \\frac{8 \\pi}{3} G_{4} \\rho_{\\Lambda} + \\mathcal{O}(\\epsilon^{2})',
            'fried ind matter': '\\left(\\frac{\\dot{a}}{a}\\right)^{2}= -\\frac{1}{a^{2}} + \\frac{8 \\pi}{3} G_{4} \\left(\\Lambda_{4} + \\frac{1}{2 \\pi^{2}}\\left(\\tfrac{M_{+}}{k_{+}}- \\tfrac{M_{-}}{k_{-}}\\right)\\frac{1}{a^{4}}\\right)',
            'fried ind strings': '\\left(\\frac{\\dot{a}}{a}\\right)^{2}= -\\frac{1}{a^{2}} + \\frac{8 \\pi}{3} G_{4} \left(\\Lambda_{4} + \\frac{3}{8 \\pi a^{3}}\\left(\\tfrac{\\alpha_{+}}{k_{+}}- \\tfrac{\\alpha_{-}}{k_{-}}\\right) \\right)',
            'fried ind gw': '\\left(\\frac{\\tilde{a}(\\eta)}{a(\\eta)}\\right)^{2}= -\\frac{1}{a^{2}} + \\frac{8 \\pi}{3} G_{4} \\left(\\Lambda_{4} + 3 \\zeta^{2}\\left(\\frac{q_{1}}{a^{2}}- \\frac{q_{3}}{H^{2}a^{4}}\\right) \\right)',
            'fried ind bh rs': '\\dot{a}^2=\\frac{1}{4 \\sigma^2 a^2}\\left[\\left(k_{-}^2-k_{+}^2\\right) a^2+\\left(f_{-}(a)-f_{+}(a)\\right)\\right]^2+\\frac{\\sigma^2}{4} a^2-\\frac{1}{2}\\left[\\left(f_{-}(a)+f_{+}(a)\\right)+\\left(k_{-}^2+k_{+}^2\\right) a^2\\right]',
           'fried ind bh dbi': '\\dot{\\mathcal{Z}}^2= -f(\\mathcal{Z})-k^2 \\mathcal{Z}^2+\\frac{k^2}{k^2 J_c^2+\\mathcal{Z}^6}\\left(\\mathcal{Z}^4-\\mathcal{Z}_H^4+\\frac{\\theta \\kappa_5 J_c}{\\mathcal{Z}_H^2}\\left(1-\\frac{\\mathcal{Z}_H^2}{\\mathcal{Z}^2}\\right)\\right)^2',
           'fried ind bh rs junc': '\\dot{a}^2= -f(a)-k^2 a^2+\\frac{k^2}{a^6}\\left(a^4-a_H^4-\\frac{\\kappa_5^2 \\theta \\Delta \\theta}{a_H^2 k \\Delta k}\\left(1-\\frac{a_H^2}{a^2}\\right)\\right)^2',
           'fried ind no exp': 'H^{2}= -\\frac{1}{a^{2}} + \\frac{1}{3}\\left(\\frac{\\kappa_{5}^{2}\\sigma^{2}}{12} - \\frac{3}{2}\\left(k^{2}_{+}+k^{2}_{-}\\right) + \\frac{27}{4} \\left(\\frac{k^{2}_{-}-k^{2}_{+}}{\\kappa_{5}\\sigma}\\right)^{2}\\right)'

         }
        
        self.chosen_equation= MathTex(str(self.eq_cosmo_refs[the_equation]), font_size= self.text_size, color= self.text_color)
        
        
        if self.decorator_presence== "box":
            self.box= SurroundingRectangle(self.chosen_equation, corner_radius= self.corner_rad, buff= self.tightness,  stroke_width= self.decorator_stroke_width, color= self.decorator_color, fill_opacity= self.fill_opa)
            self.add(self.chosen_equation, self.box)
        else:
            self.add(self.chosen_equation)