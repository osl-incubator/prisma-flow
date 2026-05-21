from prismaflow import PrismaFlow


def test_svg_renderer_outputs_accessible_svg() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    svg = flow.to_svg()
    assert svg.startswith('<?xml version="1.0"')
    assert "<svg" in svg
    assert "<title" in svg
    assert 'marker-end="url(#arrowhead)"' in svg
    assert "Wrong population" in svg


def test_svg_renderer_escapes_text() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    flow.title = "A < B & C"
    svg = flow.to_svg()
    assert "A &lt; B &amp; C" in svg
