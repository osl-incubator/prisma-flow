"""Geometry primitives for diagram layout."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Anchor = Literal["top", "bottom", "left", "right"]


@dataclass(frozen=True)
class Point:
    """A point in diagram coordinates."""

    x: float
    y: float


@dataclass(frozen=True)
class Rect:
    """A rectangular diagram area."""

    x: float
    y: float
    width: float
    height: float

    @property
    def center_x(self) -> float:
        """Horizontal center coordinate."""
        return self.x + self.width / 2

    @property
    def center_y(self) -> float:
        """Vertical center coordinate."""
        return self.y + self.height / 2

    @property
    def top_center(self) -> Point:
        """Top-center anchor."""
        return Point(self.center_x, self.y)

    @property
    def bottom_center(self) -> Point:
        """Bottom-center anchor."""
        return Point(self.center_x, self.y + self.height)

    @property
    def left_center(self) -> Point:
        """Left-center anchor."""
        return Point(self.x, self.center_y)

    @property
    def right_center(self) -> Point:
        """Right-center anchor."""
        return Point(self.x + self.width, self.center_y)

    def anchor(self, name: Anchor) -> Point:
        """Return a named anchor point."""
        if name == "top":
            return self.top_center
        if name == "bottom":
            return self.bottom_center
        if name == "left":
            return self.left_center
        return self.right_center

    def overlaps(self, other: Rect, *, padding: float = 0) -> bool:
        """Return whether this rectangle overlaps another rectangle."""
        return not (
            self.x + self.width + padding <= other.x
            or other.x + other.width + padding <= self.x
            or self.y + self.height + padding <= other.y
            or other.y + other.height + padding <= self.y
        )
