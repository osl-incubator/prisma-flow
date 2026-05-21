# prisma-flow

`prisma-flow` generates PRISMA-style flow diagrams for evidence synthesis
workflows without mandatory system dependencies.

The default renderer is a pure-Python, template-based SVG renderer. JSON, SVG,
HTML, and Mermaid output work with the base install.

## Install

```bash
pip install prisma-flow
```

or:

```bash
uv add prisma-flow
```

## Quick example

```bash
prisma-flow render examples/basic_new_review.json -o prisma.svg
```
