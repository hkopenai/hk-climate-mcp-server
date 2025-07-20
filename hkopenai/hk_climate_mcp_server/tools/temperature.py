"""
Temperature Data Tools - Functions for fetching temperature data from HKO.

This module provides tools to retrieve temperature data including daily mean,
maximum, and minimum temperatures from the Hong Kong Observatory API.
"""

from typing import Dict, Any, Optional
from fastmcp import FastMCP
from hkopenai_common.json_utils import fetch_json_data


def register(mcp: FastMCP):
    """Registers the temperature data tools with the FastMCP server."""

    @mcp.tool(
        description="Get daily mean temperature data for a specific station in Hong Kong",
    )
    def get_daily_mean_temperature(
        station: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        lang: str = "en",
    ) -> Dict[str, Any]:
        return _get_daily_mean_temperature(
            station=station, year=year, month=month, lang=lang
        )

    @mcp.tool(
        description="Get daily maximum temperature data for a specific station in Hong Kong",
    )
    def get_daily_max_temperature(
        station: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        lang: str = "en",
    ) -> Dict[str, Any]:
        return _get_daily_max_temperature(
            station=station, year=year, month=month, lang=lang
        )

    @mcp.tool(
        description="Get daily minimum temperature data for a specific station in Hong Kong",
    )
    def get_daily_min_temperature(
        station: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        lang: str = "en",
    ) -> Dict[str, Any]:
        return _get_daily_min_temperature(
            station=station, year=year, month=month, lang=lang
        )


def _get_daily_mean_temperature(
    station: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    lang: str = "en",
) -> Dict[str, Any]:
    """
    Get daily mean temperature data for a specific station.

    Args:
        station: Station code (e.g. 'HKO' for Hong Kong Observatory)
        year: Optional year (varies by station)
        month: Optional month (1-12)
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing temperature data with fields and data arrays
    """
    params = {
        "dataType": "CLMTEMP",
        "lang": lang,
        "rformat": "json",
        "station": station,
    }
    if year:
        params["year"] = str(year)
    if month:
        params["month"] = str(month)

    return fetch_json_data(
        "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php", params=params
    )


def _get_daily_max_temperature(
    station: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    lang: str = "en",
) -> Dict[str, Any]:
    """
    Get daily maximum temperature data for a specific station.

    Args:
        station: Station code (e.g. 'HKO' for Hong Kong Observatory)
        year: Optional year (varies by station)
        month: Optional month (1-12)
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing temperature data with fields and data arrays
    """
    params = {
        "dataType": "CLMMAXT",
        "lang": lang,
        "rformat": "json",
        "station": station,
    }
    if year:
        params["year"] = str(year)
    if month:
        params["month"] = str(month)

    return fetch_json_data(
        "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php", params=params
    )


def _get_daily_min_temperature(
    station: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    lang: str = "en",
) -> Dict[str, Any]:
    """
    Get daily minimum temperature data for a specific station.

    Args:
        station: Station code (e.g. 'HKO' for Hong Kong Observatory)
        year: Optional year (varies by station)
        month: Optional month (1-12)
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing temperature data with fields and data arrays
    """
    params = {
        "dataType": "CLMMINT",
        "lang": lang,
        "rformat": "json",
        "station": station,
    }
    if year:
        params["year"] = str(year)
    if month:
        params["month"] = str(month)

    return fetch_json_data(
        "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php", params=params
    )
