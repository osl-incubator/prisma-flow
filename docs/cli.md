# CLI

Validate a JSON file:

```bash
prisma-flow validate review.json
```

Render a diagram:

```bash
prisma-flow render review.json --format svg --output prisma.svg
prisma-flow render review.json -f html -o prisma.html
prisma-flow render review.json -f mermaid -o prisma.mmd
```

When `--format` is omitted, the CLI infers the format from `--output` and
defaults to SVG.
