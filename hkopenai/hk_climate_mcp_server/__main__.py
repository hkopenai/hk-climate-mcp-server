"""
HKO MCP Server Main Module

This module serves as the entry point for the HKO MCP Server application.
It handles command-line arguments and initiates the main server functionality.
"""

import argparse
from .server import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HKO MCP Server")
    parser.add_argument(
        "-s", "--sse", action="store_true", help="Run in SSE mode instead of stdio"
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Port to run the server on (default: 8000)",
    )
    args = parser.parse_args()
    main(args)
