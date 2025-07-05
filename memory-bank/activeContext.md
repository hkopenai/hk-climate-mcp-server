# Active Context

## Current Work Focus
- Fixing unit tests for the server implementation
- Ensuring all project context is properly captured
- Establishing documentation standards for future updates
- Resolving packaging issue with tools directory
- Documenting API handling strategies and error handling aspects for MCP tools

### API Handling Strategies and Error Handling Table
Below is a table listing the tools within the Hong Kong Climate MCP Server, their associated API handling strategy types as defined in the MCP Tool Implementation Principles, key aspects of error handling, and validation status:

| Tool Name                       | API Handling Strategy Type                          | Key Error Handling Aspects                                      | Validated |
|---------------------------------|----------------------------------------------------|-----------------------------------------------------------------|-----------|
| get_current_weather            | Type 1 - Simple Request-Response with Structured Data | Validate response structure, handle HTTP errors, retry on transient issues | No        |
| get_9_day_weather_forecast     | Type 1 - Simple Request-Response with Structured Data | Validate response structure, handle HTTP errors, retry on transient issues | No        |
| get_local_weather_forecast     | Type 1 - Simple Request-Response with Structured Data | Validate response structure, handle HTTP errors, retry on transient issues | No        |
| get_weather_warning_summary    | Type 1 - Simple Request-Response with Structured Data | Validate response structure, handle HTTP errors, retry on transient issues | No        |
| get_weather_warning_info       | Type 1 - Simple Request-Response with Structured Data | Validate response structure, handle HTTP errors, retry on transient issues | No        |
| get_special_weather_tips       | Type 1 - Simple Request-Response with Structured Data | Validate response structure, handle HTTP errors, retry on transient issues | No        |
| get_visibility            | Type 2 - APIs Requiring Data Dictionary Supplement | Enrich data with dictionary, handle missing dictionary data, HTTP errors | No        |
| get_lightning_data             | Type 2 - APIs Requiring Data Dictionary Supplement | Enrich data with dictionary, handle missing dictionary data, HTTP errors | No        |
| get_moon_times                 | Type 2 - APIs Requiring Data Dictionary Supplement | Enrich data with dictionary, handle missing dictionary data, HTTP errors | No        |
| get_hourly_tides               | Type 3 - APIs with Transformable Data Formats (e.g., CSV) | Transform data to JSON, supplement with dictionary, handle format mismatches | No        |
| get_high_low_tides             | Type 3 - APIs with Transformable Data Formats (e.g., CSV) | Transform data to JSON, supplement with dictionary, handle format mismatches | No        |
| get_sunrise_sunset_times       | Type 2 - APIs Requiring Data Dictionary Supplement | Enrich data with dictionary, handle missing dictionary data, HTTP errors | No        |
| get_gregorian_lunar_calendar   | Type 2 - APIs Requiring Data Dictionary Supplement | Enrich data with dictionary, handle missing dictionary data, HTTP errors | No        |
| get_daily_mean_temperature     | Type 3 - APIs with Transformable Data Formats (e.g., CSV) | Transform data to JSON, supplement with dictionary, handle format mismatches | No        |
| get_daily_max_temperature      | Type 3 - APIs with Transformable Data Formats (e.g., CSV) | Transform data to JSON, supplement with dictionary, handle format mismatches | No        |
| get_daily_min_temperature      | Type 3 - APIs with Transformable Data Formats (e.g., CSV) | Transform data to JSON, supplement with dictionary, handle format mismatches | No        |
| get_weather_radiation_report   | Type 4 - APIs Requiring Aggregation from Multiple Calls | Validate response structure, handle HTTP errors, retry on transient issues | Yes       |
| get_valid_station_codes        | Type 1 - Simple Request-Response with Structured Data | Validate response structure, handle HTTP errors, retry on transient issues | No        |

This table serves as a reference for current and future development, ensuring that each tool's API interaction and error handling approach is aligned with the defined principles.

## Recent Changes
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

## Next Steps
- Update progress.md with current project status
- Review all documentation for completeness
- Establish regular memory bank update process

## Active Decisions
- Using standardized markdown format for all documentation
- Maintaining clear separation between different context types
- Prioritizing documentation completeness before adding details

## Important Patterns
- Following hierarchical documentation structure
- Linking related concepts across files
- Using consistent formatting and headers

## Learnings
- Memory bank is crucial for maintaining context
- Documentation should be updated incrementally
- Clear structure makes information easier to find
- Packaging configuration requires explicit inclusion of subdirectories
