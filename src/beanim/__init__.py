"""Beanim package: tools for building beamer like slides with Manim."""

from .figures import *
from .other_objects import *
from .graphing_objects import *
from .text_and_organisation import *
from .templates import *
from .tools import *

__all__ = []
__all__ += text_and_organisation.__all__
__all__ += other_objects.__all__
__all__ += graphing_objects.__all__
__all__ += templates.__all__
__all__ += tools.__all__
