"""
Current Weather Data Tools - Functions for fetching current weather data from HKO.

This module provides tools to retrieve current weather information including temperature,
humidity, rainfall, and weather warnings from the Hong Kong Observatory API.
"""

from typing import Dict
import requests
from fastmcp import FastMCP


def register(mcp: FastMCP):
    """Registers the current weather tool with the FastMCP server."""
    @mcp.tool(
        description="Get current weather data, warnings, temp, humidity in HK from HKO.",
    )
    def get_current_weather(
        region: str = "Hong Kong Observatory", lang: str = "en"
    ) -> Dict:
        """
        Get current weather observations for a specific region in Hong Kong

        Args:
            region: The region to get weather for (default: "Hong Kong Observatory")
            lang: Language code (en/tc/sc, default: en)

        Returns:
            Dict containing:
            - warning: Current weather warnings
            - temperature: Current temperature in Celsius
            - humidity: Current humidity percentage
            - rainfall: Current rainfall in mm
        """
        return _get_current_weather(region, lang)


def _get_current_weather(
    region: str = "Hong Kong Observatory", lang: str = "en"
) -> Dict:
    """
    Get current weather observations for a specific region in Hong Kong

    Args:
        region: The region to get weather for (default: "Hong Kong Observatory")
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
        - warning: Current weather warnings
        - temperature: Current temperature in Celsius
        - humidity: Current humidity percentage
        - rainfall: Current rainfall in mm
    """
    response = requests.get(
        f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
        f"?dataType=rhrread&lang={lang}"
    )
    data = response.json()

    # Handle warnings
    warning = "No warning in force"
    if "warningMessage" in data:
        if isinstance(data["warningMessage"], list) and data["warningMessage"]:
            warning = data["warningMessage"][0]
        elif data["warningMessage"]:
            warning = data["warningMessage"]

    # Get default values from HKO data
    default_temp = next(
        (
            t
            for t in data.get("temperature", {}).get("data", [])
            if t.get("place") == "Hong Kong Observatory"
        ),
        {"value": 25, "unit": "C", "recordTime": ""},
    )
    default_humidity = next(
        (
            h
            for h in data.get("humidity", {}).get("data", [])
            if h.get("place") == "Hong Kong Observatory"
        ),
        {"value": 60, "unit": "percent", "recordTime": ""},
    )
    # Find matching region temperature
    temp_data = data.get("temperature", {}).get("data", [])
    matched_temp = next(
        (t for t in temp_data if t["place"].lower() == region.lower()),
        {
            "place": "Hong Kong Observatory",
            "value": default_temp["value"],
            "unit": default_temp["unit"],
        },
    )
    matched_temp["recordTime"] = data["temperature"]["recordTime"]

    # Get humidity
    humidity = next(
        (
            h
            for h in data.get("humidity", {}).get("data", [])
            if h.get("place") == matched_temp["place"]
        ),
        default_humidity,
    )
    humidity["recordTime"] = data["humidity"]["recordTime"]

    # Get rainfall (0 if no rain)
    rainfall = 0
    rainfall_start = ""
    rainfall_end = ""
    if "rainfall" in data:
        rainfall = max(float(r.get("max", 0)) for r in data["rainfall"]["data"])
        rainfall_start = data["rainfall"]["startTime"]
        rainfall_end = data["rainfall"]["endTime"]

    return {
        "generalSituation": warning,
        "weatherObservation": {
            "temperature": {
                "value": matched_temp["value"],
                "unit": matched_temp["unit"],
                "recordTime": matched_temp["recordTime"],
                "place": matched_temp["place"],
            },
            "humidity": {
                "value": humidity["value"],
                "unit": humidity["unit"],
                "recordTime": humidity["recordTime"],
                "place": matched_temp["place"],
            },
            "rainfall": {
                "value": rainfall,
                "min": min(float(r.get("min", 0)) for r in data["rainfall"]["data"]),
                "unit": "mm",
                "startTime": rainfall_start,
                "endTime": rainfall_end,
            },
            "uvindex": data.get("uvindex", {}),
        },
        "updateTime": data["updateTime"],
        "icon": data.get("icon", []),
        "iconUpdateTime": data.get("iconUpdateTime", ""),
    }
