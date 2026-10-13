"""Source-resolution clipping with affine image coordinates and Cairo fill rules."""
import cairo
import numpy as np
from PIL import Image, ImageChops
from manim import ImageMobject, VMobject


def clip_image_to_mobject(image: ImageMobject, mobj: VMobject) -> ImageMobject:
    """Clip planar image against vector fill, including holes and disconnected paths.

    Cubic curves are rasterized by Cairo at source resolution. The output retains
    image rotation/shear and multiplies source alpha by antialiased coverage.
    Nonplanar masks and singular image transforms fail before creating output.
    """
    source = Image.fromarray(image.pixel_array).convert('RGBA')
    width, height = source.size
    corners = np.asarray(image.points, dtype=float)
    if corners.shape != (4, 3) or not np.isfinite(corners).all():
        raise ValueError('Image must have four finite planar corners')
    origin = corners[0]
    basis = np.column_stack((corners[1] - origin, corners[2] - origin))
    if np.linalg.matrix_rank(basis) != 2:
        raise ValueError('Image must have nonzero dimensions')
    if not np.allclose(corners[3], origin + basis.sum(axis=1)):
        raise ValueError('Image transform must be affine')
    inverse = np.linalg.pinv(basis)
    surface = cairo.ImageSurface(cairo.FORMAT_A8, width, height)
    stride = surface.get_stride()
    context = cairo.Context(surface)
    context.set_antialias(cairo.ANTIALIAS_BEST)
    context.set_tolerance(0.1)
    context.set_fill_rule(cairo.FILL_RULE_WINDING)
    context.set_source_rgba(1, 1, 1, 1)
    paths = 0
    for member in mobj.family_members_with_points():
        if not hasattr(member, 'get_subpaths'):
            raise ValueError('Clipping shape must contain vector outlines')
        for subpath in member.get_subpaths():
            if len(subpath) % 4:
                raise ValueError('Clipping outline must contain cubic curves')
            coordinates = (subpath - origin) @ inverse.T
            projected = coordinates @ basis.T + origin
            if not np.allclose(projected, subpath, atol=1e-7):
                raise ValueError('Clipping shape must lie in image plane')
            curves = (coordinates * (width, height)).reshape(-1, 4, 2)
            context.move_to(*curves[0, 0])
            for curve in curves:
                context.curve_to(*curve[1:].ravel())
            context.close_path()
            paths += 1
    if not paths:
        raise ValueError('Clipping shape must contain a vector outline')
    context.fill()
    surface.flush()
    coverage = Image.frombuffer('L', source.size, surface.get_data(), 'raw', 'L', stride, 1)
    source.putalpha(ImageChops.multiply(source.getchannel('A'), coverage))
    box = source.getbbox()
    if box is None:
        raise ValueError('Clipping shape does not overlap image')
    result = ImageMobject(source.crop(box))
    left, top, right, bottom = box
    uv = np.array([(left, top), (right, top), (left, bottom), (right, bottom)]) / (width, height)
    result.points = origin + uv @ basis.T
    return result
