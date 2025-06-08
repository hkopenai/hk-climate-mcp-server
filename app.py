import argparse
from fastmcp import FastMCP
from hko_tools import HKOTools
from typing import Dict

def create_mcp_server():
    """Create and configure the HKO MCP server"""
    mcp = FastMCP(name="HKOServer")

    @mcp.tool(
        description="Get current weather warnings from Hong Kong Observatory"
    )
    def get_weather_warning() -> Dict:
        return HKOTools.get_weather_warning()

    @mcp.tool(
        description="Get 9-day weather forecast from Hong Kong Observatory"
    )
    def get_9day_forecast() -> Dict:
        return HKOTools.get_9day_forecast()

    @mcp.tool(
        description="Get current weather observations, warnings, temperature, humiditya and rainfall in Hong Kong from Hong Kong Observatory, with option region or place in Hong Kong",
    )
    def get_current_weather(region: str = "Hong Kong Observatory") -> Dict:
        return HKOTools.get_current_weather(region)

    return mcp

def main():
    parser = argparse.ArgumentParser(description='HKO MCP Server')
    parser.add_argument('-s', '--sse', action='store_true',
                       help='Run in SSE mode instead of stdio')
    args = parser.parse_args()

    server = create_mcp_server()
    
    if args.sse:
        server.run(transport="streamable-http")
        print("HKO MCP Server running in SSE mode on port 8000")
    else:
        server.run()
        print("HKO MCP Server running in stdio mode")

if __name__ == "__main__":
    main()
