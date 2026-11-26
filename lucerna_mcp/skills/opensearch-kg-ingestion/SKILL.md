---
name: opensearch-kg-ingestion
skill_type: skill
description: >-
  Trigger a rebuild of the OpenSearch (CA-50) index from current KG state via the lucerna-mcp reindex-trigger tool, which records an :IndexingRun and returns a run id. Use after KG mutations. Do NOT use for index admin (opensearch-index-operations) or querying (opensearch-search).
license: MIT
tags: [opensearch, search, kg, ingest, mcp]
metadata:
  author: Knuckles-Team
  version: '0.2.0'
---
# OpenSearch KG Ingestion (Reindex Trigger)

Scope: Trigger a rebuild of the OpenSearch (CA-50) search index from the current KG state via the lucerna-mcp MCP server's Wire-First reindex-trigger tool. Records an :IndexingRun node and returns a run id immediately — it does NOT walk the graph or write to OpenSearch itself (CA-24 performs the actual rebuild). Use when the agent must ask for the search index to be refreshed after KG mutations. Do NOT use for reading/administering the index directly (use opensearch-index-operations) or for querying it (use opensearch-search).

Records a reindex REQUEST as a durable `:IndexingRun` node through the
required `native_ingest` (Wire-First / `ApplyChangeEnvelope`) authority —
never a bespoke write path, and never a bulk walk of OpenSearch's own
content back into the KG (the index is a derived, rebuildable projection of
the KG per DEC-CA-01 — ingesting a derived copy into its own source of truth
would be backwards).

## When to use
- Ask for the search index to be rebuilt/refreshed after KG mutations that
  should be reflected in search results.
- Kick off a full rebuild from offset 0 — always safe, because the index is
  fully derived and rebuildable (DEC-CA-01).

## When NOT to use
- Reading/administering the index directly → `opensearch-index-operations`.
- Querying the index → `opensearch-search`.
- Expecting this tool to perform the reindex synchronously — it never does;
  CA-24's own CDC-fed indexer performs the actual walk-and-index. This tool's
  contract is satisfied entirely by the request being durably recorded.

## Prerequisites & environment
Same delegated-auth requirements as every other tool in this package
(`OPENSEARCH_URL`, `ENABLE_DELEGATION`/`OIDC_CONFIG_URL`/`OIDC_CLIENT_ID`/
`OIDC_CLIENT_SECRET_REF`). No additional KG-side credentials — the `:IndexingRun`
write runs through the process-owned `GraphComputeEngine` authority via
`native_ingest.ingest_entities`.

## Steps

1. Choose the `index_pattern` argument for the indices to refresh. Verify it is non-empty and names only the index family affected by the KG mutations.
2. Call `opensearch_reindex_from_kg`(index_pattern). Verify the response carries `run_id`, `status: "requested"` and `node_id`.
3. Record the returned `run_id` with the request. Verify `requested_at` and `requested_by` are present. Verify this proves the :IndexingRun node was written.
4. Check rebuild progress on CA-24's own status surface with `opensearch_search`(index, query) against the target index. Verify new documents appear, since this tool never reports completion.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| `NativeIngestError` raised | The engine authority was unavailable, so nothing was recorded | Restore the engine connection for the `lucerna-mcp` server and call `opensearch_reindex_from_kg` again for the same pattern |
| No `run_id` returned | The write was not acknowledged | Treat the request as not recorded and resubmit with the same `index_pattern` |
| Search results still stale | The rebuild is performed asynchronously by CA-24 | Check the run on CA-24's status surface before searching with `opensearch_search` |

## Tool

`opensearch_reindex_from_kg(index_pattern)` — records:

```
:IndexingRun {runId, indexPattern, status: "requested", requestedAt, requestedBy}
```

and returns `{run_id, index_pattern, status, requested_at, node_id}`
immediately. Never partially commits — `NativeIngestError` propagates rather
than silently acking a failed write, so a returned `run_id` can be trusted to
really have been recorded.

## Failure modes to expect
- The engine authority being unavailable raises `NativeIngestError`, not a
  quiet no-op — a caller never gets back a `run_id` for a request that wasn't
  actually recorded.
- This tool never returns reindex PROGRESS or completion status — polling
  the actual rebuild is CA-24's own status surface, cross-lane, read-only
  from here.
