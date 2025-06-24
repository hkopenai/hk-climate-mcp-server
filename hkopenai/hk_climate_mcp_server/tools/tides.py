import requests
from typing import Dict, Any, Optional

def get_hourly_tides(
    station: str,
    year: int,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    lang: str = "en"
) -> Dict[str, Any]:
    """
    Get hourly heights of astronomical tides for a specific station in Hong Kong.

    Args:
        station: Station code (e.g. 'CCH' for Cheung Chau)
        year: Year (2022-2024)
        month: Optional month (1-12)
        day: Optional day (1-31)
        hour: Optional hour (1-24)
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing tide data with fields and data arrays
    """
    params = {
        'dataType': 'HHOT',
        'lang': lang,
        'rformat': 'json',
        'station': station,
        'year': year
    }
    if month: params['month'] = str(month)
    if day: params['day'] = str(day)
    if hour: params['hour'] = str(hour)

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() 

def get_high_low_tides(
    station: str,
    year: int,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    lang: str = "en",
) -> Dict[str, Any]:
    """
    Get times and heights of astronomical high and low tides for a specific station.

    Args:
        station: Station code (e.g. 'CCH' for Cheung Chau)
        year: Year (2022-2024)
        month: Optional month (1-12)
        day: Optional day (1-31)
        hour: Optional hour (1-24)
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing tide data with fields and data arrays
    """
    params = {
        'dataType': 'HLT',
        'lang': lang,
        'station': station,
        'year': year
    }
    if month: params['month'] = str(month)
    if day: params['day'] = str(day)
    if hour: params['hour'] = str(hour)

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() 