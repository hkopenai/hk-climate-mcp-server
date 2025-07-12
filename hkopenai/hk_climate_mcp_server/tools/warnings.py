"""
Weather Warnings Tools - Functions for fetching weather warning data from HKO.

This module provides tools to retrieve weather warning information from
the Hong Kong Observatory API.
"""

from typing import Dict, Any
import requests
from fastmcp import FastMCP


def register(mcp: FastMCP):
    """Registers the weather warnings tools with the FastMCP server."""
    @mcp.tool(
        description="Get weather warning summary for HK with messages and update.",
    )
    def get_weather_warning_summary(lang: str = "en") -> Dict[str, Any]:
        return _get_weather_warning_summary(lang)


    @mcp.tool(
        description="Get detailed weather warning info for HK with statement and update.",
    )
    def get_weather_warning_info(lang: str = "en") -> Dict[str, Any]:
        return _get_weather_warning_info(lang)


    @mcp.tool(
        description="Get special weather tips for Hong Kong including tips list and update.",
    )
    def get_special_weather_tips(lang: str = "en") -> Dict[str, Any]:
        return _get_special_weather_tips(lang)


def _get_weather_warning_summary(lang: str = "en") -> Dict[str, Any]:
    """
    Get weather warning summary for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - warningMessage: List of warning messages
            - updateTime: Last update time
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang={lang}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}

    return {
        "warningMessage": data.get("warningMessage", []),
        "updateTime": data.get("updateTime", ""),
    }


def _get_weather_warning_info(lang: str = "en") -> Dict[str, Any]:
    """
    Get detailed weather warning information for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - warningStatement: Warning statement
            - updateTime: Last update time
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang={lang}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}

    return {
        "warningStatement": data.get("warningStatement", ""),
        "updateTime": data.get("updateTime", ""),
    }


def _get_special_weather_tips(lang: str = "en") -> Dict[str, Any]:
    """
    Get special weather tips for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - specialWeatherTips: List of special weather tips
            - updateTime: Last update time
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=swt&lang={lang}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}

    return {
        "specialWeatherTips": data.get("specialWeatherTips", []),
        "updateTime": data.get("updateTime", ""),
    }
