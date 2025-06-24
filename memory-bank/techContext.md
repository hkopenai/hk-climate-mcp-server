# Tech Context

## Technologies Used
- Python 3.10+
- FastMCP framework
- Requests library for HTTP calls
- Pytest for testing

## Development Setup
- Python virtual environment recommended
- Install dependencies: `pip install -e .`
- Run tests: `pytest`

## Technical Constraints
- Limited to Hong Kong weather data only
- Requires internet connection to fetch HKO data
- Supports Python 3.10+ only

## Dependencies
- Core:
  - fastmcp>=0.1.0 (MCP protocol implementation)
  - requests>=2.31.0 (HTTP client)
- Development:
  - pytest>=8.2.0 (testing framework)
  - pytest-cov>=6.1.1 (test coverage)

## Tool Usage Patterns
- Run server in stdio mode: `python server.py`
- Run server in SSE mode: `python server.py --sse`
- Run tests: `pytest tests/`
- Build package: `python -m build`
