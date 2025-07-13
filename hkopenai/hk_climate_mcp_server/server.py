"""
HKO MCP Server - A server for handling weather data requests using the Model Context Protocol (MCP).

This module provides a server implementation for accessing various weather data tools
from the Hong Kong Observatory through the MCP protocol. It supports both HTTP and stdio
transports for communication.
"""

from fastmcp import FastMCP
from .tools import astronomical
from .tools import current_weather
from .tools import forecast
from .tools import lightning
from .tools import radiation
from .tools import temperature
from .tools import tides
from .tools import visibility
from .tools import warnings


def create_mcp_server():
    """
    Create and configure the HKO MCP server.

    Returns:
        FastMCP: Configured MCP server instance with weather data tools.
    """
    mcp = FastMCP(name="HKOServer")

    current_weather.register(mcp)
    forecast.register(mcp)
    lightning.register(mcp)
    radiation.register(mcp)
    temperature.register(mcp)
    tides.register(mcp)
    visibility.register(mcp)
    warnings.register(mcp)
    astronomical.register(mcp)

    return mcp


def main(host: str, port: int, sse: bool):
    """
    Main function to run the MCP Server.

    Args:
        args: Command line arguments passed to the function.
    """

    server = create_mcp_server()
    if sse:
        server.run(transport="streamable-http", host=host, port=port)
        print(
            f"MCP Server running in SSE mode on port {args.port}, bound to {args.host}"
        )
    else:
        server.run()
        print("MCP Server running in stdio mode")
