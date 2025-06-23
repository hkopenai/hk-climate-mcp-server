import requests
from typing import Dict, List, Any, Optional

def get_current_weather(region: str = "Hong Kong Observatory", lang: str = "en") -> Dict:
    """
    Get current weather observations for a specific region in Hong Kong

    Args:
        region: The region to get weather for (default: "Hong Kong Observatory")
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
        - warning: Current weather warnings
        - temperature: Current temperature in Celsius
        - humidity: Current humidity percentage
        - rainfall: Current rainfall in mm
    """
    response = requests.get(
        f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang={lang}"
    )
    data = response.json()

    # Handle warnings
    warning = "No warning in force"
    if "warningMessage" in data:
        if isinstance(data["warningMessage"], list) and data["warningMessage"]:
            warning = data["warningMessage"][0]
        elif data["warningMessage"]:  # Handle string case
            warning = data["warningMessage"]

    # Get default values from HKO data
    default_temp = next(
        (
            t
            for t in data.get("temperature", {}).get("data", [])
            if t.get("place") == "Hong Kong Observatory"
        ),
        {"value": 25, "unit": "C", "recordTime": ""},
    )
    default_humidity = next(
        (
            h
            for h in data.get("humidity", {}).get("data", [])
            if h.get("place") == "Hong Kong Observatory"
        ),
        {"value": 60, "unit": "percent", "recordTime": ""},
    )
    # Find matching region temperature
    temp_data = data.get("temperature", {}).get("data", [])
    matched_temp = next(
        (t for t in temp_data if t["place"].lower() == region.lower()),
        {
            "place": "Hong Kong Observatory",
            "value": default_temp["value"],
            "unit": default_temp["unit"],
        },
    )
    matched_temp["recordTime"] = data["temperature"]["recordTime"]

    # Get humidity
    humidity = next(
        (
            h
            for h in data.get("humidity", {}).get("data", [])
            if h.get("place") == matched_temp["place"]
        ),
        default_humidity,
    )
    humidity["recordTime"] = data["humidity"]["recordTime"]

    # Get rainfall (0 if no rain)
    rainfall = 0
    if "rainfall" in data:
        rainfall = max(float(r.get("max", 0)) for r in data["rainfall"]["data"])
        rainfall_start = data["rainfall"]["startTime"]
        rainfall_end = data["rainfall"]["endTime"]

    return {
        "generalSituation": warning,
        "weatherObservation": {
            "temperature": {
                "value": matched_temp["value"],
                "unit": matched_temp["unit"],
                "recordTime": matched_temp["recordTime"],
                "place": matched_temp["place"]
            },
            "humidity": {
                "value": humidity["value"],
                "unit": humidity["unit"],
                "recordTime": humidity["recordTime"],
                "place": matched_temp["place"]
            },
            "rainfall": {
                "value": rainfall,
                "min": min(float(r.get("min", 0)) for r in data["rainfall"]["data"]),
                "unit": "mm",
                "startTime": rainfall_start,
                "endTime": rainfall_end
            },
            "uvindex": data.get("uvindex", {})
        },
        "updateTime": data["updateTime"],
        "icon": data.get("icon", []),
        "iconUpdateTime": data.get("iconUpdateTime", "")
    }

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

def get_weather_warning_summary(lang: str = "en") -> Dict[str, Any]:
    """
    Get weather warning summary for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - warningMessage: List of warning messages
            - updateTime: Last update time
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang={lang}"
    response = requests.get(url)
    data = response.json()
    
    return {
        "warningMessage": data.get("warningMessage", []),
        "updateTime": data.get("updateTime", ""),
    }

def get_weather_warning_info(lang: str = "en") -> Dict[str, Any]:
    """
    Get detailed weather warning information for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - warningStatement: Warning statement
            - updateTime: Last update time
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang={lang}"
    response = requests.get(url)
    data = response.json()
    
    return {
        "warningStatement": data.get("warningStatement", ""),
        "updateTime": data.get("updateTime", ""),
    }

def get_special_weather_tips(lang: str = "en") -> Dict[str, Any]:
    """
    Get special weather tips for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)

    Returns:
        Dict containing:
            - specialWeatherTips: List of special weather tips
            - updateTime: Last update time
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=swt&lang={lang}"
    response = requests.get(url)
    data = response.json()
    
    return {
        "specialWeatherTips": data.get("specialWeatherTips", []),
        "updateTime": data.get("updateTime", ""),
    }

def get_visibility_data(lang: str = "en", rformat: str = "json") -> Dict[str, Any]:
    """
    Get latest 10-minute mean visibility data for Hong Kong.

    Args:
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing visibility data with fields and data arrays
    """
    url = f"https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LTMV&lang={lang}&rformat={rformat}"
    response = requests.get(url)
    return response.json() if rformat == "json" else {"data": response.text}

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

def get_daily_mean_temperature(
    station: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    lang: str = "en",
    rformat: str = "json"
) -> Dict[str, Any]:
    """
    Get daily mean temperature data for a specific station.

    Args:
        station: Station code (e.g. 'HKO' for Hong Kong Observatory)
        year: Optional year (varies by station)
        month: Optional month (1-12)
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing temperature data with fields and data arrays
    """
    params = {
        'dataType': 'CLMTEMP',
        'lang': lang,
        'rformat': rformat,
        'station': station
    }
    if year: params['year'] = year
    if month: params['month'] = month

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}

def get_daily_max_temperature(
    station: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    lang: str = "en",
    rformat: str = "json"
) -> Dict[str, Any]:
    """
    Get daily maximum temperature data for a specific station.

    Args:
        station: Station code (e.g. 'HKO' for Hong Kong Observatory)
        year: Optional year (varies by station)
        month: Optional month (1-12)
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing temperature data with fields and data arrays
    """
    params = {
        'dataType': 'CLMMAXT',
        'lang': lang,
        'rformat': rformat,
        'station': station
    }
    if year: params['year'] = year
    if month: params['month'] = month

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}

def get_daily_min_temperature(
    station: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
    lang: str = "en",
    rformat: str = "json"
) -> Dict[str, Any]:
    """
    Get daily minimum temperature data for a specific station.

    Args:
        station: Station code (e.g. 'HKO' for Hong Kong Observatory)
        year: Optional year (varies by station)
        month: Optional month (1-12)
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing temperature data with fields and data arrays
    """
    params = {
        'dataType': 'CLMMINT',
        'lang': lang,
        'rformat': rformat,
        'station': station
    }
    if year: params['year'] = year
    if month: params['month'] = month

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}

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

def get_moon_times(year: int, month: Optional[int] = None, 
                  day: Optional[int] = None, lang: str = "en",
                  rformat: str = "json") -> Dict[str, Any]:
    """
    Get times of moonrise, moon transit and moonset.

    Args:
        year: Year (2018-2024)
        month: Optional month (1-12)
        day: Optional day (1-31)
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing moon times data with fields and data arrays
    """
    params = {
        'dataType': 'MRS',
        'lang': lang,
        'rformat': rformat,
        'year': year
    }
    if month: params['month'] = month
    if day: params['day'] = day

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}

def get_hourly_tides(
    station: str,
    year: int,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    lang: str = "en",
    rformat: str = "json"
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
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing tide data with fields and data arrays
    """
    params = {
        'dataType': 'HHOT',
        'lang': lang,
        'rformat': rformat,
        'station': station,
        'year': year
    }
    if month: params['month'] = month
    if day: params['day'] = day
    if hour: params['hour'] = hour

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}

def get_high_low_tides(
    station: str,
    year: int,
    month: Optional[int] = None,
    day: Optional[int] = None,
    hour: Optional[int] = None,
    lang: str = "en",
    rformat: str = "json"
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
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing tide data with fields and data arrays
    """
    params = {
        'dataType': 'HLT',
        'lang': lang,
        'rformat': rformat,
        'station': station,
        'year': year
    }
    if month: params['month'] = month
    if day: params['day'] = day
    if hour: params['hour'] = hour

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}

def get_sunrise_sunset_times(
    year: int,
    month: Optional[int] = None,
    day: Optional[int] = None,
    lang: str = "en",
    rformat: str = "json"
) -> Dict[str, Any]:
    """
    Get times of sunrise, sun transit and sunset.

    Args:
        year: Year (2018-2024)
        month: Optional month (1-12)
        day: Optional day (1-31)
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing sun times data with fields and data arrays
    """
    params = {
        'dataType': 'SRS',
        'lang': lang,
        'rformat': rformat,
        'year': year
    }
    if month: params['month'] = month
    if day: params['day'] = day

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}

def get_gregorian_lunar_calendar(
    year: int,
    month: Optional[int] = None,
    day: Optional[int] = None,
    lang: str = "en",
    rformat: str = "json"
) -> Dict[str, Any]:
    """
    Get Gregorian-Lunar calendar conversion data.

    Args:
        year: Year (1901-2100)
        month: Optional month (1-12)
        day: Optional day (1-31)
        lang: Language code (en/tc/sc, default: en)
        rformat: Return format (json/csv, default: json)

    Returns:
        Dict containing calendar conversion data
    """
    params = {
        'dataType': 'GLC',
        'lang': lang,
        'rformat': rformat,
        'year': year
    }
    if month: params['month'] = month
    if day: params['day'] = day

    response = requests.get(
        'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
        params=params
    )
    response.raise_for_status()
    return response.json() if rformat == "json" else {"data": response.text}
