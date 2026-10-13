"""Shared constructor annotations; runtime validation remains explicit."""
from collections.abc import Mapping, Sequence
from os import PathLike
from typing import TypeAlias
from manim import ManimColor
import numpy as np

ColorLike: TypeAlias = str | ManimColor | int | Sequence[float] | np.ndarray
VectorLike: TypeAlias = Sequence[float] | np.ndarray
TextContent: TypeAlias = str | list[str] | tuple[str, ...]
DictionarySource: TypeAlias = str | PathLike[str] | Mapping[str, object]
TableCell: TypeAlias = str | int | float
TableRows: TypeAlias = list[list[TableCell] | tuple[TableCell, ...]] | tuple[list[TableCell] | tuple[TableCell, ...], ...]
