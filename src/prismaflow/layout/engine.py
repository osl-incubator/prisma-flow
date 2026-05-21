"""Layout dataclasses and template dispatch."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from prismaflow.enums import PrismaTemplate
from prismaflow.exceptions import TemplateNotSupportedError
from prismaflow.layout.geometry import Anchor, Point, Rect

NodeKind = Literal["stage", "exclusion", "header", "note"]


@dataclass
class DiagramNode:
    """A positioned text box in a diagram."""

    id: str
    rect: Rect
    text: str
    kind: NodeKind = "stage"
    href: str | None = None
    tooltip: str | None = None
    css_class: str | None = None


@dataclass
class DiagramEdge:
    """An arrow connecting two diagram nodes."""

    id: str
    source_id: str
    target_id: str
    source_anchor: Anchor
    target_anchor: Anchor
    label: str | None = None
    path: list[Point] | None = None
    css_class: str | None = None


@dataclass
class DiagramLayout:
    """Complete intermediate representation for a rendered diagram."""

    width: float
    height: float
    nodes: list[DiagramNode] = field(default_factory=list)
    edges: list[DiagramEdge] = field(default_factory=list)
    title: str | None = None

    def node_by_id(self, node_id: str) -> DiagramNode:
        """Return a node by ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        raise KeyError(node_id)


def build_layout(flow: object) -> DiagramLayout:
    """Build a diagram layout for a supported PRISMA flow template."""
    from prismaflow.models import PrismaFlow
    from prismaflow.templates.prisma_2020_new import Prisma2020NewTemplate

    if not isinstance(flow, PrismaFlow):
        raise TypeError("build_layout expects a PrismaFlow instance")

    if flow.template == PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS:
        return Prisma2020NewTemplate().build(flow)

    raise TemplateNotSupportedError(
        f"Template is not implemented in v0.1: {flow.template.value}"
    )
