from prismaflow import PrismaFlow
from prismaflow.layout.overlap import find_overlaps


def test_default_template_has_no_node_overlaps() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    assert find_overlaps(flow.to_layout(), padding=8) == []
