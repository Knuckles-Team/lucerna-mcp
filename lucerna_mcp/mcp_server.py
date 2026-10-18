"""Main FastMCP server and tool registration for lucerna-mcp."""

import sys
from typing import Any

from agent_connector_sdk.config import load_config
from agent_connector_sdk.mcp.server import create_mcp_server
from agent_connector_sdk.mcp.tool_surface import register_tool_surface
from fastmcp.utilities.logging import get_logger
from starlette.requests import Request
from starlette.responses import JSONResponse

from lucerna_mcp.api_client import Api
from lucerna_mcp.auth import get_client
from lucerna_mcp.kg_ingest import register_ingest_tools  # noqa: F401
from lucerna_mcp.mcp.mcp_opensearch import register_opensearch_tools  # noqa: F401

__version__ = "0.2.0"
logger = get_logger(name="lucerna_mcp")


def get_mcp_instance() -> tuple[Any, ...]:
    load_config()
    args, mcp, middlewares = create_mcp_server(
        name="Lucerna MCP",
        version=__version__,
        instructions=(
            "Lucerna MCP Server (CA-50 search tier) — index/alias/settings/rollover "
            "admin, BM25/kNN/hybrid search always run as the calling principal so "
            "document-level security applies, ingest-pipeline admin, DLS-bundle "
            "read/apply (never hand-authors a rule — only applies what CA-16/26 "
            "render), and a trigger-only reindex-from-KG tool."
        ),
    )

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(_request: Request) -> JSONResponse:
        return JSONResponse({"status": "OK"})

    register_tool_surface(
        mcp,
        client_cls=Api,
        get_client=get_client,
        service="lucerna-mcp",
        tools_module=sys.modules[__name__],
    )

    for mw in middlewares:
        mcp.add_middleware(mw)
    return mcp, args, middlewares


def mcp_server() -> None:
    mcp, args, middlewares = get_mcp_instance()
    print(f"Lucerna MCP v{__version__}", file=sys.stderr)
    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    mcp_server()
