import requests
from typing import Dict, Any

def get_visibility_data(lang: str = "en") -> Dict[str, Any]:
    """
    Get latest 10-minute mean visibility data for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing visibility data with fields and data arrays
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LTMV&lang={lang}&rformat=json"
    response = requests.get(url)
    return response.json()