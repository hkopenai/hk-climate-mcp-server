import requests
from typing import Dict, Any, Optional

def get_moon_times(year: int, month: Optional[int] = None, 
                  day: Optional[int] = None, lang: str = "en") -> Dict[str, Any]:
    """
    Get times of moonrise, moon transit and moonset.

    Args:
        year: Year (2018-2024)
        month: Optional month (1-12)
        day: Optional day (1-31)
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing moon times data with fields and data arrays
    """
    params = {
        'dataType': 'MRS',
        'lang': lang,
        'rformat': 'json',
        'year': year
    }
    if month: params['month'] = str(month)
    if day: params['day'] = str(day)

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}

def get_sunrise_sunset_times(
    year: int,
    month: Optional[int] = None,
    day: Optional[int] = None,
    lang: str = "en"
) -> Dict[str, Any]:
    """
    Get times of sunrise, sun transit and sunset.

    Args:
        year: Year (2018-2024)
        month: Optional month (1-12)
        day: Optional day (1-31)
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing sun times data with fields and data arrays
    """
    params = {
        'dataType': 'SRS',
        'lang': lang,
        'rformat': 'json',
        'year': year
    }
    if month: params['month'] = str(month)
    if day: params['day'] = str(day)

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}

def get_gregorian_lunar_calendar(
    year: int,
    month: Optional[int] = None,
    day: Optional[int] = None,
    lang: str = "en"
) -> Dict[str, Any]:
    """
    Get Gregorian-Lunar calendar conversion data.

    Args:
        year: Year (1901-2100)
        month: Optional month (1-12)
        day: Optional day (1-31)
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing calendar conversion data
    """
    params = {
        'dataType': 'GLC',
        'lang': lang,
        'rformat': 'json',
        'year': year
    }
    if month: params['month'] = str(month)
    if day: params['day'] = str(day)

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}