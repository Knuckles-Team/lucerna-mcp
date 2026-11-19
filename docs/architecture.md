# Architecture

## Layers

## The calling-principal invariant, structurally

`api/api_client_base.py`'s `_PerCallBearerAuth` is a `requests.auth.AuthBase`
callable. `opensearchpy.RequestsHttpConnection.__init__` assigns whatever is
passed as `http_auth` directly to `requests.Session.auth` (verified against
opensearch-py 3.2.0's own source). `requests` invokes an `AuthBase.__call__`
on every single prepared request — not once at session construction — so a
token that expires mid-session, or a caller whose identity changes between
two tool calls in the same process, is never silently reused.

`auth.py`'s `get_client()` is the ONLY place that builds an
`OpenSearchApi`. It has no parameter that accepts an override credential, and
no fallback: if OIDC delegation isn't enabled or the RFC 8693 token exchange
fails, it raises `OpenSearchApiError` rather than returning something that
will still work but silently bypass DLS. This is a deliberate divergence
from the fleet's usual delegated-auth pattern (`gitlab-api`/`twenty-mcp` fall
through to a fixed token on delegation failure) — that fallback is exactly
what this package's security contract forbids.

`OpenSearchApi.__init__` does have a second constructor path,
`_test_basic_auth`, used ONLY by this package's own live-proof tests against
the pre-bundle DLS demonstration accounts (`ca-e2e`/`restricted-viewer`,
documented in `services/opensearch/AGENTS.md`). It is never imported by
`auth.py` or by any `mcp/*.py` tool.

## Vector search

The graph engine holds native vectors, so this connector serves OpenSearch text (BM25) search only and exposes no vector or hybrid tool.

## DLS bundle application, never authored here

`opensearch_apply_dls_bundle` (`mcp/mcp_opensearch.py`) validates a
caller-supplied bundle's shape BEFORE calling
`OpenSearchApi.apply_dls_bundle_rendering` for each entry:

1. `renderings.opensearch` must exist and be a non-empty list.
2. `governs` must be exactly `["M1"]` (DEC-CA-04's contract: a bundle whose
   `governs` this package doesn't recognize is denied).
3. `graph` must be present (a bundle must not be applied to data it wasn't
   generated for).
4. Every rendering entry must carry `index_pattern`/`role`/`dls_query`.

A missing or malformed field raises with a NAMED field error and applies
nothing — this file contains no code path that builds a `dls_query` from
scratch; it only ever forwards the one it was given.

## Reindex trigger, not a reindex

`kg_ingest.py`'s `opensearch_reindex_from_kg` records one `:IndexingRun` node
(via the required `native_ingest.ingest_entities` authority) and returns
immediately with a run id. It never walks the KG or writes to OpenSearch
itself — CA-24's own CDC-fed indexer does that. Because the index is fully
derived/rebuildable (DEC-CA-01), this is always safe to call, including a
full rebuild from offset 0.
