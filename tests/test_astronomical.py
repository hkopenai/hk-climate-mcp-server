"""
Unit tests for astronomical data fetching functions.

This module tests the functionality of fetching astronomical data such as Gregorian-Lunar calendar conversions from the Hong Kong Observatory API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.astronomical import (
    register,
    _get_moon_times,
    _get_sunrise_sunset_times,
    _get_gregorian_lunar_calendar,
)
from hkopenai.hk_climate_mcp_server.tools.astronomical import fetch_json_data


class TestAstronomicalTools(unittest.TestCase):
    """Tests for the astronomical data tools."""

    def test_register_tool(self):
        """Tests that the astronomical tools are correctly registered."""
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 3)

        # Get the decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_mcp.tool.return_value.call_args_list
        }

        # Test get_moon_times
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.astronomical._get_moon_times"
        ) as mock_get_moon_times:
            decorated_funcs["get_moon_times"](year=2025, month=6, day=30)
            mock_get_moon_times.assert_called_once_with(
                year=2025, month=6, day=30, lang="en"
            )

        # Test get_sunrise_sunset_times
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.astronomical._get_sunrise_sunset_times"
        ) as mock_get_sunrise_sunset_times:
            decorated_funcs["get_sunrise_sunset_times"](year=2025)
            mock_get_sunrise_sunset_times.assert_called_once_with(
                year=2025, month=None, day=None, lang="en"
            )

        # Test get_gregorian_lunar_calendar
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.astronomical._get_gregorian_lunar_calendar"
        ) as mock_get_gregorian_lunar_calendar:
            decorated_funcs["get_gregorian_lunar_calendar"](year=2025, month=6)
            mock_get_gregorian_lunar_calendar.assert_called_once_with(
                year=2025, month=6, day=None, lang="en"
            )

    @patch("hkopenai.hk_climate_mcp_server.tools.astronomical.fetch_json_data")
    def test_get_moon_times_internal(self, mock_fetch_json_data):
        """Test the internal _get_moon_times function."""
        example_json = {
            "fields": ["Date", "Moonrise", "Moonset", "Moon Transit", "Moon Phase"],
            "data": [
                ["2025/06/30", "00:00", "12:00", "06:00", "New Moon"],
            ],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_moon_times(year=2025, month=6, day=30, lang="en")
        self.assertEqual(result, example_json)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                "dataType": "MRS",
                "lang": "en",
                "rformat": "json",
                "year": 2025,
                "month": "6",
                "day": "30",
            },
        )

    @patch("hkopenai.hk_climate_mcp_server.tools.astronomical.fetch_json_data")
    def test_get_sunrise_sunset_times_internal(self, mock_fetch_json_data):
        """Test the internal _get_sunrise_sunset_times function."""
        example_json = {
            "fields": ["Date", "Sunrise", "Sunset", "Sun Transit"],
            "data": [
                ["2025/06/30", "06:00", "18:00", "12:00"],
            ],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_sunrise_sunset_times(year=2025, lang="en")
        self.assertEqual(result, example_json)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                "dataType": "SRS",
                "lang": "en",
                "rformat": "json",
                "year": 2025,
            },
        )

    @patch("hkopenai.hk_climate_mcp_server.tools.astronomical.fetch_json_data")
    def test_get_gregorian_lunar_calendar_internal(self, mock_fetch_json_data):
        """Test the internal _get_gregorian_lunar_calendar function."""
        example_json = {
            "gregorianDate": "2025-06-30",
            "lunarDate": "2025-06-05",
            "chineseZodiac": "Snake",
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_gregorian_lunar_calendar(year=2025, month=6, day=30, lang="en")
        self.assertEqual(result, example_json)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/lunardate.php",
            params={"date": "2025-06-30"},
        )


if __name__ == "__main__":
    unittest.main()
