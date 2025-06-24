import requests
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

def get_weather_radiation_report(
    date: str = "Unknown",
    station: str = "Unknown",
    lang: str = "en",
    rformat: str = "json"
) -> Dict[str, Any]:
    """
    Get weather and radiation level report for Hong Kong.

    Args:
        date: Mandatory date in YYYYMMDD format (e.g., 20250618)
        station: Mandatory station code (e.g., 'HKO' for Hong Kong Observatory). 
                 If not provided or invalid, returns a list of valid station codes.
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing weather and radiation data or a list of valid station codes if station is invalid
    """
    valid_stations = {
        'CCH': 'Cheung Chau',
        'CLK': 'Chek Lap Kok',
        'EPC': 'Ping Chau',
        'HKO': 'Hong Kong Observatory',
        'HKP': 'Hong Kong Park',
        'HKS': 'Wong Chuk Hang',
        'HPV': 'Happy Valley',
        'JKB': 'Tseung Kwan O',
        'KAT': 'Kat O',
        'KLT': 'Kowloon City',
        'KP': 'Kings Park',
        'KTG': 'Kwun Tong',
        'LFS': 'Lau Fau Shan',
        'PLC': 'Tai Mei Tuk',
        'SE1': 'Kai Tak Runway Park',
        'SEK': 'Shek Kong',
        'SHA': 'Sha Tin',
        'SKG': 'Sai Kung',
        'SKW': 'Shau Kei Wan',
        'SSP': 'Sham Shui Po',
        'STK': 'Sha Tau Kok',
        'STY': 'Stanley',
        'SWH': 'Sai Wan Ho',
        'TAP': 'Tap Mun',
        'TBT': 'Tsim Bei Tsui',
        'TKL': 'Ta Kwu Ling',
        'TUN': 'Tuen Mun',
        'TW': 'Tsuen Wan Shing Mun Valley',
        'TWN': 'Tsuen Wan Ho Koon',
        'TY1': 'Tsing Yi',
        'WTS': 'Wong Tai Sin',
        'YCT': 'Tai Po',
        'YLP': 'Yuen Long Park',
        'YNF': 'Yuen Ng Fan'
    }
    
    if not station or station not in valid_stations:
        return {"error": "Invalid or missing station code. Valid station codes are:", "stations": valid_stations}
        
    if not date:
        return {"error": "Date parameter is mandatory in YYYYMMDD format (e.g., 20250618)"}
        
    try:
        datetime.strptime(date, '%Y%m%d')
    except ValueError:
        return {"error": "Invalid date format. Date must be in YYYYMMDD format (e.g., 20250618)"}
        
    if is_date_in_future(date):
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        return {"error": f"Date must be yesterday or before in YYYYMMDD format. Expected {yesterday} or earlier, but got {date}"}
        
    params = {
        'dataType': 'RYES',
        'lang': lang,
        'rformat': rformat,
        'date': date,
        'station': station
    }

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}


def is_date_in_future(date_str: str) -> bool:
    """
    Check if the provided date is in the future compared to today.
    
    Args:
        date_str: Date string in YYYYMMDD format.
        
    Returns:
        bool: True if the date is today or in the future, False otherwise.
    """
    try:
        input_date = datetime.strptime(date_str, '%Y%m%d')
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        input_date = input_date.replace(hour=0, minute=0, second=0, microsecond=0)
        return input_date >= today
    except ValueError:
        return False
