import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.warnings import get_weather_warning_summary, get_weather_warning_info, get_special_weather_tips

class TestWarningsTools(unittest.TestCase):
    @patch("requests.get")
    def test_get_weather_warning_summary(self, mock_get):
        example_json = {
            "warningMessage": [
                "The Very Hot Weather Warning is in force.",
                "Thunderstorm Warning is in force."
            ],
            "updateTime": "2025-06-20T07:50:00+08:00"
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_weather_warning_summary()
        self.assertEqual(result["warningMessage"], example_json["warningMessage"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en"
        )

    @patch("requests.get")
    def test_get_weather_warning_info(self, mock_get):
        example_json = {
            "warningStatement": "The Thunderstorm Warning was issued at 7:50 a.m.",
            "updateTime": "2025-06-20T07:50:00+08:00"
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_weather_warning_info()
        self.assertEqual(result["warningStatement"], example_json["warningStatement"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang=en"
        )

    @patch("requests.get")
    def test_get_special_weather_tips(self, mock_get):
        example_json = {
            "specialWeatherTips": [
                "Hot weather may cause heat stroke. Avoid prolonged exposure to sunlight.",
                "Heavy rain may cause flooding in low-lying areas."
            ],
            "updateTime": "2025-06-20T07:50:00+08:00"
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_special_weather_tips()
        self.assertEqual(result["specialWeatherTips"], example_json["specialWeatherTips"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=swt&lang=en"
        )

if __name__ == "__main__":
    unittest.main()
