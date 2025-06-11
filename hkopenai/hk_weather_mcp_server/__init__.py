"""Hong Kong weather MCP Server package."""
from .app import main
from .tool_weather import get_current_weather

__version__ = "0.1.0"
__all__ = ['main', 'get_current_weather']
