"""
Radiation Data Tools - Functions for fetching radiation data from HKO.

This module provides tools to retrieve radiation data including weather
and radiation level reports from the Hong Kong Observatory API.
"""

from datetime import datetime
from typing import Dict, Any, Optional
import requests
from fastmcp import FastMCP
from pydantic import Field
from typing_extensions import Annotated

# Station names in different languages: en (English), tc (Traditional Chinese),
# sc (Simplified Chinese)
VALID_STATIONS = {
    "en": {
        "CCH": "Cheung Chau",
        "CLK": "Chek Lap Kok",
        "EPC": "Ping Chau",
        "HKO": "Hong Kong Observatory",
        "HKP": "Hong Kong Park",
        "HKS": "Wong Chuk Hang",
        "HPV": "Happy Valley",
        "JKB": "Tseung Kwan O",
        "KAT": "Kat O",
        "KLT": "Kowloon City",
        "KP": "Kings Park",
        "KTG": "Kwun Tong",
        "LFS": "Lau Fau Shan",
        "PLC": "Tai Mei Tuk",
        "SE1": "Kai Tak Runway Park",
        "SEK": "Shek Kong",
        "SHA": "Sha Tin",
        "SKG": "Sai Kung",
        "SKW": "Shau Kei Wan",
        "SSP": "Sham Shui Po",
        "STK": "Sha Tau Kok",
        "STY": "Stanley",
        "SWH": "Sai Wan Ho",
        "TAP": "Tap Mun",
        "TBT": "Tsim Bei Tsui",
        "TKL": "Ta Kwu Ling",
        "TUN": "Tuen Mun",
        "TW": "Tsuen Wan Shing Mun Valley",
        "TWN": "Tsuen Wan Ho Koon",
        "TY1": "Tsing Yi",
        "WTS": "Wong Tai Sin",
        "YCT": "Tai Po",
        "YLP": "Yuen Long Park",
        "YNF": "Yuen Ng Fan",
    },
    "tc": {
        "CCH": "長洲",
        "CLK": "赤鱲角",
        "EPC": "平洲",
        "HKO": "香港天文台",
        "HKP": "香港公園",
        "HKS": "黃竹坑",
        "HPV": "跑馬地",
        "JKB": "將軍澳",
        "KAT": "吉澳",
        "KLT": "九龍城",
        "KP": "京士柏",
        "KTG": "觀塘",
        "LFS": "流浮山",
        "PLC": "大美督",
        "SE1": "啟德跑道公園",
        "SEK": "石崗",
        "SHA": "沙田",
        "SKG": "西貢",
        "SKW": "筲箕灣",
        "SSP": "深水埗",
        "STK": "沙頭角",
        "STY": "赤柱",
        "SWH": "西灣河",
        "TAP": "塔門",
        "TBT": "尖鼻咀",
        "TKL": "打鼓嶺",
        "TUN": "屯門",
        "TW": "荃灣城門谷",
        "TWN": "荃灣可觀",
        "TY1": "青衣",
        "WTS": "黃大仙",
        "YCT": "大埔",
        "YLP": "元朗公園",
        "YNF": "元五墳",
    },
    "sc": {
        "CCH": "长洲",
        "CLK": "赤鱲角",
        "EPC": "平洲",
        "HKO": "香港天文台",
        "HKP": "香港公园",
        "HKS": "黄竹坑",
        "HPV": "跑马地",
        "JKB": "将军澳",
        "KAT": "吉澳",
        "KLT": "九龙城",
        "KP": "京士柏",
        "KTG": "观塘",
        "LFS": "流浮山",
        "PLC": "大美督",
        "SE1": "启德跑道公园",
        "SEK": "石岗",
        "SHA": "沙田",
        "SKG": "西贡",
        "SKW": "筲箕湾",
        "SSP": "深水埗",
        "STK": "沙头角",
        "STY": "赤柱",
        "SWH": "西湾河",
        "TAP": "塔门",
        "TBT": "尖鼻咀",
        "TKL": "打鼓岭",
        "TUN": "屯门",
        "TW": "荃湾城门谷",
        "TWN": "荃湾可观",
        "TY1": "青衣",
        "WTS": "黄大仙",
        "YCT": "大埔",
        "YLP": "元朗公园",
        "YNF": "元五坟",
    },
}


def register(mcp: FastMCP):
    @mcp.tool(
        description="Get weather, radiation report for HK. Date must be YYYYMMDD.",
    )
    def get_weather_radiation_report(
        date: Annotated[
            str, Field(description="Date in yyyyMMdd format, e.g., 20250618")
        ],
        station: Annotated[str, Field(description="Station code, e.g., HKO")],
        lang: Annotated[Optional[str], Field(description="Language (en/tc/sc)")] = "en",
    ) -> Dict[str, Any]:
        return _get_weather_radiation_report(
            date=date, station=station, lang=lang or "en"
        )


    @mcp.tool(
        description="Get list of weather station codes and names for radiation reports in HK.",
    )
    def get_radiation_station_codes(lang: str = "en") -> Dict[str, str]:
        return _get_radiation_station_codes(lang=lang)

def _get_weather_radiation_report(
    date: str = "Unknown", station: str = "Unknown", lang: str = "en"
) -> Dict[str, Any]:
    """
    Get weather and radiation level report for Hong Kong.

    Args:
        date: Mandatory date in YYYYMMDD format (e.g., 20250618)
        station: Mandatory station code (e.g., 'HKO' for Hong Kong Observatory).
                 If not provided or invalid, returns an error message.
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing weather and radiation data or an error message if
        station is invalid
    """
    # Select station by language
    stations_dict = VALID_STATIONS.get(lang, VALID_STATIONS["en"])
    if not station or station not in stations_dict:
        return {
            "error": "Invalid or missing station code. "
            "Use 'get_radiation_station_codes' for codes."
        }
    if not date:
        return {
            "error": "Date parameter is mandatory in YYYYMMDD format (e.g., 20250618)"
        }
    try:
        datetime.strptime(date, "%Y%m%d")
    except ValueError:
        return {
            "error": "Invalid date format. Date must be in YYYYMMDD format (e.g., 20250618)"
        }
    if is_date_in_future(date):
        return {"error": "Date must be yesterday or before."}
    params = {
        "dataType": "RYES",
        "lang": lang,
        "rformat": "json",
        "date": date,
        "station": station,
    }

    try:
        base_url = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {
                "error": (
                    "Failed to parse JSON. Invalid params or data not updated. "
                    "Try again."
                )
            }
    except requests.RequestException as e:
        return {
            "error": (f"Failed to fetch data: {str(e)}. Please try " "again later.")
        }


def _get_radiation_station_codes(lang: str = "en") -> Dict[str, str]:
    """
    Get a dictionary of station codes and their corresponding names for weather and radiation reports in Hong Kong used in radiation API.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict mapping station codes to station names in the specified language.
    """
    # Return the dictionary for the specified language, default to English
    return VALID_STATIONS.get(lang, VALID_STATIONS["en"])



def is_date_in_future(date_str: str) -> bool:
    """
    Check if the provided date is in the future compared to today.

    Args:
        date_str: Date string in YYYYMMDD format.

    Returns:
        bool: True if the date is today or in the future, False otherwise.
    """
    try:
        input_date = datetime.strptime(date_str, "%Y%m%d")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        input_date = input_date.replace(hour=0, minute=0, second=0, microsecond=0)
        return input_date >= today
    except ValueError:
        return False
