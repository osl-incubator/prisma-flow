"""Pydantic data models for PRISMA-style flow diagrams."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from prismaflow.enums import PrismaTemplate

if TYPE_CHECKING:
    from prismaflow.validation import ValidationReport

Count = Annotated[int, Field(ge=0, strict=True)]
PathLike = str | Path


class FlowMetadata(BaseModel):
    """Optional metadata associated with a PRISMA flow."""

    review_id: str | None = None
    authors: list[str] = Field(default_factory=list)
    created_at: date | None = None
    notes: str | None = None
    extra: dict[str, str] = Field(default_factory=dict)


class IdentificationStage(BaseModel):
    """Identification-stage counts."""

    records_identified_databases: Count
    records_identified_registers: Count

    @property
    def records_identified_total(self) -> int:
        """Total records identified from databases and registers."""
        return self.records_identified_databases + self.records_identified_registers


class ScreeningStage(BaseModel):
    """Screening-stage counts."""

    records_removed_duplicates: Count
    records_removed_automation: Count
    records_removed_other: Count
    records_screened: Count
    records_excluded: Count

    @property
    def records_removed_total(self) -> int:
        """Total records removed before screening."""
        return (
            self.records_removed_duplicates
            + self.records_removed_automation
            + self.records_removed_other
        )


class EligibilityStage(BaseModel):
    """Eligibility-stage counts."""

    reports_sought: Count
    reports_not_retrieved: Count
    reports_assessed: Count
    reports_excluded: dict[str, Count] = Field(default_factory=dict)

    @field_validator("reports_excluded")
    @classmethod
    def _validate_reports_excluded(
        cls,
        value: dict[str, Count],
    ) -> dict[str, Count]:
        for reason, count in value.items():
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError("reports_excluded reasons must be non-empty strings")
            if not isinstance(count, int) or count < 0:
                raise ValueError(
                    "reports_excluded counts must be non-negative integers"
                )
        return value

    @property
    def reports_excluded_total(self) -> int:
        """Total reports excluded after eligibility assessment."""
        return sum(self.reports_excluded.values())


class IncludedStage(BaseModel):
    """Included-stage counts."""

    studies_included: Count


class PrismaFlow(BaseModel):
    """A validated PRISMA-style flow diagram document."""

    template: PrismaTemplate = PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS
    title: str | None = None
    identification: IdentificationStage
    screening: ScreeningStage
    eligibility: EligibilityStage
    included: IncludedStage
    metadata: FlowMetadata | None = None

    model_config = ConfigDict(
        use_enum_values=False,
        validate_assignment=True,
    )

    @classmethod
    def new_review(
        cls,
        *,
        records_identified_databases: int,
        records_identified_registers: int,
        records_removed_duplicates: int,
        records_removed_automation: int,
        records_removed_other: int,
        records_screened: int,
        records_excluded: int,
        reports_sought: int,
        reports_not_retrieved: int,
        reports_assessed: int,
        reports_excluded: dict[str, int] | None = None,
        studies_included: int,
        title: str | None = None,
        metadata: FlowMetadata | None = None,
        template: PrismaTemplate = PrismaTemplate.PRISMA_2020_NEW_DATABASES_REGISTERS,
    ) -> PrismaFlow:
        """Create a PRISMA 2020 new-review flow from flat count arguments."""
        return cls(
            template=template,
            title=title,
            identification=IdentificationStage(
                records_identified_databases=records_identified_databases,
                records_identified_registers=records_identified_registers,
            ),
            screening=ScreeningStage(
                records_removed_duplicates=records_removed_duplicates,
                records_removed_automation=records_removed_automation,
                records_removed_other=records_removed_other,
                records_screened=records_screened,
                records_excluded=records_excluded,
            ),
            eligibility=EligibilityStage(
                reports_sought=reports_sought,
                reports_not_retrieved=reports_not_retrieved,
                reports_assessed=reports_assessed,
                reports_excluded=reports_excluded or {},
            ),
            included=IncludedStage(studies_included=studies_included),
            metadata=metadata,
        )

    def validate(  # type: ignore[override]
        self,
        *,
        strict_included: bool = False,
    ) -> ValidationReport:
        """Validate PRISMA count relationships and return a report."""
        from prismaflow.validation import validate_flow

        return validate_flow(self, strict_included=strict_included)

    def to_layout(self) -> Any:
        """Build the intermediate layout representation for this flow."""
        from prismaflow.layout.engine import build_layout

        return build_layout(self)

    def to_svg(self, path: PathLike | None = None) -> str:
        """Render the flow as SVG and optionally write it to a file."""
        from prismaflow.renderers.svg import SVGRenderer

        output = SVGRenderer().render(self.to_layout())
        _write_text(path, output)
        return output

    def to_html(self, path: PathLike | None = None) -> str:
        """Render the flow as standalone HTML and optionally write it."""
        from prismaflow.renderers.html import HTMLRenderer

        output = HTMLRenderer().render(self.to_layout())
        _write_text(path, output)
        return output

    def to_mermaid(self, path: PathLike | None = None) -> str:
        """Render the flow as Mermaid text and optionally write it."""
        from prismaflow.renderers.mermaid import MermaidRenderer

        output = MermaidRenderer().render(self.to_layout())
        _write_text(path, output)
        return output

    def to_png(self, path: PathLike | None = None) -> bytes:
        """Export PNG if an optional backend is available.

        PNG is intentionally not implemented in v0.1 because the default stable
        output is pure-Python SVG.
        """
        from prismaflow.renderers.png import PNGRenderer

        return PNGRenderer().render(self.to_layout(), path=path)

    def to_json(self, path: PathLike | None = None) -> str:
        """Serialize the flow to JSON and optionally write it."""
        output = self.model_dump_json(indent=2)
        _write_text(path, output + "\n")
        return output

    @classmethod
    def from_json(cls, source: str | Path) -> PrismaFlow:
        """Load a flow from a JSON path or JSON string."""
        from prismaflow.io.json import load_json

        return load_json(source)

    def to_yaml(self, path: PathLike | None = None) -> str:
        """Serialize the flow to YAML when PyYAML is installed."""
        from prismaflow.io.yaml import dump_yaml

        output = dump_yaml(self)
        _write_text(path, output)
        return output

    @classmethod
    def from_yaml(cls, source: str | Path) -> PrismaFlow:
        """Load a flow from YAML when PyYAML is installed."""
        from prismaflow.io.yaml import load_yaml

        return load_yaml(source)


def _write_text(path: PathLike | None, content: str) -> None:
    if path is None:
        return
    Path(path).write_text(content, encoding="utf-8")
