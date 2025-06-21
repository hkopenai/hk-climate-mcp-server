"""Hong Kong climate MCP Server package."""
from .app import main
from .tool_weather import (
    get_current_weather,
    get_9_day_weather_forecast,
    get_local_weather_forecast,
    get_weather_warning_summary,
    get_weather_warning_info,
    get_special_weather_tips
)

__version__ = "0.1.0"
__all__ = [
    'main',
    'get_current_weather',
    'get_9_day_weather_forecast',
    'get_local_weather_forecast',
    'get_weather_warning_summary',
    'get_weather_warning_info',
    'get_special_weather_tips'
]
