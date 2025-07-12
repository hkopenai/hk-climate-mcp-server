"""
Unit tests for astronomical data fetching functions.

This module tests the functionality of fetching astronomical data such as Gregorian-Lunar calendar conversions from the Hong Kong Observatory API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.astronomical import register


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


if __name__ == "__main__":
    unittest.main()
