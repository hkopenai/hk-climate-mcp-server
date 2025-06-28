import requests
from typing import Dict, Any, Optional

# Station names for tide data in different languages: en (English), tc (Traditional Chinese), sc (Simplified Chinese)
VALID_TIDE_STATIONS = {
    'en': {
        'CCH': 'Cheung Chau',
        'CLK': 'Chek Lap Kok',
        'CMW': 'Chi Ma Wan',
        'KCT': 'Kwai Chung',
        'KLW': 'Ko Lau Wan',
        'LOP': 'Lok On Pai',
        'MWC': 'Ma Wan',
        'QUB': 'Quarry Bay',
        'SPW': 'Shek Pik',
        'TAO': 'Tai O',
        'TBT': 'Tsim Bei Tsui',
        'TMW': 'Tai Miu Wan',
        'TPK': 'Tai Po Kau',
        'WAG': 'Waglan Island'
    },
    'tc': {
        'CCH': '長洲',
        'CLK': '赤鱲角',
        'CMW': '芝麻灣',
        'KCT': '葵涌',
        'KLW': '高流灣',
        'LOP': '樂安排',
        'MWC': '馬灣',
        'QUB': '鰂魚涌',
        'SPW': '石壁',
        'TAO': '大澳',
        'TBT': '尖鼻咀',
        'TMW': '大廟灣',
        'TPK': '大埔滘',
        'WAG': '橫瀾島'
    },
    'sc': {
        'CCH': '长洲',
        'CLK': '赤鱲角',
        'CMW': '芝麻湾',
        'KCT': '葵涌',
        'KLW': '高流湾',
        'LOP': '乐安排',
        'MWC': '马湾',
        'QUB': '鲗鱼涌',
        'SPW': '石壁',
        'TAO': '大澳',
        'TBT': '尖鼻咀',
        'TMW': '大庙湾',
        'TPK': '大埔滘',
        'WAG': '横澜岛'
    }
}

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
    try:
        response.raise_for_status()
        # Decode response content with utf-8-sig to handle potential BOM
        content = response.content.decode('utf-8-sig')
        import json
        return json.loads(content)
    except (requests.RequestException, UnicodeDecodeError, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}

def get_tide_station_codes(lang: str = "en") -> Dict[str, str]:
    """
    Get a dictionary of station codes and their corresponding names for tide reports in Hong Kong.
    
    Args:
        lang: Language code (en/tc/sc, default: en)
    
    Returns:
        Dict mapping station codes to station names in the specified language.
    """
    # Return the dictionary for the specified language, default to English
    return VALID_TIDE_STATIONS.get(lang, VALID_TIDE_STATIONS['en'])

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
        Dict containing tide data with fields and data arrays or an error message if station is invalid
    """
    # Select the station dictionary based on the language, default to English
    stations_dict = VALID_TIDE_STATIONS.get(lang, VALID_TIDE_STATIONS['en'])
    
    if not station or station not in stations_dict:
        return {"error": "Invalid or missing station code. Use the 'get_tide_station_codes' tool to retrieve the list of valid station codes."}
        
    params = {
        'dataType': 'HLT',
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
    try:
        response.raise_for_status()
        # Decode response content with utf-8-sig to handle potential BOM
        content = response.content.decode('utf-8-sig')
        import json
        return json.loads(content)
    except (requests.RequestException, UnicodeDecodeError, ValueError) as e:
        return {"error": f"Failed to fetch data: {str(e)}."}
