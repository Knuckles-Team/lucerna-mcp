"""Main FastMCP server and tool registration for lucerna-mcp."""

from lucerna_mcp.kg_ingest import register_ingest_tools  # noqa: F401
from lucerna_mcp.mcp.mcp_opensearch import register_opensearch_tools  # noqa: F401

# SDK discovery registers the register_<tag>_tools functions bound in this module.
__all__ = ["register_ingest_tools", "register_opensearch_tools"]
