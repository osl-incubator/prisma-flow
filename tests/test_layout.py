from prismaflow import PrismaFlow
from prismaflow.layout import DiagramLayout, Rect


def test_rect_anchor_properties() -> None:
    rect = Rect(10, 20, 100, 50)
    assert rect.center_x == 60
    assert rect.center_y == 45
    assert rect.top_center.y == 20
    assert rect.bottom_center.y == 70
    assert rect.left_center.x == 10
    assert rect.right_center.x == 110


def test_layout_contains_expected_nodes() -> None:
    flow = PrismaFlow.from_json("examples/basic_new_review.json")
    layout = flow.to_layout()
    assert isinstance(layout, DiagramLayout)
    assert layout.node_by_id("identified").text.startswith("Records identified")
    assert layout.node_by_id("included").text.startswith("Studies included")
