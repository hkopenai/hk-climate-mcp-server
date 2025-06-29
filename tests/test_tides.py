import unittest
from unittest.mock import patch, MagicMock
import json
from hkopenai.hk_climate_mcp_server.tools.tides import get_hourly_tides, get_high_low_tides

class TestTidesTools(unittest.TestCase):
    @patch("requests.get")
    def test_get_hourly_tides(self, mock_get):
        example_json = {
            "fields": ["Date time", "Height (m)"],
            "data": [
                ["202506010100", "1.2"],
                ["202506010200", "1.3"]
            ]
        }
        mock_response = MagicMock()
        mock_response.content = json.dumps(example_json).encode('utf-8')
        mock_get.return_value = mock_response

        result = get_hourly_tides(station="CCH", year=2025)
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
            params={'dataType': 'HHOT', 'lang': 'en', 'rformat': 'json', 'station': 'CCH', 'year': 2025}
        )

    @patch("requests.get")
    def test_get_high_low_tides(self, mock_get):
        example_json = {
            "fields": ["Date time", "Type", "Height (m)"],
            "data": [
                ["202506010430", "High", "1.8"],
                ["202506011030", "Low", "0.5"]
            ]
        }
        mock_response = MagicMock()
        mock_response.content = json.dumps(example_json).encode('utf-8')
        mock_get.return_value = mock_response

        result = get_high_low_tides(station="CCH", year=2025)
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            'https://data.weather.gov.hk/weatherAPI/opendata/opendata.php',
            params={'dataType': 'HLT', 'lang': 'en', 'station': 'CCH', 'year': 2025, 'rformat': 'json'}
        )

if __name__ == "__main__":
    unittest.main()
