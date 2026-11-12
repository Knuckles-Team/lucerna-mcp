"""Search-size cap and the absence of vector search, exercised against the real
``OpenSearchApi`` class with its low-level ``opensearchpy`` client mocked out
(no network) — never against ``auth.get_client()``, per this package's own
test-only-escape-hatch rule (see ``api/api_client_opensearch.py``)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from lucerna_mcp.api.api_client_base import OpenSearchApiError
from lucerna_mcp.api.api_client_opensearch import OpenSearchApi


def _api() -> OpenSearchApi:
    return OpenSearchApi(
        "https://opensearch.example", _test_basic_auth=("test-user", "test-pass")
    )


def test_search_caps_size_at_100():
    api = _api()
    api._client = MagicMock()
    api._client.search.return_value = {"hits": {"hits": []}}

    api.search("kg-*", {"match_all": {}}, size=10_000)

    _, kwargs = api._client.search.call_args
    assert kwargs["body"]["size"] == 100


def test_search_rejects_negative_size_by_flooring_at_zero():
    api = _api()
    api._client = MagicMock()
    api._client.search.return_value = {"hits": {"hits": []}}

    api.search("kg-*", {"match_all": {}}, size=-5)

    _, kwargs = api._client.search.call_args
    assert kwargs["body"]["size"] == 0


def test_no_vector_search_surface_remains():
    api = _api()
    for name in ("knn_search", "hybrid_search", "knn_plugin_enabled"):
        assert not hasattr(api, name)


def test_no_vector_search_tool_is_registered():
    import inspect

    from lucerna_mcp.mcp import mcp_opensearch

    source = inspect.getsource(mcp_opensearch)
    for name in ("opensearch_knn_search", "opensearch_hybrid_search", "opensearch_knn_plugin_enabled"):
        assert name not in source


def test_create_index_is_idempotent_on_already_exists():
    from opensearchpy.exceptions import TransportError

    api = _api()
    api._client = MagicMock()
    api._client.indices.create.side_effect = TransportError(
        400,
        "resource_already_exists_exception",
        {"error": {"type": "resource_already_exists_exception"}},
    )

    result = api.create_index("kg-existing")

    assert result["already_exists"] is True
