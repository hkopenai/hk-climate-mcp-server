"""
Unit tests for moon times data retrieval functionality.

This module tests the `get_moon_times` function from the astronomical tools module
to ensure it correctly fetches and processes moon times data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.astronomical import register


class TestMoonTimesTools(unittest.TestCase):
    """Test case class for moon times data tools."""
    def test_register_tool(self):
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
        with patch("hkopenai.hk_climate_mcp_server.tools.astronomical._get_moon_times") as mock_get_moon_times:
            decorated_funcs["get_moon_times"](year=2025, month=6, day=30)
            mock_get_moon_times.assert_called_once_with(year=2025, month=6, day=30, lang="en")


if __name__ == "__main__":
    unittest.main()
