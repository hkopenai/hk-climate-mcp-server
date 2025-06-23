# Project Brief

## Core Requirements
- Provide weather data from Hong Kong Observatory via MCP interface
- Support multiple weather data types (current, forecasts, warnings)
- Offer both stdio and SSE communication modes
- Maintain API compatibility with FastMCP specification

## Goals
- Create reliable weather data service for Hong Kong region
- Enable easy integration with Cline and other MCP clients
- Provide comprehensive weather information in multiple languages
- Ensure high availability and performance

## Scope
- Included:
  - Current weather observations
  - 9-day weather forecasts
  - Weather warnings and alerts
  - Special weather tips
  - Tidal data (astronomical tides, high/low tides)
  - Sun/moon times (sunrise/sunset, moonrise/moonset)
  - Lightning data
  - Visibility data
  - Temperature data (mean, max, min)
  - Weather and radiation reports
- Excluded:
  - Weather data outside Hong Kong
  - Graphical weather visualizations

## Key Stakeholders
- Hong Kong Observatory (data provider)
- Cline integration team
- Weather application developers

## Timeline
- Initial release: v1.0.0 (current)
- Future milestones:
  - Add caching layer
  - Expand to more data sources
  - Implement rate limiting
