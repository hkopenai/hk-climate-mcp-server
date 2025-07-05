# HK Climate and Weather MCP Server

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

### Visibility Data
`get_visibility(lang: str = "en") -> Dict`
- Get latest 10-minute mean visibility data for Hong Kong
- Parameters:
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing visibility data with fields and data arrays

### Lightning Data  
`get_lightning_data(lang: str = "en") -> Dict`
- Get cloud-to-ground and cloud-to-cloud lightning count data
- Parameters:
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing lightning data with fields and data arrays

### Moon Times
`get_moon_times(year: int, month: Optional[int] = None, day: Optional[int] = None, lang: str = "en") -> Dict`
- Get times of moonrise, moon transit and moonset
- Parameters:
  - year: Year (2018-2024)
  - month: Optional month (1-12)
  - day: Optional day (1-31)
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing moon times data with fields and data arrays

### Hourly Tides
`get_hourly_tides(station: str, year: int, month: Optional[int] = None, day: Optional[int] = None, hour: Optional[int] = None, lang: str = "en") -> Dict`
- Get hourly heights of astronomical tides for a specific station
- Parameters:
  - station: Station code (e.g. 'CCH' for Cheung Chau)
  - year: Year (2022-2024)
  - month: Optional month (1-12)
  - day: Optional day (1-31)
  - hour: Optional hour (1-24)
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing tide data with fields and data arrays

### High/Low Tides
`get_high_low_tides(station: str, year: int, month: Optional[int] = None, day: Optional[int] = None, hour: Optional[int] = None, lang: str = "en") -> Dict`
- Get times and heights of astronomical high and low tides
- Parameters:
  - station: Station code (e.g. 'CCH' for Cheung Chau)
  - year: Year (2022-2024)
  - month: Optional month (1-12)
  - day: Optional day (1-31)
  - hour: Optional hour (1-24)
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing tide data with fields and data arrays

### Weather and Radiation Report
`get_weather_radiation_report(date: str, station: str, lang: str = "en") -> Dict`
- Get weather and radiation level report for Hong Kong
- Parameters:
  - date: Mandatory date in YYYYMMDD format (e.g., 20250618)
  - station: Mandatory station code (e.g., 'HKO' for Hong Kong Observatory)
  - lang: Language code (en/tc/sc, default: en)
- Returns:
  - Dict containing weather and radiation data or error message if parameters are invalid

### Station Codes
`get_radiation_station_codes() -> Dict`
- Get a list of station codes and their corresponding names for weather and radiation reports in Hong Kong
- Parameters:
  - None
- Returns:
  - Dict mapping station codes to station names

## Setup

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```

### Running Options

- Default stdio mode: `python server.py`
- SSE mode (port 8000): `python server.py --sse`

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
      "hkopenai.hk_climate_mcp_server"
    ]
  }
}
```

## Testing

Tests are available in `tests`. Run with:
```bash
pytest
