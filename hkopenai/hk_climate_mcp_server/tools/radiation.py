import requests
from typing import Dict, Any, Optional

def get_weather_radiation_report(
    date: Optional[str] = None,
    station: Optional[str] = None,
    lang: str = "en",
    rformat: str = "json"
) -> Dict[str, Any]:
    """
    Get weather and radiation level report for Hong Kong.

    Args:
        date: Optional date in YYYYMMDD format (default: yesterday)
        station: Optional station code (e.g. 'HKO' for Hong Kong Observatory)
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing weather and radiation data
    """
    params = {
        'dataType': 'RYES',
        'lang': lang,
        'rformat': rformat
    }
    if date: params['date'] = date
    if station: params['station'] = station

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}
