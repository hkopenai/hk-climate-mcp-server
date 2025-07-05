"""
Unit tests for astronomical data fetching functions.

This module tests the functionality of fetching astronomical data such as Gregorian-Lunar calendar conversions from the Hong Kong Observatory API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.astronomical import get_gregorian_lunar_calendar

class TestCalendarTools(unittest.TestCase):
    """
    Test case class for testing calendar-related tools and functions.
    """
    @patch("requests.get")
    def test_get_gregorian_lunar_calendar(self, mock_get):
        example_json = {
            "fields": ["Gregorian Date", "Lunar Date"],
            "data": [
                ["20250601", "4th Month 25, 2025 (Yi Si)"],
                ["20250602", "4th Month 26, 2025 (Yi Si)"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_gregorian_lunar_calendar(year=2025)
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            'https://data.weather.gov.hk/weatherAPI/opendata/lunardate.php', params={'date': '2025-01-01'}
        )

if __name__ == "__main__":
    unittest.main()
