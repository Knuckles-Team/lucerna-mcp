"""Connector surface: tool-use contracts and ontology roll-up (CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002)."""

import json
import re
from pathlib import Path

import pytest

from lucerna_mcp.connector_contracts import CONTRACTS, LINKS

PACKAGE = Path(__file__).resolve().parents[1] / "lucerna_mcp"
CORE_PREFIX = "@prefix core: <https://knuckles-team.github.io/ontology/core#> ."
VECTOR_TOOLS = ("knn_search", "hybrid_search", "knn_plugin_enabled")


@pytest.mark.spec("CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002")
def test_every_ontology_class_rolls_up_to_core() -> None:
    text = (PACKAGE / "ontology" / "opensearch.ttl").read_text(encoding="utf-8")
    assert CORE_PREFIX in text and "owl:imports" not in text
    blocks = re.findall(r"^:(\w+) a owl:Class ;(.*?) \.$", text, re.S | re.M)
    assert {name for name, _ in blocks} == {"SearchAlias"}
    for name, body in blocks:
        assert re.search(r"rdfs:subClassOf core:\w+", body), name


@pytest.mark.spec("CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002")
def test_served_surface_has_no_contract_link_or_prompt_gap() -> None:
    from scion_sdk.testing.surface_check import surface_check

    assert surface_check("lucerna_mcp") == []


@pytest.mark.spec("CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R003")
def test_no_contract_link_or_prompt_names_a_vector_tool() -> None:
    steps = {step.tool for contract in CONTRACTS for step in contract.steps}
    linked = {tool for link in LINKS for tool in link.tools}
    prompted: set[str] = set()
    for path in (PACKAGE / "prompts").glob("*.json"):
        prompted |= set(json.loads(path.read_text(encoding="utf-8"))["agent"]["tools"])
    for name in steps | linked | prompted:
        assert not name.endswith(VECTOR_TOOLS), name
