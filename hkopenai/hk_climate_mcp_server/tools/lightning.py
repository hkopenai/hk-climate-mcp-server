import requests
from typing import Dict, Any

def get_lightning_data(lang: str = "en") -> Dict[str, Any]:
    """
    Get cloud-to-ground and cloud-to-cloud lightning count data.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing lightning data with fields and data arrays
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LHL&lang={lang}&rformat=json"
    response = requests.get(url)
    try:
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."} 
