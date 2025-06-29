import requests
from typing import Dict, Any, Optional

def get_daily_mean_temperature(
    station: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    lang: str = "en"
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
        'dataType': 'CLMTEMP',
        'lang': lang,
        'rformat': 'json',
        'station': station
    }
    if year: params['year'] = str(year)
    if month: params['month'] = str(month)

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}

def get_daily_max_temperature(
    station: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    lang: str = "en"
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
        'dataType': 'CLMMAXT',
        'lang': lang,
        'rformat': 'json',
        'station': station
    }
    if year: params['year'] = str(year)
    if month: params['month'] = str(month)

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}

def get_daily_min_temperature(
    station: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    lang: str = "en"
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
        'dataType': 'CLMMINT',
        'lang': lang,
        'rformat': 'json',
        'station': station
    }
    if year: params['year'] = str(year)
    if month: params['month'] = str(month)

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}
