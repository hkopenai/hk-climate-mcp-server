"""
Visibility Data Tools - Functions for fetching visibility data from HKO.

This module provides tools to retrieve visibility data from the Hong Kong Observatory API.
"""

from typing import Dict, Any
from fastmcp import FastMCP
from hkopenai_common.json_utils import fetch_json_data


def register(mcp: FastMCP):
    """Registers the visibility data tool with the FastMCP server."""

    @mcp.tool(
        description="Get latest 10-minute mean visibility data for Hong Kong",
    )
    def get_visibility(lang: str = "en") -> Dict[str, Any]:
        """
        Get latest 10-minute mean visibility data for Hong Kong.

        Args:
            lang: Language code (en/tc/sc, default: en)

        Returns:
            Dict containing visibility data with fields and data arrays
        """
        return _get_visibility(lang=lang)


def _get_visibility(lang: str = "en") -> Dict[str, Any]:
    """
    Get latest 10-minute mean visibility data for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing visibility data with fields and data arrays
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LTMV&lang={lang}&rformat=json"
    return fetch_json_data(url)
