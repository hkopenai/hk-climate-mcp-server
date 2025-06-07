# HKO MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/yourusername/hko-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Tests](https://github.com/neoalienson/hko-mcp-server/actions/workflows/test.yml/badge.svg)](https://github.com/neoalienson/hko-mcp-server/actions/workflows/test.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/neoalienson/74ca6d01d35092293864c8044cda02c3/raw/3fd49519da12394e190fc76063f45be99e39469f/coverage.json)](https://github.com/neoalienson/hko-mcp-server/actions/workflows/test.yml)

This is an MCP server that provides access to Hong Kong Observatory weather data through a FastMCP interface.

## Features
- Current weather: Get current weather observations from HKO (supports optional region parameter)

## Setup

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python hko_mcp_server.py
   ```

### Running Options

- Default stdio mode: `python hko_mcp_server.py`
- SSE mode (port 8000): `python hko_mcp_server.py --sse`

## Cline Integration

To connect this MCP server to Cline using stdio:

1. Add this configuration to your Cline MCP settings (cline_mcp_settings.json):
```json
{
  "hko-server": {
    "disabled": false,
    "timeout": 3,
    "type": "stdio",
    "command": "python",
    "args": [
      "c:/Projects/hko-mcp-server/hko_mcp_server.py"
    ]
  }
}
```

## Testing

Tests are available in `tests/test_hko_tools.py`. Run with:
```bash
python -m unittest tests/test_hko_tools.py
