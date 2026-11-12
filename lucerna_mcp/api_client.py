"""Public client facade for lucerna_mcp."""

from lucerna_mcp.api.api_client_opensearch import OpenSearchApi, OpenSearchApiError

__all__ = ["Api", "OpenSearchApiError"]


class Api(OpenSearchApi):
    """Authenticated OpenSearch client — always the calling principal's token."""

    pass


def served_api() -> type:
    """The operation facade the connector serves: ``Api`` minus the gated k-NN methods."""
    import inspect

    from lucerna_mcp.knn_gate import KNN_METHODS, knn_enabled

    hidden = frozenset() if knn_enabled() else KNN_METHODS
    members = {
        name: method
        for name, method in inspect.getmembers(Api, inspect.isfunction)
        if not name.startswith("_") and name not in hidden
    }
    return type("ServedApi", (), members)
