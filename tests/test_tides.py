"""
Unit tests for tides data retrieval functionality.

This module tests the tides-related functions from the tides tools module
to ensure they correctly fetch and process tides data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.tides import (
    register,
    _get_hourly_tides,
    _get_high_low_tides,
    _get_tide_station_codes,
)
from hkopenai.hk_climate_mcp_server.tools.tides import fetch_json_data


class TestTidesTools(unittest.TestCase):
    """Test case class for tides data tools."""

    def test_register_tool(self):
        """Tests that the tides tools are correctly registered."""
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 3)

        # Get the decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_mcp.tool.return_value.call_args_list
        }

        # Test get_hourly_tides
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.tides._get_hourly_tides"
        ) as mock_get_hourly_tides:
            decorated_funcs["get_hourly_tides"](
                station="TBT", year=2025, options={"month": 6, "day": 30}
            )
            mock_get_hourly_tides.assert_called_once_with(
                station="TBT", year=2025, month=6, day=30, hour=None, lang="en"
            )

        # Test get_high_low_tides
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.tides._get_high_low_tides"
        ) as mock_get_high_low_tides:
            decorated_funcs["get_high_low_tides"](
                station="TBT", year=2025, options={"month": 6}
            )
            mock_get_high_low_tides.assert_called_once_with(
                station="TBT", year=2025, month=6, day=None, hour=None, lang="en"
            )

        # Test get_tide_station_codes
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.tides._get_tide_station_codes"
        ) as mock_get_tide_station_codes:
            decorated_funcs["get_tide_station_codes"](lang="en")
            mock_get_tide_station_codes.assert_called_once_with("en")

    @patch("hkopenai.hk_climate_mcp_server.tools.tides.fetch_json_data")
    def test_get_hourly_tides_internal(self, mock_fetch_json_data):
        """Test the internal _get_hourly_tides function."""
        example_json = {
            "fields": ["Date", "Time", "Height"],
            "data": [
                ["2025/06/30", "00:00", "1.5"],
                ["2025/06/30", "01:00", "1.8"],
            ],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_hourly_tides(station="TBT", year=2025, month=6, day=30, lang="en")
        self.assertEqual(result, example_json)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                "dataType": "HHOT",
                "lang": "en",
                "rformat": "json",
                "station": "TBT",
                "year": 2025,
                "month": "6",
                "day": "30",
            },
            encoding="utf-8-sig",
        )

    @patch("hkopenai.hk_climate_mcp_server.tools.tides.fetch_json_data")
    def test_get_high_low_tides_internal(self, mock_fetch_json_data):
        """Test the internal _get_high_low_tides function."""
        example_json = {
            "fields": ["Date", "Time", "Height", "High/Low"],
            "data": [
                ["2025/06/30", "06:00", "2.5", "High"],
                ["2025/06/30", "12:00", "0.5", "Low"],
            ],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_high_low_tides(station="TBT", year=2025, month=6, lang="en")
        self.assertEqual(result, example_json)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                "dataType": "HLT",
                "lang": "en",
                "rformat": "json",
                "station": "TBT",
                "year": 2025,
                "month": "6",
            },
            encoding="utf-8-sig",
        )


if __name__ == "__main__":
    unittest.main()
