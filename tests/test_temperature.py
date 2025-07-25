"""
Unit tests for temperature data retrieval functionality.

This module tests the temperature-related functions from the temperature tools module
to ensure they correctly fetch and process temperature data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.temperature import (
    register,
    _get_daily_mean_temperature,
    _get_daily_max_temperature,
    _get_daily_min_temperature,
)
from hkopenai_common.json_utils import fetch_json_data


class TestTemperatureTools(unittest.TestCase):
    """Test case class for temperature data tools."""

    def test_register_tool(self):
        """Tests that the temperature tools are correctly registered."""
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 3)

        # Get the decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_mcp.tool.return_value.call_args_list
        }

        # Test get_daily_mean_temperature
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.temperature._get_daily_mean_temperature"
        ) as mock_get_daily_mean_temperature:
            decorated_funcs["get_daily_mean_temperature"](station="HKO", year=2025)
            mock_get_daily_mean_temperature.assert_called_once_with(
                station="HKO", year=2025, month=None, lang="en"
            )

        # Test get_daily_max_temperature
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.temperature._get_daily_max_temperature"
        ) as mock_get_daily_max_temperature:
            decorated_funcs["get_daily_max_temperature"](
                station="HKO", year=2025, month=6
            )
            mock_get_daily_max_temperature.assert_called_once_with(
                station="HKO", year=2025, month=6, lang="en"
            )

        # Test get_daily_min_temperature
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.temperature._get_daily_min_temperature"
        ) as mock_get_daily_min_temperature:
            decorated_funcs["get_daily_min_temperature"](station="HKO")
            mock_get_daily_min_temperature.assert_called_once_with(
                station="HKO", year=None, month=None, lang="en"
            )

    @patch("hkopenai.hk_climate_mcp_server.tools.temperature.fetch_json_data")
    def test_get_daily_mean_temperature_internal(self, mock_fetch_json_data):
        """Test the internal _get_daily_mean_temperature function."""
        example_json = {
            "fields": ["Year", "Month", "Day", "Mean Temperature"],
            "data": [
                [2025, 6, 23, 28.5],
            ],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_daily_mean_temperature(
            station="HKO", year=2025, month=6, lang="en"
        )
        self.assertEqual(result, example_json)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                "dataType": "CLMTEMP",
                "lang": "en",
                "rformat": "json",
                "station": "HKO",
                "year": "2025",
                "month": "6",
            },
        )

    @patch("hkopenai.hk_climate_mcp_server.tools.temperature.fetch_json_data")
    def test_get_daily_max_temperature_internal(self, mock_fetch_json_data):
        """Test the internal _get_daily_max_temperature function."""
        example_json = {
            "fields": ["Year", "Month", "Day", "Max Temperature"],
            "data": [
                [2025, 6, 23, 32.1],
            ],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_daily_max_temperature(
            station="HKO", year=2025, month=6, lang="en"
        )
        self.assertEqual(result, example_json)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                "dataType": "CLMMAXT",
                "lang": "en",
                "rformat": "json",
                "station": "HKO",
                "year": "2025",
                "month": "6",
            },
        )

    @patch("hkopenai.hk_climate_mcp_server.tools.temperature.fetch_json_data")
    def test_get_daily_min_temperature_internal(self, mock_fetch_json_data):
        """Test the internal _get_daily_min_temperature function."""
        example_json = {
            "fields": ["Year", "Month", "Day", "Min Temperature"],
            "data": [
                [2025, 6, 23, 25.0],
            ],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_daily_min_temperature(
            station="HKO", year=2025, month=6, lang="en"
        )
        self.assertEqual(result, example_json)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                "dataType": "CLMMINT",
                "lang": "en",
                "rformat": "json",
                "station": "HKO",
                "year": "2025",
                "month": "6",
            },
        )


if __name__ == "__main__":
    unittest.main()
