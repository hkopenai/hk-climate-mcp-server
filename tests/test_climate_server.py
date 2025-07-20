"""Unit tests for the MCP server creation and tool registration."""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_climate_mcp_server.server import server


class TestApp(unittest.TestCase):
    """Test case class for MCP server functionality."""

    @patch("hkopenai.hk_climate_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_climate_mcp_server.tools.astronomical.register")
    @patch("hkopenai.hk_climate_mcp_server.tools.current_weather.register")
    @patch("hkopenai.hk_climate_mcp_server.tools.forecast.register")
    @patch("hkopenai.hk_climate_mcp_server.tools.lightning.register")
    @patch("hkopenai.hk_climate_mcp_server.tools.radiation.register")
    @patch("hkopenai.hk_climate_mcp_server.tools.temperature.register")
    @patch("hkopenai.hk_climate_mcp_server.tools.tides.register")
    @patch("hkopenai.hk_climate_mcp_server.tools.visibility.register")
    @patch("hkopenai.hk_climate_mcp_server.tools.warnings.register")
    def test_create_mcp_server(
        self,
        mock_warnings_register,
        mock_visibility_register,
        mock_tides_register,
        mock_temperature_register,
        mock_radiation_register,
        mock_lightning_register,
        mock_forecast_register,
        mock_current_weather_register,
        mock_astronomical_register,
        mock_fastmcp,
    ):
        """
        Test the creation of the MCP server and its tool integrations.
        """
        # Setup mocks
        mock_server = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server_instance = server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server_instance, mock_server)

        # Verify that the register function of each tool module was called with the mcp instance
        mock_astronomical_register.assert_called_once_with(mock_server)
        mock_current_weather_register.assert_called_once_with(mock_server)
        mock_forecast_register.assert_called_once_with(mock_server)
        mock_lightning_register.assert_called_once_with(mock_server)
        mock_radiation_register.assert_called_once_with(mock_server)
        mock_temperature_register.assert_called_once_with(mock_server)
        mock_tides_register.assert_called_once_with(mock_server)
        mock_visibility_register.assert_called_once_with(mock_server)
        mock_warnings_register.assert_called_once_with(mock_server)


if __name__ == "__main__":
    unittest.main()
