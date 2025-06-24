import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.temperature import get_daily_mean_temperature, get_daily_max_temperature, get_daily_min_temperature

class TestTemperatureTools(unittest.TestCase):
    @patch("requests.get")
    def test_get_daily_mean_temperature(self, mock_get):
        example_json = {
            "fields": ["Date", "Mean Temperature (degree Celsius)"],
            "data": [
                ["20250601", "26.5"],
                ["20250602", "27.0"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_daily_mean_temperature(station="HKO")
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
            params={'dataType': 'CLMTEMP', 'lang': 'en', 'rformat': 'json', 'station': 'HKO'}
        )

    @patch("requests.get")
    def test_get_daily_max_temperature(self, mock_get):
        example_json = {
            "fields": ["Date", "Maximum Temperature (degree Celsius)"],
            "data": [
                ["20250601", "30.2"],
                ["20250602", "31.5"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_daily_max_temperature(station="HKO")
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
            params={'dataType': 'CLMMAXT', 'lang': 'en', 'rformat': 'json', 'station': 'HKO'}
        )

    @patch("requests.get")
    def test_get_daily_min_temperature(self, mock_get):
        example_json = {
            "fields": ["Date", "Minimum Temperature (degree Celsius)"],
            "data": [
                ["20250601", "23.1"],
                ["20250602", "24.0"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_daily_min_temperature(station="HKO")
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
            params={'dataType': 'CLMMINT', 'lang': 'en', 'rformat': 'json', 'station': 'HKO'}
        )

if __name__ == "__main__":
    unittest.main()
