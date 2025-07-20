"""
Unit tests for current weather data fetching functions.

This module tests the functionality of fetching current weather data from the Hong Kong Observatory API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.current_weather import (
    register,
    _get_current_weather,
)
from hkopenai_common.json_utils import fetch_json_data


class TestCurrentWeatherTools(unittest.TestCase):
    """
    Test case class for testing current weather data fetching tools and functions.
    """

    default_mock_response = {
        "rainfall": {
            "data": [
                {
                    "unit": "mm",
                    "place": "Central & Western District",
                    "max": 0,
                    "main": "FALSE",
                },
                {"unit": "mm", "place": "Eastern District", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Kwai Tsing", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Islands District", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "North District", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Sai Kung", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Sha Tin", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Southern District", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Tai Po", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Tsuen Wan", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Tuen Mun", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Wan Chai", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Yuen Long", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Yau Tsim Mong", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Sham Shui Po", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Kowloon City", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Wong Tai Sin", "max": 0, "main": "FALSE"},
                {"unit": "mm", "place": "Kwun Tong", "max": 0, "main": "FALSE"},
            ],
            "startTime": "2025-06-07T20:45:00+08:00",
            "endTime": "2025-06-07T21:45:00+08:00",
        },
        "icon": [72],
        "iconUpdateTime": "2025-06-07T18:00:00+08:00",
        "uvindex": "",
        "updateTime": "2025-06-07T22:02:00+08:00",
        "temperature": {
            "data": [
                {"place": "King's Park", "value": 28, "unit": "C"},
                {"place": "Hong Kong Observatory", "value": 29, "unit": "C"},
                {"place": "Wong Chuk Hang", "value": 28, "unit": "C"},
                {"place": "Ta Kwu Ling", "value": 28, "unit": "C"},
                {"place": "Lau Fau Shan", "value": 28, "unit": "C"},
                {"place": "Tai Po", "value": 29, "unit": "C"},
                {"place": "Sha Tin", "value": 29, "unit": "C"},
                {"place": "Tuen Mun", "value": 29, "unit": "C"},
                {"place": "Tseung Kwan O", "value": 27, "unit": "C"},
                {"place": "Sai Kung", "value": 28, "unit": "C"},
                {"place": "Cheung Chau", "value": 27, "unit": "C"},
                {"place": "Chek Lap Kok", "value": 29, "unit": "C"},
                {"place": "Tsing Yi", "value": 28, "unit": "C"},
                {"place": "Shek Kong", "value": 29, "unit": "C"},
                {"place": "Tsuen Wan Ho Koon", "value": 27, "unit": "C"},
                {"place": "Tsuen Wan Shing Mun Valley", "value": 28, "unit": "C"},
                {"place": "Hong Kong Park", "value": 28, "unit": "C"},
                {"place": "Shau Kei Wan", "value": 28, "unit": "C"},
                {"place": "Kowloon City", "value": 29, "unit": "C"},
                {"place": "Happy Valley", "value": 29, "unit": "C"},
                {"place": "Wong Tai Sin", "value": 29, "unit": "C"},
                {"place": "Stanley", "value": 28, "unit": "C"},
                {"place": "Kwun Tong", "value": 28, "unit": "C"},
                {"place": "Sham Shui Po", "value": 29, "unit": "C"},
                {"place": "Kai Tak Runway Park", "value": 29, "unit": "C"},
                {"place": "Yuen Long Park", "value": 28, "unit": "C"},
                {"place": "Tai Mei Tuk", "value": 28, "unit": "C"},
            ],
            "recordTime": "2025-06-07T22:00:00+08:00",
        },
        "warningMessage": [
            "The Very Hot weather Warning is now in force. Prolonged heat alert! Please drink sufficient water. If feeling unwell, take rest or seek help immediately. If needed, seek medical advice as soon as possible."
        ],
        "mintempFrom00To09": "",
        "rainfallFrom00To12": "",
        "rainfallLastMonth": "",
        "rainfallJanuaryToLastMonth": "",
        "tcmessage": "",
        "humidity": {
            "recordTime": "2025-06-07T22:00:00+08:00",
            "data": [
                {"unit": "percent", "value": 79, "place": "Hong Kong Observatory"}
            ],
        },
    }

    def test_register_tool(self):
        """Tests that the current weather tool is correctly registered."""
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 1)

        # Get the decorated function
        decorated_func = mock_mcp.tool.return_value.call_args[0][0]

        # Test get_current_weather
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.current_weather._get_current_weather"
        ) as mock_get_current_weather:
            decorated_func(region="test", lang="en")
            mock_get_current_weather.assert_called_once_with("test", "en")

    @patch("hkopenai.hk_climate_mcp_server.tools.current_weather.fetch_json_data")
    def test_get_current_weather_internal(self, mock_fetch_json_data):
        """Test the internal _get_current_weather function."""
        mock_fetch_json_data.return_value = self.default_mock_response

        result = _get_current_weather(region="Hong Kong Observatory", lang="en")
        self.assertIsNotNone(result)
        self.assertIn("generalSituation", result)
        self.assertIn("weatherObservation", result)
        self.assertEqual(
            result["weatherObservation"]["temperature"]["value"], 29
        )  # From default_mock_response
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"
        )


if __name__ == "__main__":
    unittest.main()
