import requests
from typing import Dict, Any

def get_9_day_weather_forecast(lang: str = "en") -> Dict[str, Any]:
    """
    Get the 9-day weather forecast for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - generalSituation: General weather situation
            - weatherForecast: List of daily forecast dicts (date, week, wind, weather, temp/humidity, etc.)
            - updateTime: Last update time
            - seaTemp: Sea temperature info
            - soilTemp: List of soil temperature info
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang={lang}"
    response = requests.get(url)
    data = response.json()

    # Structure the output
    forecast = {
        "generalSituation": data.get("generalSituation", ""),
        "weatherForecast": [],
        "updateTime": data.get("updateTime", ""),
        "seaTemp": data.get("seaTemp", {}),
        "soilTemp": data.get("soilTemp", []),
    }

    # Extract 9-day forecast
    for day in data.get("weatherForecast", []):
        forecast["weatherForecast"].append({
            "forecastDate": day.get("forecastDate", ""),
            "week": day.get("week", ""),
            "forecastWind": day.get("forecastWind", ""),
            "forecastWeather": day.get("forecastWeather", ""),
            "forecastMaxtemp": day.get("forecastMaxtemp", {}),
            "forecastMintemp": day.get("forecastMintemp", {}),
            "forecastMaxrh": day.get("forecastMaxrh", {}),
            "forecastMinrh": day.get("forecastMinrh", {}),
            "ForecastIcon": day.get("ForecastIcon", ""),
            "PSR": day.get("PSR", ""),
        })
    return forecast

def get_local_weather_forecast(lang: str = "en") -> Dict[str, Any]:
    """
    Get local weather forecast for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - forecastDesc: Forecast description
            - outlook: Outlook forecast
            - updateTime: Last update time
            - forecastPeriod: Forecast period
            - forecastDate: Forecast date
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang={lang}"
    response = requests.get(url)
    data = response.json()
    
    return {
        "generalSituation": data.get("generalSituation", ""),
        "forecastDesc": data.get("forecastDesc", ""),
        "outlook": data.get("outlook", ""),
        "updateTime": data.get("updateTime", ""),
        "forecastPeriod": data.get("forecastPeriod", ""),
        "forecastDate": data.get("forecastDate", ""),
    }
