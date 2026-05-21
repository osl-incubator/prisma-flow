"""Optional YAML input/output helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol

from prismaflow.exceptions import OptionalDependencyError
from prismaflow.models import PrismaFlow


class _YamlModule(Protocol):
    """Minimal PyYAML module protocol used by prisma-flow."""

    def safe_load(self, stream: str) -> Any:
        """Load YAML text."""
        ...

    def safe_dump(self, data: Any, *, sort_keys: bool = ...) -> str:
        """Dump data as YAML text."""
        ...


def _yaml_module() -> _YamlModule:
    try:
        import yaml  # type: ignore[import-untyped]
    except ModuleNotFoundError as exc:
        raise OptionalDependencyError(
            "YAML support requires the optional dependency.\n\n"
            "Install it with:\n\n"
            '  pip install "prisma-flow[yaml]"\n\n'
            "or:\n\n"
            '  uv add "prisma-flow[yaml]"'
        ) from exc
    module: _YamlModule = yaml
    return module


def load_yaml(source: str | Path) -> PrismaFlow:
    """Load a PrismaFlow model from a YAML file path or YAML string."""
    yaml = _yaml_module()
    if isinstance(source, Path) or _looks_like_path(source):
        path = Path(source)
        if path.exists():
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            return PrismaFlow.model_validate(data)
    data = yaml.safe_load(str(source))
    return PrismaFlow.model_validate(data)


def dump_yaml(flow: PrismaFlow, path: str | Path | None = None) -> str:
    """Serialize a flow to YAML and optionally write it."""
    yaml = _yaml_module()
    data = flow.model_dump(mode="json")
    output = yaml.safe_dump(data, sort_keys=False)
    if path is not None:
        Path(path).write_text(output, encoding="utf-8")
    return output


def _looks_like_path(source: str | Path) -> bool:
    if isinstance(source, Path):
        return True
    text = str(source)
    return text.endswith((".yaml", ".yml")) or "/" in text or "\\" in text
