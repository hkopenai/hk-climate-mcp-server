import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.astronomical import get_sunrise_sunset_times


class TestSunTimesTools(unittest.TestCase):
    @patch("requests.get")
    def test_get_sunrise_sunset_times(self, mock_get):
        example_json = {
            "fields": ["Date", "Sunrise", "Sun Transit", "Sunset"],
            "data": [
                ["20250601", "05:40", "12:15", "18:50"],
                ["20250602", "05:40", "12:15", "18:51"],
            ],
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_sunrise_sunset_times(year=2025)
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={"dataType": "SRS", "lang": "en", "rformat": "json", "year": 2025},
        )


if __name__ == "__main__":
    unittest.main()
