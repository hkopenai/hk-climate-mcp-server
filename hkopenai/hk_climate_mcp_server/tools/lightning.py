"""
Lightning Data Tools - Functions for fetching lightning data from HKO.

This module provides tools to retrieve lightning data including cloud-to-ground
and cloud-to-cloud lightning counts from the Hong Kong Observatory API.
"""

from typing import Dict, Any
import requests
from fastmcp import FastMCP


def register(mcp: FastMCP):
    """Registers the lightning data tool with the FastMCP server."""
    @mcp.tool(
        description="Get cloud-to-ground and cloud-to-cloud lightning count data",
    )
    def get_lightning_data(lang: str = "en") -> Dict[str, Any]:
        return _get_lightning_data(lang)


def _get_lightning_data(lang: str = "en") -> Dict[str, Any]:
    """
    Get cloud-to-ground and cloud-to-cloud lightning count data.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing lightning data with fields and data arrays
    """
    url = (
        f"https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"
        f"?dataType=LHL&lang={lang}&rformat=json"
    )
    response = requests.get(url)
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}
