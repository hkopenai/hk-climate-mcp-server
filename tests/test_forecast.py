"""
Unit Tests for Forecast Tools

This module contains unit tests for the forecast tools provided by the HKO MCP Server.
It tests the functionality of fetching 9-day and local weather forecasts using mocked API responses.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.forecast import (
    register,
    _get_9_day_weather_forecast,
    _get_local_weather_forecast,
)
from hkopenai_common.json_utils import fetch_json_data


class TestForecastTools(unittest.TestCase):
    """
    Test case class for forecast tools.

    This class contains test methods to verify the correct functioning of
    forecast data retrieval functions using mocked HTTP requests.
    """

    def test_register_tool(self):
        """Tests that the forecast tools are correctly registered."""
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
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.forecast._get_9_day_weather_forecast"
        ) as mock_get_9_day_weather_forecast:
            decorated_funcs["get_9_day_weather_forecast"](lang="en")
            mock_get_9_day_weather_forecast.assert_called_once_with("en")

        # Test get_local_weather_forecast
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.forecast._get_local_weather_forecast"
        ) as mock_get_local_weather_forecast:
            decorated_funcs["get_local_weather_forecast"](lang="en")
            mock_get_local_weather_forecast.assert_called_once_with("en")

    @patch("hkopenai.hk_climate_mcp_server.tools.forecast.fetch_json_data")
    def test_get_9_day_weather_forecast_internal(self, mock_fetch_json_data):
        """Test the internal _get_9_day_weather_forecast function."""
        example_json = {
            "generalSituation": "Fine.",
            "weatherForecast": [
                {
                    "forecastDate": "20250623",
                    "week": "Monday",
                    "forecastWind": "Light winds.",
                    "forecastWeather": "Sunny periods.",
                    "forecastMaxtemp": {"value": 30, "unit": "C"},
                    "forecastMintemp": {"value": 25, "unit": "C"},
                    "forecastMaxrh": {"value": 95, "unit": "percent"},
                    "forecastMinrh": {"value": 70, "unit": "percent"},
                    "ForecastIcon": 51,
                    "PSR": "High",
                }
            ],
            "updateTime": "2025-06-22T16:30:00+08:00",
            "seaTemp": {},
            "soilTemp": [],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_9_day_weather_forecast(lang="en")
        self.assertEqual(result["generalSituation"], example_json["generalSituation"])
        self.assertEqual(len(result["weatherForecast"]), 1)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=en"
        )

    @patch("hkopenai.hk_climate_mcp_server.tools.forecast.fetch_json_data")
    def test_get_local_weather_forecast_internal(self, mock_fetch_json_data):
        """Test the internal _get_local_weather_forecast function."""
        example_json = {
            "generalSituation": "Fine.",
            "forecastDesc": "Sunny periods.",
            "outlook": "Mainly fine.",
            "updateTime": "2025-06-22T16:30:00+08:00",
            "forecastPeriod": "Today and tomorrow.",
            "forecastDate": "20250623",
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_local_weather_forecast(lang="en")
        self.assertEqual(result["forecastDesc"], example_json["forecastDesc"])
        self.assertEqual(result["outlook"], example_json["outlook"])
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=en"
        )


if __name__ == "__main__":
    unittest.main()
