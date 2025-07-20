"""
Unit tests for lightning data retrieval functionality.

This module tests the `get_lightning_data` function from the lightning tools module
to ensure it correctly fetches and processes lightning data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.lightning import register, _get_lightning_data
from hkopenai.hk_climate_mcp_server.tools.lightning import fetch_json_data


class TestLightningTools(unittest.TestCase):
    """Test case class for lightning data tools."""

    def test_register_tool(self):
        """Tests that the lightning data tool is correctly registered."""
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 1)

        # Get the decorated function
        decorated_func = mock_mcp.tool.return_value.call_args[0][0]

        # Test get_lightning_data
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.lightning._get_lightning_data"
        ) as mock_get_lightning_data:
            decorated_func(lang="en")
            mock_get_lightning_data.assert_called_once_with("en")

    @patch("hkopenai.hk_climate_mcp_server.tools.lightning.fetch_json_data")
    def test_get_lightning_data_internal(self, mock_fetch_json_data):
        """Test the internal _get_lightning_data function."""
        example_json = {
            "fields": ["Time", "Cloud-to-ground", "Cloud-to-cloud"],
            "data": [
                ["202506231400", 10, 5],
                ["202506231410", 12, 7],
            ],
        }
        mock_fetch_json_data.return_value = example_json

        result = _get_lightning_data(lang="en")
        self.assertEqual(result, example_json)
        mock_fetch_json_data.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LHL&lang=en&rformat=json"
        )


if __name__ == "__main__":
    unittest.main()
