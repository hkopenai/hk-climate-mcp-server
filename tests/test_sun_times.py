"""
Unit tests for sunrise and sunset times data retrieval functionality.

This module tests the `get_sunrise_sunset_times` function from the astronomical tools module
to ensure it correctly fetches and processes sun times data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.astronomical import register


class TestSunTimesTools(unittest.TestCase):
    """Test case class for sun times data tools."""

    def test_register_tool(self):
        """Tests that the sun times tool is correctly registered."""
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 3)

        # Get the decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_mcp.tool.return_value.call_args_list
        }

        # Test get_sunrise_sunset_times
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.astronomical._get_sunrise_sunset_times"
        ) as mock_get_sunrise_sunset_times:
            decorated_funcs["get_sunrise_sunset_times"](year=2025)
            mock_get_sunrise_sunset_times.assert_called_once_with(
                year=2025, month=None, day=None, lang="en"
            )


if __name__ == "__main__":
    unittest.main()
