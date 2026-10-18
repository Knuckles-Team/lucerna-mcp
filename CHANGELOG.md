# Changelog

All notable changes to `lucerna-mcp` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
