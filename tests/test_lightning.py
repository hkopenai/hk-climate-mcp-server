"""
Unit tests for lightning data retrieval functionality.

This module tests the `get_lightning_data` function from the lightning tools module
to ensure it correctly fetches and processes lightning data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.lightning import register


class TestLightningTools(unittest.TestCase):
    """Test case class for lightning data tools."""
    def test_register_tool(self):
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 1)

        # Get the decorated function
        decorated_func = mock_mcp.tool.return_value.call_args[0][0]

        # Test get_lightning_data
        with patch("hkopenai.hk_climate_mcp_server.tools.lightning._get_lightning_data") as mock_get_lightning_data:
            decorated_func(lang="en")
            mock_get_lightning_data.assert_called_once_with("en")


if __name__ == "__main__":
    unittest.main()
