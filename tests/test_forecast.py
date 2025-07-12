"""
Unit Tests for Forecast Tools

This module contains unit tests for the forecast tools provided by the HKO MCP Server.
It tests the functionality of fetching 9-day and local weather forecasts using mocked API responses.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.forecast import register


class TestForecastTools(unittest.TestCase):
    """
    Test case class for forecast tools.
    
    This class contains test methods to verify the correct functioning of 
    forecast data retrieval functions using mocked HTTP requests.
    """
    def test_register_tool(self):
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 2)

        # Get the decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_mcp.tool.return_value.call_args_list
        }

        # Test get_9_day_weather_forecast
        with patch("hkopenai.hk_climate_mcp_server.tools.forecast._get_9_day_weather_forecast") as mock_get_9_day_weather_forecast:
            decorated_funcs["get_9_day_weather_forecast"](lang="en")
            mock_get_9_day_weather_forecast.assert_called_once_with("en")

        # Test get_local_weather_forecast
        with patch("hkopenai.hk_climate_mcp_server.tools.forecast._get_local_weather_forecast") as mock_get_local_weather_forecast:
            decorated_funcs["get_local_weather_forecast"](lang="en")
            mock_get_local_weather_forecast.assert_called_once_with("en")


if __name__ == "__main__":
    unittest.main()

