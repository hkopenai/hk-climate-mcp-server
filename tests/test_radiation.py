import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.radiation import get_weather_radiation_report

class TestRadiationTools(unittest.TestCase):
    @patch("requests.get")
    def test_get_weather_radiation_report(self, mock_get):
        example_json = {
            "fields": ["Date", "Station", "Radiation Level (microsievert/hour)"],
            "data": [
                ["20250622", "HKO", "0.12"],
                ["20250622", "KCP", "0.15"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_weather_radiation_report()
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
            params={'dataType': 'RYES', 'lang': 'en', 'rformat': 'json'}
        )

if __name__ == "__main__":
    unittest.main()
