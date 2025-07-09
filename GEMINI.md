# Project Overview

## Active Context
### Current Work Focus
- Fixing unit tests for the server implementation
- Ensuring all project context is properly captured
- Establishing documentation standards for future updates
- Resolving packaging issue with tools directory
- Documenting API handling strategies and error handling aspects for MCP tools

#### API Handling Strategies and Error Handling Table
| Tool Name                       | API Handling Strategy Type                          | Validated |
|---------------------------------|----------------------------------------------------|-----------|
| get_current_weather            | Type 1 | No        |
| get_9_day_weather_forecast     | Type 1 | No        |
| get_local_weather_forecast     | Type 1 | No        |
| get_weather_warning_summary    | Type 1 | No        |
| get_weather_warning_info       | Type 1 | No        |
| get_special_weather_tips       | Type 1 | No        |
| get_visibility            | Type 2 | No        |
| get_lightning_data             | Type 2 | No        |
| get_moon_times                 | Type 2 | No        |
| get_hourly_tides               | Type 3 | No        |
| get_high_low_tides             | Type 3 | No        |
| get_sunrise_sunset_times       | Type 2 | No        |
| get_gregorian_lunar_calendar   | Type 2 | No        |
| get_daily_mean_temperature     | Type 3 | No        |
| get_daily_max_temperature      | Type 3 | No        |
| get_daily_min_temperature      | Type 3 | No        |
| get_weather_radiation_report   | Type 1 | Yes       |
| get_valid_station_codes        | Type 1 | No        |

This table serves as a reference for current and future development, ensuring that each tool's API interaction and error handling approach is aligned with the defined principles.

### Recent Changes
- Successfully fixed the unit test for `test_server.py`
- Updated packaging configuration to include `tools` directory files in the built package
- Created `MANIFEST.in` to specify inclusion of tool files
- Updated `pyproject.toml` to enable `include-package-data`
- Rebuilt package to confirm inclusion of tools
- Created all core memory bank files
- Updated projectbrief.md with actual project details
- Populated productContext.md with purpose and value proposition
- Documented technical stack in techContext.md
- Captured system architecture in systemPatterns.md

### Next Steps
- Update progress.md with current project status
- Review all documentation for completeness
- Establish regular memory bank update process

### Active Decisions
- Using standardized markdown format for all documentation
- Maintaining clear separation between different context types
- Prioritizing documentation completeness before adding details

### Important Patterns
- Following hierarchical documentation structure
- Linking related concepts across files
- Using consistent formatting and headers

### Learnings
- Memory bank is crucial for maintaining context
- Documentation should be updated incrementally
- Clear structure makes information easier to find
- Packaging configuration requires explicit inclusion of subdirectories

## MCP Tool Implementation Principles

### Overview
This document outlines the principles for implementing tools within the Hong Kong Climate MCP Server, with a specific focus on guiding Language Learning Models (LLMs) to achieve their goals when a tool is called without proper input or when an API returns an error. These principles aim to enhance the reliability, usability, and integration ease of the MCP server tools, aligning with the project's objectives of providing a standardized, high-performance weather data service.

### Core Principles

#### 1. Input Validation and Guidance
- **Validation Check**: Every tool must perform thorough input validation before processing any request. This includes checking for the presence, type, and format of all required parameters as defined in the tool's input schema.
- **Error Messaging**: If a tool is called without proper input (missing or incorrect parameters), it must return a clear, actionable error message. This message should:
  - Specify which parameters are missing or incorrect.
  - Provide the expected format or type for each parameter.
  - Include a reference to the tool's input schema for further details.
- **Guidance for Correction**: Alongside the error message, the tool should suggest corrective actions or provide examples of correct input. For instance, if a required 'date' parameter is missing, the tool could suggest a format like 'YYYY-MM-DD' and provide an example.

#### 2. API Error Handling and Recovery Guidance
- **Error Detection**: Tools must robustly handle errors returned by external APIs, such as the Hong Kong Observatory (HKO) API. This includes detecting HTTP error codes (e.g., 404, 500), connection issues, or unexpected response formats.
- **Detailed Error Reporting**: Upon encountering an API error, the tool should return a detailed error message to the LLM, including:
  - The specific error code or message received from the API.
  - The context of the request that led to the error (e.g., the endpoint called, parameters used).
  - Any relevant API documentation or error code explanations if available.
- **Recovery Suggestions**: The tool should guide the LLM on potential recovery steps. Examples include:
  - Retrying the request after a delay if the error suggests a temporary issue (e.g., rate limiting or server overload).
  - Checking network connectivity if a connection error occurs.
  - Using alternative parameters or endpoints if the requested data is unavailable (e.g., suggesting a different weather station or date range).
  - Fallback to cached data if available and the API is down (once caching is implemented).

#### 3. Contextual Tool Recommendation
- **Relevance Assessment**: If a tool determines that it cannot fulfill the request due to improper input or API limitations, it should assess whether another tool within the MCP server might be more suitable for the LLM's goal.
- **Tool Suggestion**: The tool should suggest alternative tools by name and briefly describe their purpose or capabilities. For example, if a request for current weather data fails due to an invalid region, the tool might suggest using 'get_valid_station_codes' to retrieve acceptable input values.
- **Integration Path**: Provide a clear path for the LLM to integrate with the suggested tool, including any prerequisite steps (e.g., fetching valid input data) or parameter adjustments needed.

#### 4. User-Centric Feedback Design
- **Clarity and Conciseness**: All feedback messages (error or guidance) must be clear, concise, and tailored for programmatic consumption by LLMs, avoiding ambiguous language or unnecessary verbosity.
- **Structured Format**: Feedback should be structured (e.g., JSON format if applicable) to facilitate parsing by LLMs, including fields like 'error_type', 'message', 'suggested_action', and 'alternative_tool'.
- **Consistency Across Tools**: Ensure that feedback mechanisms are consistent across all tools within the MCP server, using standardized error codes or message templates to build predictability for LLMs.

#### 5. Proactive Error Prevention
- **Default Values**: Where possible, tools should provide sensible default values for optional parameters to prevent errors due to omission. For instance, defaulting to 'en' for language if not specified.
- **Input Constraints**: Clearly define and enforce constraints on input parameters (e.g., date ranges, valid station codes) within the tool's schema and documentation, reducing the likelihood of invalid calls.
- **Pre-Validation Hooks**: Implement pre-validation hooks or checks that can intercept common mistakes before they reach the API call stage, returning guidance early in the process.

#### 6. API Handling Strategies for Diverse Data Sources
- **Categorization of API Types**: Tools must identify and handle different API types based on their response structure and processing needs:
  - **Type 1**: For APIs returning structured data (e.g., JSON with metadata and descriptions), tools should directly pass the response to the client without additional processing, ensuring the data is in a readily consumable format for LLMs. Error handling should focus on validating the structure and completeness of the response.
  - **Type 2**: For APIs where the response data needs contextual supplementation (e.g., codes or abbreviations requiring explanation), tools must fetch or reference a data dictionary to enrich the response. The enriched data should be formatted to include both raw data and explanatory metadata, aiding LLMs in interpretation.
  - **Type 3**: For APIs returning data in formats like CSV that require transformation for lower-end LLMs, tools must parse and convert the data into a structured format (e.g., JSON). Additionally, supplement the data with a data dictionary to explain fields or values, ensuring accessibility. Transformation logic should be modular to handle various input formats.
  - **Type 4 - APIs Requiring Aggregation from Multiple Calls**: For APIs where data must be aggregated from multiple endpoints or calls, tools should orchestrate these calls, handle dependencies, and combine results into a unified response. Use a data dictionary to standardize and explain aggregated data elements. Ensure error handling accounts for partial failures in multi-call sequences.
- **Cross-Cutting Concerns**:
  - **Paging**: For APIs with paginated responses, tools must implement logic to iterate through pages, aggregate data, and handle pagination tokens or parameters. Provide feedback to LLMs on progress or issues (e.g., incomplete data due to pagination limits).
  - **Retries**: Implement retry mechanisms for transient failures (e.g., rate limiting, temporary outages) with exponential backoff strategies. Inform LLMs of retry attempts and outcomes in error messages, suggesting alternative actions if retries fail.
  - **Error Handling Specific to API Type**: Tailor error handling to the API type. For instance, transformation errors in Type 3 should include details on format mismatches, while aggregation errors in Type 4 should specify which API call failed and suggest fallback to partial data if available.
- **Performance Optimization**: Minimize API calls by caching responses where feasible (once caching is implemented), especially for Type 4 aggregation scenarios. Optimize transformation processes in Type 3 to handle large datasets efficiently, providing progress feedback for long-running operations.
- **Documentation and Guidance**: Each tool must document the API type it interacts with and the specific handling strategy employed. Guidance messages should inform LLMs of the API type and any specific actions needed (e.g., providing pagination parameters, awaiting aggregation completion).

#### 7. Logging and Diagnostics
- **Error Logging**: Tools must log all errors (input validation failures and API errors) internally for debugging and performance monitoring, without exposing sensitive details to the LLM unless necessary.
- **Diagnostic Information**: Provide diagnostic information in error messages, such as request IDs or timestamps, to help trace issues if the LLM or developer needs to escalate the problem for support.

### Implementation Considerations
- **Modular Error Handling**: Design error handling as a modular component within each tool to allow for easy updates or enhancements as new error types or API behaviors are encountered.
- **Versioning**: Ensure that changes to error handling or guidance messages are versioned to maintain backward compatibility with existing LLM integrations.
- **Testing**: Include comprehensive test cases for input validation and API error scenarios in the test suite (using Pytest), ensuring that guidance messages are triggered correctly and are helpful.
- **Documentation**: Update tool documentation to reflect these principles, including examples of error messages and recovery steps, to aid developers and LLMs in understanding expected behavior.

### Alignment with Project Goals
- **Reliability**: By providing robust error handling and recovery guidance, these principles address current known issues like limited error handling for HKO API failures, enhancing overall system reliability.
- **Ease of Integration**: Clear guidance and tool recommendations simplify the integration process for LLMs and developers, aligning with the project's user experience goals.
- **Performance**: Proactive error prevention and structured feedback minimize unnecessary API calls or retries, supporting high performance objectives.

### Future Enhancements
- Once caching is implemented, integrate fallback mechanisms to cached data in error guidance.
- As rate limiting is added, include specific guidance on retry intervals or backoff strategies in error messages.
- Expand tool recommendation logic to consider external MCP servers or tools as additional data sources become available.

This document serves as a guideline for current and future tool implementations within the Hong Kong Climate MCP Server, ensuring a consistent, user-friendly approach to error handling and tool usage guidance.

## Product Context

### Purpose
- Provide programmatic access to Hong Kong weather data through standardized MCP interface
- Bridge between HKO's public weather data and developer applications
- Enable real-time weather monitoring and alerting capabilities

### Problems Solved
- Eliminates need for scraping HKO website for weather data
- Standardizes access to multiple weather data types through single API
- Provides reliable, structured weather data with proper documentation
- Supports multiple languages (English, Traditional Chinese, Simplified Chinese)

### User Experience
- Developers can integrate weather data with minimal setup
- Simple, well-documented API endpoints for all weather data types
- Consistent response formats across all endpoints
- Supports both interactive (stdio) and streaming (SSE) modes

### Value Proposition
- Saves development time by providing ready-to-use weather API
- More reliable than scraping or manual data collection
- Enables building weather-aware applications quickly
- Supports multiple integration methods for different use cases

## Progress

### What Works
- All core weather data tools implemented:
  - Current weather observations
  - 9-day weather forecasts
  - Weather warnings and alerts
  - Special weather tips
- Both stdio and SSE transport modes supported
- Language support for English, Traditional and Simplified Chinese
- Unit test for `test_server.py` has been successfully fixed
- Packaging issue resolved to include `tools` directory in built package

### What's Left to Build
- Caching layer for HKO API responses
- Rate limiting implementation
- Implement new data sources:
  - Tidal data (astronomical tides, high/low tides)
  - Sun/moon times (sunrise/sunset, moonrise/moonset)
  - Lightning data
  - Visibility data
  - Temperature data (mean, max, min)
  - Weather and radiation reports

### Current Status
- Core functionality complete and operational
- Documentation being finalized
- Ready for production deployment
- Unit test for `test_server.py` fixed and confirmed passing
- Packaging configuration updated to include all tool files

### Known Issues
- No caching means repeated API calls to HKO
- No rate limiting implemented yet
- Limited error handling for HKO API failures
- New data sources not yet implemented

### Evolution of Decisions
- Originally planned database caching → Changed to direct API calls
- Initially only stdio mode → Added SSE support
- Started with English only → Added Chinese language support
- Updated packaging to include subdirectories explicitly

## Project Brief

### Core Requirements
- Provide weather data from Hong Kong Observatory via MCP interface
- Support multiple weather data types (current, forecasts, warnings)
- Offer both stdio and SSE communication modes
- Maintain API compatibility with FastMCP specification

### Goals
- Create reliable weather data service for Hong Kong region
- Enable easy integration with Cline and other MCP clients
- Provide comprehensive weather information in multiple languages
- Ensure high availability and performance

### Scope
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

### Key Stakeholders
- Hong Kong Observatory (data provider)
- Cline integration team
- Weather application developers

### Timeline
- Initial release: v1.0.0 (current)
- Future milestones:
  - Add caching layer
  - Expand to more data sources
  - Implement rate limiting

## System Patterns

### System Architecture
- FastMCP server exposing weather data tools
- Modular design with separate tool implementation for each data type
- REST API client pattern for HKO data access
- Layered architecture:
  1. Interface layer (server.py - FastMCP tools)
  2. Service layer (individual tool files - data processing)
  3. Data layer (HKO API - raw weather data)

### Key Technical Decisions
- Using FastMCP for standardized tool interface
- Direct HTTP calls to HKO API rather than database caching
- Support for both stdio and SSE transport modes
- Language parameter support (en/tc/sc) throughout API
- Modular tool structure with separate files for each weather data type

### Design Patterns in Use
- Adapter pattern: Tool files adapt HKO API to MCP interface
- Facade pattern: Simplified interface to complex weather data
- Singleton pattern: Single FastMCP server instance
- Strategy pattern: Different transport modes (stdio/SSE)

### Component Relationships
- server.py depends on individual tool files for all weather data
- Tool files depend on requests library for HTTP
- Both depend on FastMCP framework
- Independent of specific client implementation

### Critical Implementation Paths
1. Tool registration in server.py
2. HTTP request/response handling in tool files
3. Data transformation from HKO format to MCP format
4. Error handling for API failures
5. Transport mode selection (stdio/SSE)

## Tech Context

### Technologies Used
- Python 3.10+
- FastMCP framework
- Requests library for HTTP calls
- Pytest for testing

### Development Setup
- Python virtual environment recommended
- Install dependencies: `pip install -e .`
- Run tests: `pytest`

### Technical Constraints
- Limited to Hong Kong weather data only
- Requires internet connection to fetch HKO data
- Supports Python 3.10+ only

### Dependencies
- Core:
  - fastmcp>=0.1.0 (MCP protocol implementation)
  - requests>=2.31.0 (HTTP client)
- Development:
  - pytest>=8.2.0 (testing framework)
  - pytest-cov>=6.1.1 (test coverage)

### Tool Usage Patterns
- Run server in stdio mode: `python server.py`
- Run server in SSE mode: `python server.py --sse`
- Run tests: `pytest tests/`
- Build package: `python -m build`