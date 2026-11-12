# Changelog

All notable changes to `lucerna-mcp` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.9] - 2026-11-12

### Removed
- The vector and hybrid search tools (`opensearch_knn_search`, `opensearch_hybrid_search`, `opensearch_knn_plugin_enabled` and their `lucerna_` operation names), the client methods behind them and the `LUCERNA_KNN_ENABLED` switch. The graph engine holds native vectors; OpenSearch text (BM25) search stays.

## [0.3.8] - 2026-11-12

### Changed
- The connector declares its whole surface: tool-use contracts, links, data location, business roles, operator and role prompts, and a data resource. `SearchAlias` rolls up to a core class.
- `opensearch_ingest_pipeline` (an `action` router) is replaced by `opensearch_ingest_pipeline_get` and `opensearch_ingest_pipeline_put`.
- Remove the unresolvable `scion_sdk.prompt_providers` entry point; require `scion-sdk>=0.9.0,<1.0.0`.

## [0.3.7] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [0.3.5] - 2026-10-26

### Added
- Canonical spec-delivery Pages dashboard wiring and the packaged
  `lucerna-mcp-development` contributor skill.

## [0.3.4] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.4`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [Unreleased]

## [0.3.0] - 2026-10-18

### Changed
- Renamed from opensearch-mcp to lucerna-mcp (PyPI distribution, import package
  `lucerna_mcp`, CLI `lucerna-mcp`, Docker image `knucklessg1/lucerna-mcp`, GitHub
  repository). The `OPENSEARCH_*` environment variables name the OpenSearch system
  and are unchanged. Spec IDs keep the `CONN-OPENSEARCH-MCP` prefix.
- agent-connector-sdk 0.3.6 floor: per-operation tools are `lucerna_<operation>`.

## [0.1.0] - 2026-08-26

### Added
- Initial release: MCP server, A2A agent, and API client for OpenSearch
  (the CA-50 search tier) integration — index/alias/settings administration,
  BM25/kNN/hybrid search, ingest pipelines, and document-level-security (DLS)
  policy bundle application.
- Connector capability certification bundle (`connector_manifest.yml`,
  ontology, KG ingestion).
- Standard fleet scaffolding (CI workflows, pre-commit, docs site, packaging
  metadata) to bring the repo to parity with the rest of the agent-packages
  fleet.

### Fixed
- Env-var drift: `OIDC_CLIENT_SECRET_REF`, not `OIDC_CLIENT_SECRET`.
