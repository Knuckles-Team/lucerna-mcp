"""Surface contracts: tool use, links, data locations and business roles."""

from scion_sdk.surface_contracts import (
    BusinessRole,
    DataLocation,
    Refusal,
    SurfaceLink,
    ToolStep,
    ToolUseContract,
)

CONTRACTS = (
    ToolUseContract(
        task="inspect-search-tier",
        description="Read cluster health, whether the k-NN plugin works, and the aliases.",
        steps=(
            ToolStep(
                tool="lucerna_cluster_health",
                params=(),
                result=("status", "number_of_nodes"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="opensearch_get_aliases",
                params=("index",),
                result=("alias", "index"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_get_aliases",
                params=("index",),
                result=("alias", "index"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="search-documents",
        description="Run lexical searches as the calling principal.",
        steps=(
            ToolStep(
                tool="opensearch_search",
                params=("index", "query", "size", "source_fields"),
                result=("hits",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_search",
                params=("index", "query", "size", "_source"),
                result=("hits",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="create-and-tune-index",
        description="Create an index, update its mapping and settings, then read it back through the aliases.",
        steps=(
            ToolStep(
                tool="opensearch_create_index",
                params=("index", "mappings", "settings"),
                result=("acknowledged", "index"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_create_index",
                params=("index", "body"),
                result=("acknowledged", "index"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="opensearch_update_mapping",
                params=("index", "properties"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_update_mapping",
                params=("index", "properties"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="opensearch_update_settings",
                params=("index", "settings"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_update_settings",
                params=("index", "settings"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="opensearch_get_aliases",
                params=("index",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-aliases-and-rollover",
        description="Switch aliases atomically and roll an alias over to a new index.",
        steps=(
            ToolStep(
                tool="opensearch_get_aliases",
                params=("index",),
                result=("alias", "index"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="opensearch_manage_alias",
                params=("actions",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_manage_alias",
                params=("actions",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="opensearch_rollover",
                params=("alias", "conditions", "new_index"),
                result=("rolled_over", "new_index"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_rollover",
                params=("alias", "conditions", "new_index"),
                result=("rolled_over", "new_index"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="delete-index",
        description="Delete an index on confirmation.",
        steps=(
            ToolStep(
                tool="opensearch_get_aliases",
                params=("index",),
                result=("alias", "index"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="opensearch_delete_index",
                params=("index",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal("INDEX_NOT_FOUND", "no index has the name"),
                ),
            ),
            ToolStep(
                tool="lucerna_delete_index",
                params=("index", "confirm"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "CONFIRMATION_REQUIRED",
                        "the caller has not confirmed the destructive call",
                    ),
                    Refusal("INDEX_NOT_FOUND", "no index has the name"),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="manage-ingest-pipelines",
        description="Read and define ingest pipelines.",
        steps=(
            ToolStep(
                tool="opensearch_ingest_pipeline_get",
                params=("pipeline_id",),
                result=("processors",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_get_ingest_pipeline",
                params=("pipeline_id",),
                result=("processors",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="opensearch_ingest_pipeline_put",
                params=("pipeline_id", "body"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_put_ingest_pipeline",
                params=("pipeline_id", "body"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="apply-access-policy",
        description="Read a role's document-level security and apply a rendered policy bundle.",
        steps=(
            ToolStep(
                tool="opensearch_read_dls_rules",
                params=("role",),
                result=("index_permissions",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_read_dls_rules",
                params=("role",),
                result=("index_permissions",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
            ToolStep(
                tool="opensearch_apply_dls_bundle",
                params=("bundle",),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                    Refusal(
                        "MALFORMED_BUNDLE",
                        "the bundle lacks renderings or recognized governs",
                    ),
                ),
            ),
            ToolStep(
                tool="lucerna_apply_dls_bundle_rendering",
                params=("role", "index_pattern", "dls_query"),
                result=("result",),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
    ToolUseContract(
        task="rebuild-index-from-graph",
        description="Trigger a rebuild of an index from the knowledge graph.",
        steps=(
            ToolStep(
                tool="opensearch_reindex_from_kg",
                params=("index_pattern",),
                result=("run_id", "state"),
                refusals=(
                    Refusal(
                        "ACCESS_DENIED", "the credential lacks access to the operation"
                    ),
                    Refusal(
                        "INVALID_ARGUMENT", "the upstream system rejects the input"
                    ),
                ),
            ),
        ),
    ),
)

LINKS = (
    SurfaceLink(
        task="inspect-search-tier",
        tools=(
            "lucerna_cluster_health",
            "opensearch_get_aliases",
            "lucerna_get_aliases",
        ),
        prompts=(
            "lucerna-mcp-operator",
            "lucerna-mcp-search-administrator",
            "lucerna-mcp-search-analyst",
        ),
        skills=("opensearch-index-operations",),
    ),
    SurfaceLink(
        task="search-documents",
        tools=(
            "opensearch_search",
            "lucerna_search",
        ),
        prompts=("lucerna-mcp-operator", "lucerna-mcp-search-analyst"),
        skills=("opensearch-search",),
    ),
    SurfaceLink(
        task="create-and-tune-index",
        tools=(
            "opensearch_create_index",
            "lucerna_create_index",
            "opensearch_update_mapping",
            "lucerna_update_mapping",
            "opensearch_update_settings",
            "lucerna_update_settings",
            "opensearch_get_aliases",
        ),
        prompts=("lucerna-mcp-operator", "lucerna-mcp-search-administrator"),
        skills=("opensearch-index-operations",),
    ),
    SurfaceLink(
        task="manage-aliases-and-rollover",
        tools=(
            "opensearch_get_aliases",
            "opensearch_manage_alias",
            "lucerna_manage_alias",
            "opensearch_rollover",
            "lucerna_rollover",
        ),
        prompts=("lucerna-mcp-operator", "lucerna-mcp-search-administrator"),
        skills=("opensearch-index-operations",),
    ),
    SurfaceLink(
        task="delete-index",
        tools=(
            "opensearch_get_aliases",
            "opensearch_delete_index",
            "lucerna_delete_index",
        ),
        prompts=("lucerna-mcp-operator", "lucerna-mcp-search-administrator"),
        skills=("opensearch-index-operations",),
    ),
    SurfaceLink(
        task="manage-ingest-pipelines",
        tools=(
            "opensearch_ingest_pipeline_get",
            "lucerna_get_ingest_pipeline",
            "opensearch_ingest_pipeline_put",
            "lucerna_put_ingest_pipeline",
        ),
        prompts=("lucerna-mcp-operator", "lucerna-mcp-search-administrator"),
        skills=("opensearch-index-operations",),
    ),
    SurfaceLink(
        task="apply-access-policy",
        tools=(
            "opensearch_read_dls_rules",
            "lucerna_read_dls_rules",
            "opensearch_apply_dls_bundle",
            "lucerna_apply_dls_bundle_rendering",
        ),
        prompts=("lucerna-mcp-operator", "lucerna-mcp-search-administrator"),
        skills=("opensearch-search",),
    ),
    SurfaceLink(
        task="rebuild-index-from-graph",
        tools=("opensearch_reindex_from_kg",),
        prompts=("lucerna-mcp-operator", "lucerna-mcp-search-administrator"),
        skills=("opensearch-kg-ingestion",),
    ),
)

LOCATIONS = (
    DataLocation(
        name="search-indexes",
        holds=("SearchIndex", "SearchAlias", "IndexingRun"),
        instance="OPENSEARCH_URL",
        read_tool="opensearch_get_aliases",
        federation_key="index",
    ),
)

ROLES = (
    BusinessRole(
        name="search administrator",
        description="Create, tune, alias, roll over and retire indexes and apply access policy.",
        tasks=(
            "inspect-search-tier",
            "create-and-tune-index",
            "manage-aliases-and-rollover",
            "delete-index",
            "manage-ingest-pipelines",
            "apply-access-policy",
            "rebuild-index-from-graph",
        ),
    ),
    BusinessRole(
        name="search analyst",
        description="Find indexed knowledge-graph content with lexical search.",
        tasks=("search-documents", "inspect-search-tier"),
    ),
)
