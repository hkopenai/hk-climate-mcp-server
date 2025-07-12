"""
Weather Forecast Tools - Functions for fetching weather forecast data from HKO.

This module provides tools to retrieve weather forecast information including
9-day and local weather forecasts from the Hong Kong Observatory API.
"""

from typing import Dict, Any
import requests
from fastmcp import FastMCP


def register(mcp: FastMCP):
    """Registers the forecast tools with the FastMCP server."""
    @mcp.tool(
        description="Get 9-day weather forecast for HK with general situation, daily data.",
    )
    def get_9_day_weather_forecast(lang: str = "en") -> Dict[str, Any]:
        return _get_9_day_weather_forecast(lang)

    @mcp.tool(
        description="Get local weather forecast for HK with description, outlook, update.",
    )
    def get_local_weather_forecast(lang: str = "en") -> Dict[str, Any]:
        return _get_local_weather_forecast(lang)


def _get_9_day_weather_forecast(lang: str = "en") -> Dict[str, Any]:
    """
    Get the 9-day weather forecast for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - generalSituation: General weather situation
            - weatherForecast: List of daily forecast dicts with details like date, week, wind,
              weather, temp, humidity, etc.
            - updateTime: Last update time
            - seaTemp: Sea temperature info
            - soilTemp: List of soil temperature info
    """
    base_url = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
    url = f"{base_url}?dataType=fnd&lang={lang}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}

    # Structure the output
    forecast = {
        "generalSituation": data.get("generalSituation", ""),
        "weatherForecast": [],
        "updateTime": data.get("updateTime", ""),
        "seaTemp": data.get("seaTemp", {}),
        "soilTemp": data.get("soilTemp", []),
    }

    # Extract 9-day forecast
    for day in data.get("weatherForecast", []):
        forecast["weatherForecast"].append(
            {
                "forecastDate": day.get("forecastDate", ""),
                "week": day.get("week", ""),
                "forecastWind": day.get("forecastWind", ""),
                "forecastWeather": day.get("forecastWeather", ""),
                "forecastMaxtemp": day.get("forecastMaxtemp", {}),
                "forecastMintemp": day.get("forecastMintemp", {}),
                "forecastMaxrh": day.get("forecastMaxrh", {}),
                "forecastMinrh": day.get("forecastMinrh", {}),
                "ForecastIcon": day.get("ForecastIcon", ""),
                "PSR": day.get("PSR", ""),
            }
        )
    return forecast


def _get_local_weather_forecast(lang: str = "en") -> Dict[str, Any]:
    """
    Get local weather forecast for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - forecastDesc: Forecast description
            - outlook: Outlook forecast
            - updateTime: Last update time
            - forecastPeriod: Forecast period
            - forecastDate: Forecast date
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang={lang}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}
    return {
        "generalSituation": data.get("generalSituation", ""),
        "forecastDesc": data.get("forecastDesc", ""),
        "outlook": data.get("outlook", ""),
        "updateTime": data.get("updateTime", ""),
        "forecastPeriod": data.get("forecastPeriod", ""),
        "forecastDate": data.get("forecastDate", ""),
    }
