# HKO MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/hkopenai/hk-climate-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This is an MCP server that provides access to climate and weather data through a FastMCP interface.

## Data Source

* Hong Kong Observatory 

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
   python app.py
   ```

### Running Options

- Default stdio mode: `python app.py`
- SSE mode (port 8000): `python app.py --sse`

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
      "c:/Projects/hkopenai/hk-climate-mcp-server/app.py"
    ]
  }
}
```

## Testing

Tests are available in `tests`. Run with:
```bash
pytest