# CONN-LUCERNA-MCP-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `lucerna-mcp` as the single `scion_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Proving test: `tests/test_default_content_surfaces.py`. Caller chain: the scion_sdk.connector entry point lucerna-mcp in pyproject.toml resolves to lucerna_mcp/__init__.py::connector (line 89), which the lucerna-mcp console script (scion_sdk.cli:serve) serves; packaged content lives in lucerna_mcp/skills and lucerna_mcp/ontology, and the scion_sdk.prompt_providers entry point names lucerna_mcp.prompts. Shape: serve the packaged skills, ontology and prompts through scion_sdk.mcp.content.ConnectorContent.for_package with no content= argument; lucerna_mcp/prompts is declared in pyproject.toml but absent from the tree, and no content test exists, so add one beside tests/test_startup.py. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Planned test: `tests/test_default_content_surfaces.py::test_default_content_surfaces`. |
