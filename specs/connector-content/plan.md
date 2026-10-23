# CONN-LUCERNA-MCP-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `lucerna-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `lucerna_mcp` from it.
