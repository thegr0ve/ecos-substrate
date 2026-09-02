#!/usr/bin/env python3
"""
Validates the graph substrate:
  1. Every Markdown file under entities/ and relationships/ has YAML
     frontmatter with required fields (type, title, description, tags,
     depends_on, timestamp) — per docs/GRAPH_CONVENTIONS.md and AGENTS.md.
  2. `type` matches a declared entity_type in schema/schema.yaml.
  3. Every `depends_on` relative path resolves to an existing file
     (no dangling edges / orphaned references).
  4. `timestamp` is a strict ISO-8601 UTC timestamp (YYYY-MM-DDTHH:MM:SSZ).
  5. config/graphrag.settings.template.yaml:entity_types, once populated,
     does not silently drift from schema/schema.yaml:entity_types.

Fails closed: if schema/schema.yaml is missing or fails to parse, this is
treated as a hard configuration error (exit 2) rather than silently
skipping type validation.

Run locally: python scripts/validate_graph.py
"""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "schema.yaml"
GRAPHRAG_SETTINGS_PATH = ROOT / "config" / "graphrag.settings.template.yaml"
CONTENT_DIRS = ["entities", "relationships"]
REQUIRED_FIELDS = ["type", "title", "description", "tags", "depends_on", "timestamp"]

# Tolerates a leading UTF-8 BOM (stripped before matching) and CRLF line
# endings (normalized to LF before matching) — see _read_text().
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

# Strict ISO-8601 UTC timestamp, matching the convention documented in
# docs/GRAPH_CONVENTIONS.md: YYYY-MM-DDTHH:MM:SSZ
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PASCAL_CASE_RE = re.compile(r"^[A-Z][A-Za-z0-9]*$")
SNAKE_CASE_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")


class SchemaConfigError(Exception):
    """Raised when schema/schema.yaml is missing or unparsable.

    This is a hard configuration failure (fail closed), distinct from a
    validly-parsed schema that simply declares zero entity_types.
    """


def _read_text(path: Path) -> str:
    """Read a file as UTF-8, tolerating a leading BOM, and normalize CRLF."""
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("\ufeff"):
        raw = raw[1:]
    return raw.replace("\r\n", "\n")


def load_schema():
    """Load schema/schema.yaml, failing closed on missing/unparsable schema."""
    if not SCHEMA_PATH.exists():
        raise SchemaConfigError(f"{SCHEMA_PATH} does not exist")
    try:
        text = _read_text(SCHEMA_PATH)
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise SchemaConfigError(f"{SCHEMA_PATH} is not valid YAML: {e}")
    if data is None or not isinstance(data, dict):
        raise SchemaConfigError(f"{SCHEMA_PATH} did not parse to a mapping")
    return data


def load_schema_type_names(schema_data):
    """Return declared entity names after validating both type vocabularies."""
    vocabularies = (
        ("entity_types", PASCAL_CASE_RE, "PascalCase"),
        ("relation_types", SNAKE_CASE_RE, "snake_case"),
    )
    resolved = {}
    for key, naming_pattern, naming_label in vocabularies:
        entries = schema_data.get(key)
        if not isinstance(entries, list):
            raise SchemaConfigError(f"{SCHEMA_PATH}: {key} must be a list")

        names = []
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                raise SchemaConfigError(
                    f"{SCHEMA_PATH}: {key}[{index}] must be a mapping"
                )
            name = entry.get("name")
            if not isinstance(name, str) or not naming_pattern.fullmatch(name):
                raise SchemaConfigError(
                    f"{SCHEMA_PATH}: {key}[{index}].name must use {naming_label}"
                )
            names.append(name)

        if len(names) != len(set(names)):
            raise SchemaConfigError(f"{SCHEMA_PATH}: {key} contains duplicate names")
        resolved[key] = set(names)

    return resolved["entity_types"], resolved["relation_types"]


def find_markdown_files():
    files = []
    for d in CONTENT_DIRS:
        p = ROOT / d
        if p.exists():
            files.extend(p.rglob("*.md"))
    return [f for f in files if f.name != "README.md"]


def validate_timestamp(value):
    if not isinstance(value, str) or not TIMESTAMP_RE.match(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return False
    return True


def validate_file(path, valid_types, errors):
    try:
        text = _read_text(path)
    except UnicodeDecodeError as e:
        errors.append(f"{path}: could not read as UTF-8 ({e})")
        return

    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter block")
        return
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as e:
        errors.append(f"{path}: invalid YAML frontmatter ({e})")
        return

    if not isinstance(meta, dict):
        errors.append(f"{path}: frontmatter did not parse to a mapping")
        return

    for field in REQUIRED_FIELDS:
        if field not in meta:
            errors.append(f"{path}: missing required field '{field}'")

    node_type = meta.get("type")
    if node_type is not None and node_type not in valid_types:
        errors.append(f"{path}: type '{node_type}' not declared in schema/schema.yaml")

    timestamp = meta.get("timestamp")
    if timestamp is not None and not validate_timestamp(timestamp):
        errors.append(
            f"{path}: timestamp '{timestamp}' is not a valid ISO-8601 UTC "
            "timestamp (expected YYYY-MM-DDTHH:MM:SSZ)"
        )

    dependencies = meta.get("depends_on")
    if dependencies is not None and not isinstance(dependencies, list):
        errors.append(f"{path}: depends_on must be a list of relative paths")
        return

    for dep in dependencies or []:
        if not isinstance(dep, str) or not dep.strip():
            errors.append(f"{path}: depends_on entries must be non-empty strings")
            continue
        dep_value = Path(dep)
        if dep_value.is_absolute():
            errors.append(f"{path}: depends_on target must be relative: {dep}")
            continue
        dep_path = (path.parent / dep_value).resolve()
        try:
            dep_path.relative_to(ROOT.resolve())
        except ValueError:
            errors.append(f"{path}: depends_on target escapes repository: {dep}")
            continue
        if not dep_path.is_file():
            errors.append(f"{path}: depends_on target does not exist: {dep}")


def check_graphrag_drift(schema_entity_type_names, errors):
    """Fail if the GraphRAG config's entity_types have been populated but
    have drifted from schema/schema.yaml:entity_types.

    An empty (unpopulated) list in the config is not an error — see
    config/graphrag.settings.template.yaml's own header comment, which
    documents it as intentionally inactive until extraction begins.
    """
    if not GRAPHRAG_SETTINGS_PATH.exists():
        return
    try:
        text = _read_text(GRAPHRAG_SETTINGS_PATH)
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError as e:
        errors.append(f"{GRAPHRAG_SETTINGS_PATH}: invalid YAML ({e})")
        return

    extract_graph = data.get("extract_graph") or {}
    configured = extract_graph.get("entity_types") or []
    if not configured:
        return

    configured_names = set(configured)
    if configured_names != schema_entity_type_names:
        missing = schema_entity_type_names - configured_names
        extra = configured_names - schema_entity_type_names
        detail = []
        if missing:
            detail.append(f"missing from config: {sorted(missing)}")
        if extra:
            detail.append(f"not declared in schema: {sorted(extra)}")
        errors.append(
            f"{GRAPHRAG_SETTINGS_PATH}: extract_graph.entity_types has drifted "
            f"from schema/schema.yaml:entity_types ({'; '.join(detail)})"
        )


def main():
    try:
        schema_data = load_schema()
        valid_types, _relation_types = load_schema_type_names(schema_data)
    except SchemaConfigError as e:
        print(f"Graph validation failed: {e}")
        print("schema/schema.yaml must exist and parse cleanly (fail-closed).")
        sys.exit(2)

    errors = []
    files = find_markdown_files()
    for f in files:
        validate_file(f, valid_types, errors)

    check_graphrag_drift(valid_types, errors)

    if errors:
        print(f"Graph validation failed with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"Graph validation passed ({len(files)} node file(s) checked).")


if __name__ == "__main__":
    main()
