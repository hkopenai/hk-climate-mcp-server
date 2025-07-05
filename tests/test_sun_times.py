"""
Unit tests for sunrise and sunset times data retrieval functionality.

This module tests the `get_sunrise_sunset_times` function from the astronomical tools module
to ensure it correctly fetches and processes sun times data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.astronomical import get_sunrise_sunset_times


class TestSunTimesTools(unittest.TestCase):
    """Test case class for sun times data tools."""
    @patch("requests.get")
    def test_get_sunrise_sunset_times(self, mock_get):
        """
        Test the retrieval of sunrise and sunset times data from HKO API.
        
        Args:
            mock_get: Mock object for requests.get to simulate API response.
        """
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
