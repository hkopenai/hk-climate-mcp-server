"""
Unit tests for moon times data retrieval functionality.

This module tests the `get_moon_times` function from the astronomical tools module
to ensure it correctly fetches and processes moon times data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.astronomical import get_moon_times


class TestMoonTimesTools(unittest.TestCase):
    """Test case class for moon times data tools."""
    @patch("requests.get")
    def test_get_moon_times(self, mock_get):
        """
        Test the retrieval of moon times data from HKO API.
        
        Args:
            mock_get: Mock object for requests.get to simulate API response.
        """
        example_json = {
            "fields": ["Date", "Moonrise", "Moon Transit", "Moonset"],
            "data": [
                ["20250601", "01:23", "07:45", "14:10"],
                ["20250602", "02:05", "08:30", "15:00"],
            ],
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_moon_times(year=2025)
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={"dataType": "MRS", "lang": "en", "rformat": "json", "year": 2025},
        )


if __name__ == "__main__":
    unittest.main()
