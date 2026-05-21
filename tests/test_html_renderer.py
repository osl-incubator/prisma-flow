from prismaflow import PrismaFlow


def test_html_renderer_embeds_svg() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    html = flow.to_html()
    assert html.startswith("<!doctype html>")
    assert "<svg" in html
    assert "Example PRISMA Flow Diagram" in html
