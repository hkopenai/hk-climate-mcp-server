import requests
from typing import Dict, Any

def get_lightning_data(lang: str = "en", rformat: str = "json") -> Dict[str, Any]:
    """
    Get cloud-to-ground and cloud-to-cloud lightning count data.

    Args:
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing lightning data with fields and data arrays
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LHL&lang={lang}&rformat={rformat}"
    response = requests.get(url)
    return response.json() if rformat == "json" else {"data": response.text}
