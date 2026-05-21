import pytest

import prismaflow.renderers.png as png_module
from prismaflow import PrismaFlow
from prismaflow.exceptions import OptionalDependencyError
from prismaflow.renderers.png import PNGRenderer


def test_png_renderer_outputs_png_bytes() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    png = flow.to_png()

    assert png.startswith(b"\x89PNG\r\n\x1a\n")


def test_png_renderer_writes_png_file(tmp_path) -> None:  # type: ignore[no-untyped-def]
    output = tmp_path / "prisma.png"
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    png = flow.to_png(output)

    assert output.read_bytes() == png


def test_png_renderer_reports_missing_optional_dependency(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    def missing_import(name: str) -> object:
        raise ImportError(name)

    monkeypatch.setattr(png_module, "import_module", missing_import)
    flow = PrismaFlow.from_json("examples/basic_new_review.json")

    with pytest.raises(OptionalDependencyError, match="prisma-flow\\[png\\]"):
        PNGRenderer().render(flow.to_layout())


def test_png_renderer_rejects_non_positive_scale() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        PNGRenderer(scale=0)
