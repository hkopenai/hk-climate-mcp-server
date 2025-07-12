"""
Unit tests for weather warnings data retrieval functionality.

This module tests the warnings-related functions from the warnings tools module
to ensure they correctly fetch and process weather warnings data from the HKO API.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.warnings import register


class TestWarningsTools(unittest.TestCase):
    """Test case class for weather warnings data tools."""

    def test_register_tool(self):
        """Tests that the warnings tools are correctly registered."""
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 3)

        # Get the decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_mcp.tool.return_value.call_args_list
        }

        # Test get_weather_warning_summary
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.warnings._get_weather_warning_summary"
        ) as mock_get_weather_warning_summary:
            decorated_funcs["get_weather_warning_summary"](lang="en")
            mock_get_weather_warning_summary.assert_called_once_with("en")

        # Test get_weather_warning_info
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.warnings._get_weather_warning_info"
        ) as mock_get_weather_warning_info:
            decorated_funcs["get_weather_warning_info"](lang="en")
            mock_get_weather_warning_info.assert_called_once_with("en")

        # Test get_special_weather_tips
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.warnings._get_special_weather_tips"
        ) as mock_get_special_weather_tips:
            decorated_funcs["get_special_weather_tips"](lang="en")
            mock_get_special_weather_tips.assert_called_once_with("en")


if __name__ == "__main__":
    unittest.main()
