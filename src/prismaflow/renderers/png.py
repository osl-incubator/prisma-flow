"""
title: Optional PNG renderer.
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any, cast

from prismaflow.exceptions import OptionalDependencyError
from prismaflow.layout.engine import DiagramLayout
from prismaflow.renderers.svg import SVGRenderer

Transform = tuple[float, float, float, float, float, float]


class PNGRenderer:
    """
    title: Render diagram layouts to PNG through the optional resvg backend.
    attributes:
      scale:
        description: Scale factor applied while rasterizing the SVG.
      load_system_fonts:
        description: Whether resvg should load locally available fonts.
    """

    def __init__(self, *, scale: float = 1.0, load_system_fonts: bool = True) -> None:
        """
        title: Configure PNG rasterization.
        parameters:
          scale:
            type: float
            description: Scale factor applied while rasterizing the SVG.
          load_system_fonts:
            type: bool
            description: Whether resvg should load locally available fonts.
        """
        if scale <= 0:
            raise ValueError("PNG scale must be greater than zero")
        self.scale = scale
        self.load_system_fonts = load_system_fonts

    def render(self, layout: DiagramLayout, *, path: str | Path | None = None) -> bytes:
        """
        title: Render a layout as PNG bytes and optionally write it to a file.
        parameters:
          layout:
            type: DiagramLayout
            description: Value for layout.
          path:
            type: str | Path | None
            description: Value for path.
        returns:
          type: bytes
          description: Return value.
        """
        resvg = _load_resvg()
        options = resvg.usvg.Options.default()
        if self.load_system_fonts:
            options.load_system_fonts()

        svg = SVGRenderer().render(layout)
        tree = resvg.usvg.Tree.from_str(svg, options)
        png = cast(bytes, resvg.render(tree, self._transform()))
        if path is not None:
            Path(path).write_bytes(png)
        return png

    def _transform(self) -> Transform:
        """
        title: Return the affine transform used by resvg.
        returns:
          type: Transform
          description: Return value.
        """
        return (self.scale, 0.0, 0.0, self.scale, 0.0, 0.0)


def _load_resvg() -> Any:
    """
    title: Import the optional resvg backend.
    returns:
      type: Any
      description: Imported resvg module.
    """
    try:
        return import_module("resvg")
    except ImportError as exc:
        raise OptionalDependencyError(
            "PNG export requires the optional dependency.\n\n"
            "Install it with:\n\n"
            '  pip install "prisma-flow[png]"'
        ) from exc
