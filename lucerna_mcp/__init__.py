"""lucerna-mcp: OpenSearch (Iceberg REST catalog) API + MCP Server + A2A Server."""

import importlib
import inspect
from typing import Any

__all__: list[str] = []

CORE_MODULES = ["lucerna_mcp.api_client"]
OPTIONAL_MODULES = {
    "lucerna_mcp.mcp_server": "mcp",
}


def _expose_members(module):
    for name, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) or inspect.isfunction(obj)) and not name.startswith(
            "_"
        ):
            globals()[name] = obj
            if name not in __all__:
                __all__.append(name)


for module_name in CORE_MODULES:
    module = importlib.import_module(module_name)
    _expose_members(module)

_loaded_optional_modules: dict[str, Any] = {}


def _import_module_safely(module_name: str):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


_AVAILABILITY_FLAG_MARKERS = {
    "_MCP_AVAILABLE": "mcp_server",
}


def _resolve_availability_flag(name: str) -> bool | None:
    """Return the True/False availability flag for `name`, or None if `name`
    isn't one of the recognized ``_*_AVAILABLE`` markers."""
    marker = _AVAILABILITY_FLAG_MARKERS.get(name)
    if marker is None:
        return None
    module_key = next((k for k in OPTIONAL_MODULES if marker in k), None)
    return _import_module_safely(module_key) is not None if module_key else False


def _ensure_optional_module_loaded(module_name: str):
    """Import and expose `module_name`'s public members once, then return it
    (or the cached module, or None if it isn't installed)."""
    if module_name not in _loaded_optional_modules:
        module = _import_module_safely(module_name)
        if module is not None:
            _loaded_optional_modules[module_name] = module
            _expose_members(module)
    return _loaded_optional_modules.get(module_name)


def _lookup_optional_attribute(name: str) -> Any:
    for module_name in OPTIONAL_MODULES:
        module = _ensure_optional_module_loaded(module_name)
        if module is not None and hasattr(module, name):
            return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __getattr__(name: str) -> Any:
    flag = _resolve_availability_flag(name)
    if flag is not None:
        return flag
    return _lookup_optional_attribute(name)


def __dir__() -> list[str]:
    return sorted(list(globals().keys()) + __all__)


from agent_connector_sdk.connector import Connector

from lucerna_mcp.api_client import Api
from lucerna_mcp.auth import get_client

connector = Connector(
    api=Api,
    get_client=get_client,
    tools="lucerna_mcp.mcp_server",
    instructions="Lucerna MCP Server (CA-50 search tier) — index/alias/settings/rollover admin, BM25/kNN/hybrid search always run as the calling principal so document-level security applies, ingest-pipeline admin, DLS-bundle read/apply (never hand-authors a rule — only applies what CA-16/26 render), and a trigger-only reindex-from-KG tool.",
)
