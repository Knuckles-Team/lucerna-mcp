# CONN-LUCERNA-MCP-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py` | The listings include the packaged skills, ontology and prompts. |
| T-002 | `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002` | `tests/test_surface_contracts.py` | Every ontology class reaches a core class. |
| T-003 | `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R003` | `tests/test_search.py` | No vector, hybrid or k-NN plugin tool or client method remains. |
