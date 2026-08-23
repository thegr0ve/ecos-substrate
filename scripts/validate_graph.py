#!/usr/bin/env python3
"""
Validates the graph substrate:
  1. Every Markdown file under entities/ and relationships/ has YAML
     frontmatter with required fields (type, title, description, tags).
  2. `type` matches a declared entity_type in schema/schema.yaml.
  3. Every `depends_on` relative path resolves to an existing file
     (no dangling edges / orphaned references).

Run locally: python scripts/validate_graph.py
"""
import sys
import re
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "schema.yaml"
CONTENT_DIRS = ["entities", "relationships"]
REQUIRED_FIELDS = ["type", "title", "description", "tags"]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def load_schema_types():
    if not SCHEMA_PATH.exists():
        return set()
    data = yaml.safe_load(SCHEMA_PATH.read_text())
    return {e["name"] for e in data.get("entity_types", [])}


def find_markdown_files():
    files = []
    for d in CONTENT_DIRS:
        p = ROOT / d
        if p.exists():
            files.extend(p.rglob("*.md"))
    return [f for f in files if f.name != "README.md"]


def validate_file(path, valid_types, errors):
    text = path.read_text()
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter block")
        return
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as e:
        errors.append(f"{path}: invalid YAML frontmatter ({e})")
        return

    for field in REQUIRED_FIELDS:
        if field not in meta:
            errors.append(f"{path}: missing required field '{field}'")

    node_type = meta.get("type")
    if valid_types and node_type and node_type not in valid_types:
        errors.append(f"{path}: type '{node_type}' not declared in schema/schema.yaml")

    for dep in meta.get("depends_on", []) or []:
        dep_path = (path.parent / dep).resolve()
        if not dep_path.exists():
            errors.append(f"{path}: depends_on target does not exist: {dep}")


def main():
    valid_types = load_schema_types()
    errors = []
    files = find_markdown_files()
    for f in files:
        validate_file(f, valid_types, errors)

    if errors:
        print(f"Graph validation failed with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"Graph validation passed ({len(files)} node file(s) checked).")


if __name__ == "__main__":
    main()
