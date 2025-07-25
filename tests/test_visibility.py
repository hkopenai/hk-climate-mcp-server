"""
Unit tests for visibility data retrieval functionality.

This module tests the `get_visibility` function from the visibility tools module
to ensure it correctly fetches and processes visibility data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.visibility import register, _get_visibility
from hkopenai.hk_climate_mcp_server.tools.visibility import fetch_json_data


class TestVisibilityTools(unittest.TestCase):
    """Test case class for visibility data tools."""

    @patch("hkopenai.hk_climate_mcp_server.tools.visibility.fetch_json_data")
    def test_get_visibility_internal(self, mock_fetch_json_data):
        """
        Test the internal _get_visibility function.
        """
        example_json = {
            "fields": [
                "Date time",
                "Automatic Weather Station",
                "10 minute mean visibility",
            ],
            "data": [
                ["202506231320", "Central", "35 km"],
                ["202506231320", "Chek Lap Kok", "50 km"],
            ],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_visibility(lang="en")
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LTMV&lang=en&rformat=json"
        )

    def test_register_tool(self):
        """Tests that the visibility tool is correctly registered."""
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get latest 10-minute mean visibility data for Hong Kong"
        )


if __name__ == "__main__":
    unittest.main()
