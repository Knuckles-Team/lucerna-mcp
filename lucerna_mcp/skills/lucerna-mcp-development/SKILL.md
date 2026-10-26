---
name: lucerna-mcp-development
skill_type: skill
domain: development
description: >-
  Develop, test, gate, and release the lucerna-mcp OpenSearch connector. Use
  this skill when changing its API client, MCP tools, packaged content,
  documentation, or repository gates.
license: MIT
tags: [opensearch, lucerna, development, connector, test, gates]
tier: repository
metadata:
  author: Genius
  version: '0.1.0'
---

# lucerna-mcp development

This repository owns the Lucerna OpenSearch client, action-routed MCP tools,
connector content, ontology mappings, and source declarations for the CA-50
search tier. Shared MCP contracts, transports, delegated authentication, and
source-ingest clients belong to `agent-connector-sdk`; admission, serving, and
durable graph state belong to their owning repositories. Read `AGENTS.md`
before changing code. Keep OpenSearch URLs, tenant identifiers, credentials,
index names, raw documents, and private responses out of source, logs,
fixtures, and packaged skill content.

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver small, reviewable slices and cite the
owning spec row in the commit trailer.

- Find the owning row first with `git grep -n "<term>" -- specs`; extend the
  existing spec before adding requirement text. `CONN-LUCERNA-MCP-CONNECTOR-CONTENT`
  owns the packaged connector content contract.
- Reuse the SDK `Connector` entry point in `lucerna_mcp/__init__.py`, the one
  client factory in `lucerna_mcp/auth.py`, and the registration functions in
  `lucerna_mcp/mcp_server.py`, `lucerna_mcp/mcp/mcp_opensearch.py`, and
  `lucerna_mcp/kg_ingest.py`. Do not create a second connector entry point,
  transport, graph-write path, or parallel policy.
- Preserve the OpenSearch API boundary in `lucerna_mcp/api_client.py` and
  `lucerna_mcp/api/`, including the index, alias, settings, rollover, BM25,
  kNN, hybrid-search, ingest-pipeline, DLS-bundle, and trigger-only KG
  operations. Keep `lucerna_mcp/ontology/opensearch.ttl`,
  `lucerna_mcp/ontology/mappings/source.yaml`, and connector-source metadata
  authoritative for ontology and source mappings.
- Every OpenSearch request runs under the calling principal's bearer token.
  `get_client` is the only client factory and intentionally has no fixed or
  service-credential fallback. Preserve TLS profile resolution through
  `OPENSEARCH_TLS_PROFILE` and `OPENSEARCH_TLS_PROFILE_REF` and the delegated
  audience in `OPENSEARCH_KEYCLOAK_CLIENT_ID`.
- Preserve the condensed and verbose SDK tool surfaces and their intent mode.
  Runtime inputs include `OPENSEARCH_URL`, `OPENSEARCHTOOL`, `MCP_TOOL_MODE`,
  `MCP_ENABLED_TOOLS`, `MCP_DISABLED_TOOLS`, `MCP_ENABLED_TAGS`,
  `MCP_DISABLED_TAGS`, `OIDC_CONFIG_URL`, `OIDC_CLIENT_ID`,
  `OIDC_CLIENT_SECRET_REF`, and `ENABLE_DELEGATION`; never package private
  endpoint or credential defaults.
- Bind delivered behavior to a focused test. Generated `specs/*/status.json`
  files come from the shared hooks; never hand-edit them. Keep
  `skills/**`, `ontology/**`, `connectors/**`, prompts, and both MCP config
  files in the package-data contract.
- Put `Spec: <ID>` and the assisting-agent trailer on consecutive final
  commit-message lines. Review the complete diff and stage only the reviewed
  paths; do not use `git stash`, `git add -A`, `git add .`, or force-push.

## Setup and gates

Use the pinned environment and shared gates from the checkout root:

```bash
uv sync --locked
uvx pre-commit run --all-files
```

For focused feedback, use the tests that exercise the actual Lucerna paths:

```bash
uv run --locked --extra test pytest tests/test_publication_workflow.py -q
uv run --locked --extra test pytest tests/test_api_client.py tests/test_auth_env.py -q
uv run --locked --extra test pytest tests/test_dls_bundle.py tests/test_kg_ingest.py -q
uv run --locked --extra test pytest tests/test_search.py tests/test_startup.py -q
```

Tests use fakes and local fixtures. Do not call a live OpenSearch endpoint or
require credentials in local gates. Preserve delegated OIDC authentication,
TLS trust policy, calling-principal DLS enforcement, action validation,
trigger-only KG ingestion, tool toggles, tool modes, and ontology/source
mappings when changing client or tool modules.

## Packaging and publication

Build with `uv build` and inspect the wheel and sdist for
`lucerna_mcp/skills/lucerna-mcp-development/SKILL.md`. Keep the project version
and `uv.lock` aligned for a genuine content release. The canonical Pages
publisher is `.github/workflows/pages.yml`, which calls the shared pipelines
workflow with `.config/spec-dashboard.json`; keep `workflow_dispatch` and do
not add another documentation publisher. The generated dashboard reads
`specs/*/status.json` and is published at `spec-delivery/`.

The release workflow is `.github/workflows/pipeline.yml`: its Python reusable
workflow uses `connector: true`, and its container reusable workflow uses
`render_connector: true` after PyPI publication. Verify an exact-source Pages
workflow, the public dashboard, and the packaged skill in the public wheel and
sdist before claiming publication.
