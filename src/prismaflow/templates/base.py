"""Template builder interfaces."""

from __future__ import annotations

from typing import Protocol

from prismaflow.layout.engine import DiagramLayout


class TemplateBuilder(Protocol):
    """Protocol implemented by PRISMA template builders."""

    def build(self, flow: object) -> DiagramLayout:
        """Build a diagram layout for a flow."""
        ...
