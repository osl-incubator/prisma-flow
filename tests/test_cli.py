from pathlib import Path

from prismaflow.cli import main


def test_cli_validate_passes(capsys) -> None:  # type: ignore[no-untyped-def]
    exit_code = main(["validate", "examples/basic_new_review.json"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Validation passed" in captured.out


def test_cli_render_svg(tmp_path: Path) -> None:
    output = tmp_path / "prisma.svg"
    exit_code = main(["render", "examples/basic_new_review.json", "-o", str(output)])
    assert exit_code == 0
    assert output.read_text(encoding="utf-8").startswith("<?xml")


def test_cli_png_reports_optional_dependency(capsys) -> None:  # type: ignore[no-untyped-def]
    exit_code = main(
        [
            "render",
            "examples/basic_new_review.json",
            "--format",
            "png",
            "--output",
            "prisma.png",
        ]
    )
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "prisma-flow[png]" in captured.err
