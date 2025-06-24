# System Patterns

## System Architecture
- FastMCP server exposing weather data tools
- Modular design with separate tool implementation for each data type
- REST API client pattern for HKO data access
- Layered architecture:
  1. Interface layer (server.py - FastMCP tools)
  2. Service layer (individual tool files - data processing)
  3. Data layer (HKO API - raw weather data)

## Key Technical Decisions
- Using FastMCP for standardized tool interface
- Direct HTTP calls to HKO API rather than database caching
- Support for both stdio and SSE transport modes
- Language parameter support (en/tc/sc) throughout API
- Modular tool structure with separate files for each weather data type

## Design Patterns in Use
- Adapter pattern: Tool files adapt HKO API to MCP interface
- Facade pattern: Simplified interface to complex weather data
- Singleton pattern: Single FastMCP server instance
- Strategy pattern: Different transport modes (stdio/SSE)

## Component Relationships
- server.py depends on individual tool files for all weather data
- Tool files depend on requests library for HTTP
- Both depend on FastMCP framework
- Independent of specific client implementation

## Critical Implementation Paths
1. Tool registration in server.py
2. HTTP request/response handling in tool files
3. Data transformation from HKO format to MCP format
4. Error handling for API failures
5. Transport mode selection (stdio/SSE)
