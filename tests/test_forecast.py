"""
Unit Tests for Forecast Tools

This module contains unit tests for the forecast tools provided by the HKO MCP Server.
It tests the functionality of fetching 9-day and local weather forecasts using mocked API responses.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.forecast import (
    get_9_day_weather_forecast,
    get_local_weather_forecast,
)


class TestForecastTools(unittest.TestCase):
    """
    Test case class for forecast tools.
    
    This class contains test methods to verify the correct functioning of 
    forecast data retrieval functions using mocked HTTP requests.
    """
    @patch("requests.get")
    def test_get_9_day_weather_forecast(self, mock_get):
        """
        Test the retrieval of 9-day weather forecast data.
        
        This test uses a mocked HTTP response to simulate the API call and
        verifies that the function correctly parses and returns the forecast data.
        
        Args:
            mock_get: Mocked requests.get method to simulate API response.
        """
        example_json = {
            "generalSituation": "A southerly airstream...",
            "weatherForecast": [
                {
                    "forecastDate": "20250620",
                    "week": "Friday",
                    "forecastWind": "South force 3 to 4.",
                    "forecastWeather": "Mainly cloudy with occasional showers.",
                    "forecastMaxtemp": {"value": 31, "unit": "C"},
                    "forecastMintemp": {"value": 27, "unit": "C"},
                    "forecastMaxrh": {"value": 95, "unit": "percent"},
                    "forecastMinrh": {"value": 70, "unit": "percent"},
                    "ForecastIcon": 54,
                    "PSR": "Medium",
                }
            ],
            "updateTime": "2025-06-20T07:50:00+08:00",
            "seaTemp": {
                "place": "North Point",
                "value": 28,
                "unit": "C",
                "recordTime": "2025-06-20T07:00:00+08:00",
            },
            "soilTemp": [
                {
                    "place": "Hong Kong Observatory",
                    "value": 29.2,
                    "unit": "C",
                    "recordTime": "2025-06-20T07:00:00+08:00",
                    "depth": {"unit": "metre", "value": 0.5},
                }
            ],
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_9_day_weather_forecast()
        self.assertEqual(result["generalSituation"], example_json["generalSituation"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        self.assertEqual(result["seaTemp"], example_json["seaTemp"])
        self.assertEqual(result["soilTemp"], example_json["soilTemp"])
        self.assertIsInstance(result["weatherForecast"], list)
        self.assertEqual(result["weatherForecast"][0]["forecastDate"], "20250620")
        self.assertEqual(result["weatherForecast"][0]["week"], "Friday")
        self.assertEqual(
            result["weatherForecast"][0]["forecastWind"], "South force 3 to 4."
        )
        self.assertEqual(
            result["weatherForecast"][0]["forecastWeather"],
            "Mainly cloudy with occasional showers.",
        )

    @patch("requests.get")
    def test_get_local_weather_forecast(self, mock_get):
        """
        Test the retrieval of local weather forecast data.
        
        This test uses a mocked HTTP response to simulate the API call and
        verifies that the function correctly parses and returns the local forecast data.
        
        Args:
            mock_get: Mocked requests.get method to simulate API response.
        """
        example_json = {
            "generalSituation": "A southerly airstream is bringing showers to the coast of Guangdong and the northern part of the South China Sea. Locally, around 5 millimetres of rainfall were recorded over many places in the past couple of hours.",
            "forecastPeriod": "Weather forecast for today",
            "forecastDesc": "Mainly cloudy with a few showers. More showers with isolated thunderstorms at first. Hot with sunny periods during the day with a maximum temperature of around 32 degrees. Moderate southerly winds.",
            "outlook": "Mainly fine and very hot in the next couple of days. Showers will increase gradually in the middle and latter parts of next week.",
            "updateTime": "2025-06-21T07:45:00+08:00",
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_local_weather_forecast()
        self.assertEqual(result["forecastDesc"], example_json["forecastDesc"])
        self.assertEqual(result["outlook"], example_json["outlook"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        self.assertEqual(result["forecastPeriod"], example_json["forecastPeriod"])
        self.assertEqual(result["generalSituation"], example_json["generalSituation"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=en"
        )


if __name__ == "__main__":
    unittest.main()
