"""
Standalone server runner for HK Climate MCP Server.
"""
from hkopenai_common.cli_utils import cli_main
from hkopenai.hk_climate_mcp_server.server import server

if __name__ == "__main__":
    cli_main(server, "HK Climate MCP Server")