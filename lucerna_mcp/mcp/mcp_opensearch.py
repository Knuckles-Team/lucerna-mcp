"""Thin MCP wrappers around the OpenSearch API client (CA-50 search tier).

Each tool is a thin shim: it parses params, calls the corresponding
``OpenSearchApi`` method, and returns the result. All API surface lives in
``lucerna_mcp.api`` — these tools add no business logic beyond input
validation and the two invariants this package exists to hold:

1. **Every tool below calls ``lucerna_mcp.auth.get_client()`` and nothing
   else** — there is no second client factory, no ``token=``/``credential=``
   parameter on any tool here that could let a caller (or a future edit)
   route around the calling-principal's own token. This is true of
   ``search`` tools AND of ``opensearch_apply_dls_bundle`` (a privileged
   write that still runs under the caller's own elevated role, never a
   hardcoded admin credential baked into this package — DEC-CA-04 /
   this lane's Authority section).
2. **``opensearch_apply_dls_bundle`` never hand-authors a DLS rule.** It
   validates a caller-supplied CA-16/26-rendered bundle's
   ``renderings.opensearch`` shape and ``governs``/``graph`` fields, then
   applies EXACTLY the ``dls_query`` it was given — this file contains no
   code path that constructs a DLS predicate from scratch.

Four tool groups, per DEC-CA-08 / this lane's contract (all registered by
:func:`register_opensearch_tools`, one ``OPENSEARCHTOOL`` env toggle):
  * index      — create/update/alias/settings/rollover/delete (typed
                 ``OntologyAction``s per DEC-CA-07 once ``ActionSpec`` lands)
  * search     — BM25 text search, always as the calling principal
  * pipelines  — ingest-pipeline get/put
  * security   — DLS rule read (read-only) + bundle apply (write, gated)

The fifth group, ``reindex-from-KG`` (``opensearch_reindex_from_kg``), is
registered separately by ``kg_ingest.py``'s ``register_ingest_tools`` (its
own ``INGESTTOOL`` toggle) — it is a *trigger*, not a search/admin tool.
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from pydantic import Field

from lucerna_mcp.api.api_client_base import OpenSearchApiError
from lucerna_mcp.auth import get_client

_REQUIRED_RENDERING_FIELDS = ("index_pattern", "role", "dls_query")
_RECOGNIZED_GOVERNS = {"M1"}


def _require_bundle_is_object(bundle: Any) -> None:
    """Fail closed if the bundle is not itself a JSON object."""
    if not isinstance(bundle, dict):
        raise OpenSearchApiError("DLS bundle must be a JSON object")


def _extract_opensearch_renderings(bundle: dict[str, Any]) -> list[Any]:
    """Return the bundle's ``renderings.opensearch`` list, or fail closed."""
    renderings = bundle.get("renderings")
    if not isinstance(renderings, dict) or "opensearch" not in renderings:
        raise OpenSearchApiError(
            "malformed DLS bundle: missing required field 'renderings.opensearch'"
        )
    opensearch_renderings = renderings["opensearch"]
    if not isinstance(opensearch_renderings, list) or not opensearch_renderings:
        raise OpenSearchApiError(
            "malformed DLS bundle: 'renderings.opensearch' must be a non-empty list"
        )
    return opensearch_renderings


def _require_recognized_governs(bundle: dict[str, Any]) -> None:
    """DEC-CA-04 Contract: an unrecognized (or missing) ``governs`` denies."""
    governs = bundle.get("governs")
    if not isinstance(governs, list) or not _RECOGNIZED_GOVERNS.issuperset(governs):
        raise OpenSearchApiError(
            f"malformed DLS bundle: unrecognized or missing 'governs' {governs!r} — "
            f"this package only applies bundles governing {sorted(_RECOGNIZED_GOVERNS)}"
        )


def _require_bundle_graph(bundle: dict[str, Any]) -> None:
    """A bundle must not be applied to data it wasn't generated for."""
    if not bundle.get("graph"):
        raise OpenSearchApiError(
            "malformed DLS bundle: missing required field 'graph' — a bundle must "
            "not be applied to data it wasn't generated for"
        )


def _validate_rendering_entries(entries: list[Any]) -> list[dict[str, Any]]:
    """Validate each ``renderings.opensearch`` entry has the required shape."""
    validated: list[dict[str, Any]] = []
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise OpenSearchApiError(
                f"malformed DLS bundle: renderings.opensearch[{i}] is not an object"
            )
        missing = [f for f in _REQUIRED_RENDERING_FIELDS if f not in entry]
        if missing:
            raise OpenSearchApiError(
                f"malformed DLS bundle: renderings.opensearch[{i}] missing "
                f"required field(s) {missing}"
            )
        validated.append(entry)
    return validated


def _validate_dls_bundle(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate a caller-supplied DEC-CA-04 policy bundle's shape.

    Fails closed with a NAMED field error (this lane's explicit negative-test
    requirement) rather than partially applying anything. Returns the
    validated ``renderings.opensearch`` list on success.
    """
    _require_bundle_is_object(bundle)
    opensearch_renderings = _extract_opensearch_renderings(bundle)
    _require_recognized_governs(bundle)
    _require_bundle_graph(bundle)
    return _validate_rendering_entries(opensearch_renderings)


def register_opensearch_tools(mcp: FastMCP) -> None:
    """Register index/search/pipelines/security tools."""

    # ── index admin (typed OntologyActions per DEC-CA-07 — see AGENTS.md for
    #    the ActionSpec-schema blocker status) ────────────────────────────
    @mcp.tool(
        annotations={
            "title": "Create OpenSearch Index",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
        tags={"index", "mutating"},
    )
    async def opensearch_create_index(
        index: str = Field(description="Index name to create."),
        mappings: dict[str, Any] | None = Field(
            default=None, description="Optional mappings.properties dict."
        ),
        settings: dict[str, Any] | None = Field(
            default=None, description="Optional index settings dict."
        ),
    ) -> dict[str, Any]:
        """Create an index. Idempotent: creating an already-existing index
        returns ``already_exists: true`` rather than raising."""
        body: dict[str, Any] = {}
        if mappings:
            body["mappings"] = {"properties": mappings}
        if settings:
            body["settings"] = settings
        return get_client().create_index(index, body or None)

    @mcp.tool(tags={"index", "mutating"})
    async def opensearch_update_mapping(
        index: str = Field(description="Index name."),
        properties: dict[str, Any] = Field(
            description="Field-name -> mapping dict to merge in."
        ),
    ) -> dict[str, Any]:
        """Add/merge field mappings into an existing index (non-destructive)."""
        return get_client().update_mapping(index, properties)

    @mcp.tool(tags={"index", "mutating"})
    async def opensearch_manage_alias(
        actions: list[dict[str, Any]] = Field(
            description=(
                "List of alias actions, e.g. "
                "[{'add': {'index': 'kg-v2', 'alias': 'kg-current'}}, "
                "{'remove': {'index': 'kg-v1', 'alias': 'kg-current'}}]."
            )
        ),
    ) -> dict[str, Any]:
        """Add/remove/swap index aliases in one atomic call."""
        return get_client().manage_alias(actions)

    @mcp.tool(tags={"index"})
    async def opensearch_get_aliases(
        index: str = Field(
            default="*", description="Index or index-pattern to inspect."
        ),
    ) -> dict[str, Any]:
        """List aliases for an index or index-pattern (read-only)."""
        return get_client().get_aliases(index)

    @mcp.tool(tags={"index", "mutating"})
    async def opensearch_update_settings(
        index: str = Field(description="Index name."),
        settings: dict[str, Any] = Field(
            description="Dynamic index settings to apply."
        ),
    ) -> dict[str, Any]:
        """Update an index's dynamic settings (e.g. refresh_interval, replicas)."""
        return get_client().update_settings(index, settings)

    @mcp.tool(
        annotations={
            "title": "Rollover OpenSearch Alias",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": True,
        },
        tags={"index", "mutating"},
    )
    async def opensearch_rollover(
        alias: str = Field(description="Write alias to roll over."),
        conditions: dict[str, Any] | None = Field(
            default=None, description="Rollover conditions (max_age/max_docs/max_size)."
        ),
        new_index: str = Field(
            default="", description="Explicit name for the new index (optional)."
        ),
    ) -> dict[str, Any]:
        """Roll an alias over to a new backing index once conditions are met.

        A typed ``OntologyAction`` per DEC-CA-07 — never auto-triggered by
        this package's own logic (this lane's Authority section)."""
        return get_client().rollover(alias, conditions, new_index or None)

    @mcp.tool(
        annotations={
            "title": "Delete OpenSearch Index",
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": True,
            "openWorldHint": True,
        },
        tags={"index", "mutating"},
    )
    async def opensearch_delete_index(
        index: str = Field(description="Index name to delete."),
    ) -> dict[str, Any]:
        """Delete an index. A typed, destructive ``OntologyAction`` per DEC-CA-07 —
        because the index is fully derived/rebuildable from the KG (DEC-CA-01),
        this carries no data-loss risk to the system of record."""
        return get_client().delete_index(index)

    # ── search (always the calling principal — DLS enforced per-request) ─
    @mcp.tool(tags={"search"})
    async def opensearch_search(
        index: str = Field(description="Index or index-pattern to search."),
        query: dict[str, Any] = Field(description="OpenSearch Query DSL object."),
        size: int = Field(
            default=10, description="Max hits to return (capped at 100)."
        ),
        source_fields: list[str] | None = Field(
            default=None, description="Optional _source field allowlist to project."
        ),
    ) -> dict[str, Any]:
        """BM25 (lexical) search. Runs as the calling principal — any DLS role
        mapped to that principal's OpenSearch backend role filters results
        server-side; this tool never widens or bypasses that filter."""
        return get_client().search(index, query, size=size, _source=source_fields)

    # ── pipelines ──────────────────────────────────────────────────────────
    @mcp.tool(tags={"pipelines"})
    async def opensearch_ingest_pipeline_get(
        pipeline_id: str = Field(description="Ingest pipeline id."),
    ) -> dict[str, Any]:
        """Read an ingest pipeline definition."""
        return get_client().get_ingest_pipeline(pipeline_id)

    @mcp.tool(tags={"pipelines", "mutating"})
    async def opensearch_ingest_pipeline_put(
        pipeline_id: str = Field(description="Ingest pipeline id."),
        body: dict[str, Any] = Field(
            description="Pipeline definition ({'processors': [...]})."
        ),
    ) -> dict[str, Any]:
        """Create or replace an ingest pipeline."""
        if not body:
            raise OpenSearchApiError("opensearch_ingest_pipeline_put requires 'body'")
        return get_client().put_ingest_pipeline(pipeline_id, body)

    # ── security / DLS (never hand-authored here) ─────────────────────────
    @mcp.tool(tags={"security"})
    async def opensearch_read_dls_rules(
        role: str = Field(description="OpenSearch security-plugin role name."),
    ) -> dict[str, Any]:
        """Read one security-plugin role's index permissions/DLS query (read-only)."""
        return get_client().read_dls_rules(role)

    @mcp.tool(
        annotations={
            "title": "Apply DLS Policy Bundle",
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": True,
        },
        tags={"security", "mutating"},
    )
    async def opensearch_apply_dls_bundle(
        bundle: dict[str, Any] = Field(
            description=(
                "A DEC-CA-04-shaped policy bundle, as generated by CA-16 and "
                "rendered by CA-26 — never hand-authored by the caller. Must "
                "contain top-level 'governs' (['M1']), 'graph', and "
                "'renderings.opensearch' (list of "
                "{index_pattern, role, dls_query})."
            )
        ),
    ) -> dict[str, Any]:
        """Apply a CA-16/26-rendered policy bundle's OpenSearch renderings.

        Validates the bundle's shape FIRST (fails closed on any single
        malformed rendering — never partially applies the bundle) and only
        then pushes each ``{index_pattern, role, dls_query}`` entry to
        OpenSearch's security-plugin role API. This tool contains no code
        path that constructs a DLS predicate from scratch — it is a pure
        applier, per this package's Authority section."""
        validated = _validate_dls_bundle(bundle)
        client = get_client()
        applied = []
        for entry in validated:
            result = client.apply_dls_bundle_rendering(
                role=entry["role"],
                index_pattern=entry["index_pattern"],
                dls_query=entry["dls_query"],
            )
            applied.append(
                {
                    "role": entry["role"],
                    "index_pattern": entry["index_pattern"],
                    "result": result,
                }
            )
        return {"applied": applied, "count": len(applied)}
