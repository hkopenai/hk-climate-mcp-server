"""
HKO MCP Server - A server for handling weather data requests using the Model Context Protocol (MCP).

This module provides a server implementation for accessing various weather data tools
from the Hong Kong Observatory through the MCP protocol. It supports both HTTP and stdio
transports for communication.
"""

import argparse
from typing import Dict, Annotated, Optional
from pydantic import Field
from fastmcp import FastMCP
from hkopenai.hk_climate_mcp_server.tools import astronomical
from hkopenai.hk_climate_mcp_server.tools import current_weather
from hkopenai.hk_climate_mcp_server.tools import forecast
from hkopenai.hk_climate_mcp_server.tools import lightning
from hkopenai.hk_climate_mcp_server.tools import radiation
from hkopenai.hk_climate_mcp_server.tools import temperature
from hkopenai.hk_climate_mcp_server.tools import tides
from hkopenai.hk_climate_mcp_server.tools import visibility
from hkopenai.hk_climate_mcp_server.tools import warnings

def create_mcp_server():
    """Create and configure the HKO MCP server"""
    mcp = FastMCP(name="HKOServer")

    @mcp.tool(
        description="Get current weather data, warnings, temp, humidity in HK from HKO.",
    )
    def get_current_weather(region: str = "Hong Kong Observatory") -> Dict:
        return current_weather.get_current_weather(region)

    @mcp.tool(
        description="Get 9-day weather forecast for HK with general situation, daily data.",
    )
    def get_9_day_weather_forecast(lang: str = "en") -> Dict:
        return forecast.get_9_day_weather_forecast(lang)

    @mcp.tool(
        description="Get local weather forecast for HK with description, outlook, update.",
    )
    def get_local_weather_forecast(lang: str = "en") -> Dict:
        return forecast.get_local_weather_forecast(lang)

    @mcp.tool(
        description="Get weather warning summary for HK with messages and update.",
    )
    def get_weather_warning_summary(lang: str = "en") -> Dict:
        return warnings.get_weather_warning_summary(lang)

    @mcp.tool(
        description="Get detailed weather warning info for HK with statement and update.",
    )
    def get_weather_warning_info(lang: str = "en") -> Dict:
        return warnings.get_weather_warning_info(lang)

    @mcp.tool(
        description="Get special weather tips for Hong Kong including tips list and update.",
    )
    def get_special_weather_tips(lang: str = "en") -> Dict:
        return warnings.get_special_weather_tips(lang)

    @mcp.tool(
        description="Get latest 10-minute mean visibility data for Hong Kong",
    )
    def get_visibility_data(lang: str = "en") -> Dict:
        return visibility.get_visibility_data(lang)

    @mcp.tool(
        description="Get cloud-to-ground and cloud-to-cloud lightning count data",
    )
    def get_lightning_data(lang: str = "en") -> Dict:
        return lightning.get_lightning_data(lang)

    @mcp.tool(
        description="Get times of moonrise, moon transit and moonset",
    )
    def get_moon_times(
        year: int,
        month: Optional[int] = None,
        day: Optional[int] = None,
        lang: str = "en"
    ) -> Dict:
        return astronomical.get_moon_times(
            year=year,
            month=month,
            day=day,
            lang=lang
        )

    @mcp.tool(
        description="Get hourly heights of astronomical tides for a station in HK.",
    )
    def get_hourly_tides(
        station: str,
        year: int,
        options: Optional[Dict] = None
    ) -> Dict:
        params = {
            "station": station,
            "year": year,
            "month": None,
            "day": None,
            "hour": None,
            "lang": "en"
        }
        if options:
            params.update(options)
        return tides.get_hourly_tides(**params)

    @mcp.tool(
        description="Get times, heights of astronomical high/low tides for a station in HK.",
    )
    def get_high_low_tides(
        station: str,
        year: int,
        options: Optional[Dict] = None
    ) -> Dict:
        params = {
            "station": station,
            "year": year,
            "month": None,
            "day": None,
            "hour": None,
            "lang": "en"
        }
        if options:
            params.update(options)
        return tides.get_high_low_tides(**params)

    @mcp.tool(
        description="Get list of tide station codes and names for tide reports in HK.",
    )
    def get_tide_station_codes(lang: str = "en") -> Dict:
        return tides.get_tide_station_codes(lang)

    @mcp.tool(
        description="Get times of sunrise, sun transit and sunset for Hong Kong",
    )
    def get_sunrise_sunset_times(
        year: int,
        month: Optional[int] = None,
        day: Optional[int] = None,
        lang: str = "en"
    ) -> Dict:
        return astronomical.get_sunrise_sunset_times(
            year=year,
            month=month,
            day=day,
            lang=lang
        )

    @mcp.tool(
        description="Get Gregorian-Lunar calendar conversion data",
    )
    def get_gregorian_lunar_calendar(
        year: int,
        month: Optional[int] = None,
        day: Optional[int] = None,
        lang: str = "en"
    ) -> Dict:
        return astronomical.get_gregorian_lunar_calendar(
            year=year,
            month=month,
            day=day,
            lang=lang
        )

    @mcp.tool(
        description="Get daily mean temperature data for a specific station in Hong Kong",
    )
    def get_daily_mean_temperature(
        station: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        lang: str = "en"
    ) -> Dict:
        return temperature.get_daily_mean_temperature(
            station=station,
            year=year,
            month=month,
            lang=lang
        )

    @mcp.tool(
        description="Get daily maximum temperature data for a specific station in Hong Kong",
    )
    def get_daily_max_temperature(
        station: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        lang: str = "en"
    ) -> Dict:
        return temperature.get_daily_max_temperature(
            station=station,
            year=year,
            month=month,
            lang=lang
        )

    @mcp.tool(
        description="Get daily minimum temperature data for a specific station in Hong Kong",
    )
    def get_daily_min_temperature(
        station: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        lang: str = "en"
    ) -> Dict:
        return temperature.get_daily_min_temperature(
            station=station,
            year=year,
            month=month,
            lang=lang
        )

    @mcp.tool(
        description="Get weather, radiation report for HK. Date must be YYYYMMDD.",
    )
    def get_weather_radiation_report(
        date: Annotated[str, Field(description="Date in yyyyMMdd format, e.g., 20250618")],
        station: Annotated[str, Field(description="Station code in 3 caps letters, e.g., HKO")],
        lang: Annotated[Optional[str], Field(description="Language (en/tc/sc)")] = 'en',
    ) -> Dict:
        return radiation.get_weather_radiation_report(
            date=date,
            station=station,
            lang=lang or 'en'
        )

    @mcp.tool(
        description="Get list of weather station codes and names for radiation reports in HK.",
    )
    def get_radiation_station_codes(lang: str = "en") -> Dict:
        return radiation.get_radiation_station_codes(lang)
    return mcp

def main(args):
    """
    Main function to run the HKO MCP Server.
    
    Args:
        args: Command line arguments passed to the function.
    """
    parser = argparse.ArgumentParser(description='HKO MCP Server')
    parser.add_argument('-s', '--sse', action='store_true',
                       help='Run in SSE mode instead of stdio')
    parser.add_argument('-p', '--port', type=int, default=8000,
                       help='Port to run the server on (default: 8000)')
    args = parser.parse_args()

    print(f"[DEBUG] Parsed arguments: {args}")
    server = create_mcp_server()
    if args.sse:
        server.run(transport="streamable-http", port=args.port)
        print(f"HKO MCP Server running in SSE mode on port {args.port}")
    else:
        server.run()
        print("HKO MCP Server running in stdio mode")
