"""
Pytest fixtures/tests for scripts/validate_graph.py.

Covers: valid node, missing required field, invalid type, dangling
depends_on, malformed timestamp, CRLF line endings, UTF-8 BOM, and a
missing/unparsable schema/schema.yaml (fail-closed behavior), plus the
GraphRAG entity_types drift check.

Each test builds an isolated fake repo under tmp_path (with its own
entities/, relationships/, schema/schema.yaml, config/) and monkeypatches
the module-level path constants so validate_graph never touches the real
repository.
"""
import sys
from pathlib import Path

import pytest

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import validate_graph  # noqa: E402


VALID_SCHEMA = """\
entity_types:
  - name: "Entity"
    description: "Root entity type."
    required_frontmatter: ["type", "title", "description", "tags"]
"""

VALID_FRONTMATTER = """\
---
type: "Entity"
title: "Test Node"
description: "A test node."
tags: ["test"]
depends_on: []
timestamp: "2026-08-24T00:00:00Z"
---
Body text.
"""


@pytest.fixture
def repo(tmp_path, monkeypatch):
    (tmp_path / "schema").mkdir()
    (tmp_path / "entities").mkdir()
    (tmp_path / "relationships").mkdir()
    (tmp_path / "config").mkdir()
    (tmp_path / "schema" / "schema.yaml").write_text(VALID_SCHEMA, encoding="utf-8")

    monkeypatch.setattr(validate_graph, "ROOT", tmp_path)
    monkeypatch.setattr(validate_graph, "SCHEMA_PATH", tmp_path / "schema" / "schema.yaml")
    monkeypatch.setattr(
        validate_graph,
        "GRAPHRAG_SETTINGS_PATH",
        tmp_path / "config" / "graphrag.settings.template.yaml",
    )
    return tmp_path


def write_node(repo, name, content, newline=None):
    path = repo / "entities" / name
    if newline == "crlf":
        content = content.replace("\n", "\r\n")
    path.write_bytes(content.encode("utf-8"))
    return path


def test_valid_node_passes(repo):
    write_node(repo, "valid.md", VALID_FRONTMATTER)
    schema_data = validate_graph.load_schema()
    valid_types = validate_graph.load_schema_entity_type_names(schema_data)
    errors = []
    validate_graph.validate_file(repo / "entities" / "valid.md", valid_types, errors)
    assert errors == []


def test_missing_required_field(repo):
    bad = VALID_FRONTMATTER.replace('tags: ["test"]\n', "")
    write_node(repo, "missing_field.md", bad)
    schema_data = validate_graph.load_schema()
    valid_types = validate_graph.load_schema_entity_type_names(schema_data)
    errors = []
    validate_graph.validate_file(repo / "entities" / "missing_field.md", valid_types, errors)
    assert any("missing required field 'tags'" in e for e in errors)


def test_invalid_type(repo):
    bad = VALID_FRONTMATTER.replace('type: "Entity"', 'type: "NotDeclared"')
    write_node(repo, "invalid_type.md", bad)
    schema_data = validate_graph.load_schema()
    valid_types = validate_graph.load_schema_entity_type_names(schema_data)
    errors = []
    validate_graph.validate_file(repo / "entities" / "invalid_type.md", valid_types, errors)
    assert any("not declared in schema/schema.yaml" in e for e in errors)


def test_dangling_depends_on(repo):
    bad = VALID_FRONTMATTER.replace("depends_on: []", 'depends_on: ["./does-not-exist.md"]')
    write_node(repo, "dangling.md", bad)
    schema_data = validate_graph.load_schema()
    valid_types = validate_graph.load_schema_entity_type_names(schema_data)
    errors = []
    validate_graph.validate_file(repo / "entities" / "dangling.md", valid_types, errors)
    assert any("depends_on target does not exist" in e for e in errors)


def test_malformed_timestamp(repo):
    bad = VALID_FRONTMATTER.replace(
        'timestamp: "2026-08-24T00:00:00Z"', 'timestamp: "08/24/2026"'
    )
    write_node(repo, "bad_timestamp.md", bad)
    schema_data = validate_graph.load_schema()
    valid_types = validate_graph.load_schema_entity_type_names(schema_data)
    errors = []
    validate_graph.validate_file(repo / "entities" / "bad_timestamp.md", valid_types, errors)
    assert any("not a valid ISO-8601" in e for e in errors)


def test_crlf_file_is_tolerated(repo):
    path = write_node(repo, "crlf.md", VALID_FRONTMATTER, newline="crlf")
    schema_data = validate_graph.load_schema()
    valid_types = validate_graph.load_schema_entity_type_names(schema_data)
    errors = []
    validate_graph.validate_file(path, valid_types, errors)
    assert errors == []


def test_bom_file_is_tolerated(repo):
    path = repo / "entities" / "bom.md"
    path.write_bytes(b"\xef\xbb\xbf" + VALID_FRONTMATTER.encode("utf-8"))
    schema_data = validate_graph.load_schema()
    valid_types = validate_graph.load_schema_entity_type_names(schema_data)
    errors = []
    validate_graph.validate_file(path, valid_types, errors)
    assert errors == []


def test_missing_schema_fails_closed(repo):
    (repo / "schema" / "schema.yaml").unlink()
    with pytest.raises(validate_graph.SchemaConfigError):
        validate_graph.load_schema()


def test_unparsable_schema_fails_closed(repo):
    (repo / "schema" / "schema.yaml").write_text(":\n  - not: [valid", encoding="utf-8")
    with pytest.raises(validate_graph.SchemaConfigError):
        validate_graph.load_schema()


def test_graphrag_drift_detected(repo):
    (repo / "config" / "graphrag.settings.template.yaml").write_text(
        'extract_graph:\n  entity_types: ["SomethingElse"]\n', encoding="utf-8"
    )
    schema_data = validate_graph.load_schema()
    valid_types = validate_graph.load_schema_entity_type_names(schema_data)
    errors = []
    validate_graph.check_graphrag_drift(valid_types, errors)
    assert any("has drifted" in e for e in errors)


def test_graphrag_empty_entity_types_is_not_drift(repo):
    (repo / "config" / "graphrag.settings.template.yaml").write_text(
        "extract_graph:\n  entity_types: []\n", encoding="utf-8"
    )
    schema_data = validate_graph.load_schema()
    valid_types = validate_graph.load_schema_entity_type_names(schema_data)
    errors = []
    validate_graph.check_graphrag_drift(valid_types, errors)
    assert errors == []
