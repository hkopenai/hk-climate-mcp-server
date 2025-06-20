"""Hong Kong climate MCP Server package."""
from .app import main
from .tool_weather import get_current_weather
from .tool_weather import get_9_day_weather_forecast

__version__ = "0.1.0"
__all__ = ['main', 'get_current_weather', 'get_9_day_weather_forecast']
