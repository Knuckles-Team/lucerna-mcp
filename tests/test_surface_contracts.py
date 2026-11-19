"""Connector surface: tool-use contracts and ontology roll-up (CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002)."""

import json
import re
from pathlib import Path

import pytest

from lucerna_mcp.connector_contracts import CONTRACTS, LINKS

PACKAGE = Path(__file__).resolve().parents[1] / "lucerna_mcp"
CORE_PREFIX = "@prefix core: <https://knuckles-team.github.io/ontology/core#> ."
KNN_TOOLS = ("opensearch_knn_search", "lucerna_knn_search")


@pytest.mark.spec("CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002")
def test_every_ontology_class_rolls_up_to_core() -> None:
    text = (PACKAGE / "ontology" / "opensearch.ttl").read_text(encoding="utf-8")
    assert CORE_PREFIX in text and "owl:imports" not in text
    blocks = re.findall(r"^:(\w+) a owl:Class ;(.*?) \.$", text, re.S | re.M)
    assert {name for name, _ in blocks} == {"SearchIndex", "SearchAlias", "IndexingRun"}
    for name, body in blocks:
        assert re.search(r"rdfs:subClassOf core:\w+", body), name


@pytest.mark.spec("CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002")
def test_knn_search_tools_are_in_a_contract_a_link_and_the_search_prompts() -> None:
    steps = {step.tool for contract in CONTRACTS for step in contract.steps}
    linked = {tool for link in LINKS for tool in link.tools}
    for tool in KNN_TOOLS:
        assert tool in steps and tool in linked, tool
    for name in ("lucerna-mcp-operator", "lucerna-mcp-search-analyst"):
        prompt = json.loads(
            (PACKAGE / "prompts" / f"{name}.json").read_text(encoding="utf-8")
        )
        assert set(KNN_TOOLS) <= set(prompt["agent"]["tools"]), name
