"""Public client facade for lucerna_mcp."""

from lucerna_mcp.api.api_client_opensearch import OpenSearchApi, OpenSearchApiError

__all__ = ["Api", "OpenSearchApiError"]


class Api(OpenSearchApi):
    """Authenticated OpenSearch client — always the calling principal's token."""

    pass
