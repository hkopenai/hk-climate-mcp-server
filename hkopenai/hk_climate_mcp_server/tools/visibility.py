"""
Visibility Data Tools - Functions for fetching visibility data from HKO.

This module provides tools to retrieve visibility data from the Hong Kong Observatory API.
"""

from typing import Dict, Any
import requests


def get_visibility(lang: str = "en") -> Dict[str, Any]:
    """
    Get latest 10-minute mean visibility data for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing visibility data with fields and data arrays
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LTMV&lang={lang}&rformat=json"
    response = requests.get(url)
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}
