# HKO MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/hkopenai/hk-climate-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This is an MCP server that provides access to climate and weather data through a FastMCP interface.

## Data Source

* Hong Kong Observatory 

## Features

- Current weather: Get current weather observations from HKO (supports optional region parameter)
- 9-day forecast: Get extended weather forecast including general situation, daily forecasts, sea and soil temperatures
- Local weather forecast: Get short-term weather forecast with outlook
- Weather warnings: Get summary and detailed information about active weather warnings
- Special weather tips: Get important weather-related safety tips

## API Reference

### Current Weather
`get_current_weather(region: str = "Hong Kong Observatory") -> Dict`
- Get current weather observations for a specific region in Hong Kong
- Parameters:
  - region: The region to get weather for (default: "Hong Kong Observatory")
- Returns:
  - Dict containing:
    - warning: Current weather warnings
    - temperature: Current temperature in Celsius
    - humidity: Current humidity percentage
    - rainfall: Current rainfall in mm

### 9-Day Weather Forecast
`get_9_day_weather_forecast(lang: str = "en") -> Dict`
- Get the 9-day weather forecast for Hong Kong
- Parameters:
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing:
    - generalSituation: General weather situation
    - weatherForecast: List of daily forecast dicts
    - updateTime: Last update time
    - seaTemp: Sea temperature info
    - soilTemp: List of soil temperature info

### Local Weather Forecast  
`get_local_weather_forecast(lang: str = "en") -> Dict`
- Get local weather forecast for Hong Kong
- Parameters:
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing:
    - forecastDesc: Forecast description
    - outlook: Outlook forecast
    - updateTime: Last update time
    - forecastPeriod: Forecast period
    - forecastDate: Forecast date

### Weather Warning Summary
`get_weather_warning_summary(lang: str = "en") -> Dict`
- Get weather warning summary for Hong Kong
- Parameters:
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing:
    - warningMessage: List of warning messages
    - updateTime: Last update time

### Weather Warning Information
`get_weather_warning_info(lang: str = "en") -> Dict`
- Get detailed weather warning information
- Parameters:
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing:
    - warningStatement: Warning statement
    - updateTime: Last update time

### Special Weather Tips
`get_special_weather_tips(lang: str = "en") -> Dict`
- Get special weather tips for Hong Kong
- Parameters:
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing:
    - specialWeatherTips: List of special weather tips
    - updateTime: Last update time

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
       "-m",
      "hkopenai.hk-climate-mcp-server"
    ]
  }
}
```

## Testing

Tests are available in `tests`. Run with:
```bash
pytest
