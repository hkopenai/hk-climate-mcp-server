"""Hong Kong climate MCP Server package."""
from .app import main
from .tool_weather import (
    get_current_weather,
    get_9_day_weather_forecast,
    get_local_weather_forecast,
    get_weather_warning_summary,
    get_weather_warning_info,
    get_special_weather_tips,
    get_visibility_data,
    get_lightning_data,
    get_moon_times,
    get_hourly_tides,
    get_high_low_tides,
    get_sunrise_sunset_times,
    get_gregorian_lunar_calendar,
    get_daily_mean_temperature,
    get_daily_max_temperature,
    get_daily_min_temperature,
    get_weather_radiation_report
)

__version__ = "0.1.0"
__all__ = [
    'main',
    'get_current_weather',
    'get_9_day_weather_forecast',
    'get_local_weather_forecast',
    'get_weather_warning_summary',
    'get_weather_warning_info',
    'get_special_weather_tips',
    'get_visibility_data',
    'get_lightning_data',
    'get_moon_times',
    'get_hourly_tides',
    'get_high_low_tides',
    'get_sunrise_sunset_times',
    'get_gregorian_lunar_calendar',
    'get_daily_mean_temperature',
    'get_daily_max_temperature',
    'get_daily_min_temperature',
    'get_weather_radiation_report'
]
