# CONN-LUCERNA-MCP-CONNECTOR-CONTENT — The connector serves its packaged content

Owner: lucerna-mcp. Cross-repo IDs: `SCION-CONNECTOR-CONTROL-R071`, `SCION-CONNECTOR-CONTROL-R073`.

## Purpose and user stories

The `lucerna-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

## Why a new spec

The specs of this repository were read; none owns this capability. This spec states it for this connector only.

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: the SDK modules and the engine, which own the shared capabilities.

## User Scenarios & Testing

### User Story 1 - The connector serves its packaged content (Priority: P1)

The `lucerna-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R001` (default content) is exercised, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.

### User Story 2 - The connector surface is complete (Priority: P2)

The fleet and the business agents rely on `lucerna-mcp` declaring its whole surface: an ontology that rolls up to the core ontology and tool-use contracts, links and prompts that name every tool.

**Acceptance Scenarios**:

1. **Given** the connector is built from the default branch, **When** the behaviour of row `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002` (surface completeness) is exercised, **Then** every ontology class reaches a core class, and every served tool is in a contract, a link and an agent prompt.

### User Story 3 - Search is text search only (Priority: P2)

The graph engine holds native vectors, so the search tier serves text (BM25) search and no vector or hybrid search.

**Acceptance Scenarios**:

1. **Given** the connector is built from the default branch, **When** the behaviour of row `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R003` (text search only) is exercised, **Then** no vector, hybrid or k-NN plugin tool or client method remains.

### Edge Cases

- If `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R001` is not met, its proving test fails: default content.
- If `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002` is not met, its proving test fails: surface completeness.
- If `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R003` is not met, its proving test fails: text search only.

## Requirements

- **FR-001**: Default content. Rows: `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R001`.
- **FR-002**: Surface completeness. Rows: `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002`.
- **FR-003**: Text search only. Rows: `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R003`.

## Success Criteria

- **SC-001**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R001`.
- **SC-002**: The surface audit reports no gap for the ontology, contracts, links and prompts. Rows: `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002`.
- **SC-003**: No vector, hybrid or k-NN plugin tool or client method is served. Rows: `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R003`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
| FR-003 | `CONN-LUCERNA-MCP-CONNECTOR-CONTENT-R003` | [plan.md](plan.md) | T-003 | [test-spec.md](test-spec.md) |
