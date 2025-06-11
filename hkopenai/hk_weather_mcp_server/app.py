import argparse
from fastmcp import FastMCP
from hkopenai.hk_weather_mcp_server import tool_weather
from typing import Dict, Annotated, Optional
from pydantic import Field

def create_mcp_server():
    """Create and configure the HKO MCP server"""
    mcp = FastMCP(name="HKOServer")

    @mcp.tool(
        description="Get current weather observations, warnings, temperature, humidity and rainfall in Hong Kong from Hong Kong Observatory, with option region or place in Hong Kong",
    )
    def get_current_weather(region: str = "Hong Kong Observatory") -> Dict:
        return tool_weather.get_current_weather(region)
    
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
