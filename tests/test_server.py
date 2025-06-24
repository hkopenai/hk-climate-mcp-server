import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_climate_mcp_server.server import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_climate_mcp_server.server.FastMCP')
    @patch('hkopenai.hk_climate_mcp_server.tools.current_weather')
    @patch('hkopenai.hk_climate_mcp_server.tools.forecast')
    @patch('hkopenai.hk_climate_mcp_server.tools.warnings')
    @patch('hkopenai.hk_climate_mcp_server.tools.lightning')
    @patch('hkopenai.hk_climate_mcp_server.tools.visibility')
    @patch('hkopenai.hk_climate_mcp_server.tools.tides')
    @patch('hkopenai.hk_climate_mcp_server.tools.temperature')
    @patch('hkopenai.hk_climate_mcp_server.tools.radiation')
    @patch('hkopenai.hk_climate_mcp_server.tools.astronomical')
    def test_create_mcp_server(self, mock_astronomical, mock_radiation, mock_temperature, mock_tides, mock_visibility, mock_lightning, mock_warnings, mock_forecast, mock_current_weather, mock_fastmcp):
        # Setup mocks
        mock_server = Mock()
        
        # Track decorator calls and capture decorated functions
        decorator_calls = []
        decorated_funcs = []
        
        def tool_decorator(description=None):
            # First call: @tool(description=...)
            decorator_calls.append(((), {'description': description}))
            
            def decorator(f):
                # Second call: decorator(function)
                decorated_funcs.append(f)
                return f
                
            return decorator
            
        mock_server.tool = tool_decorator
        mock_server.tool.call_args = None  # Initialize call_args
        mock_fastmcp.return_value = mock_server
        mock_current_weather.get_current_weather.return_value = {'test': 'data'}

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify all tools were decorated
        self.assertEqual(len(decorator_calls), 17)
        self.assertEqual(len(decorated_funcs), 17)
        
        # Verify that tools are registered (we don't call them directly to avoid mock issues)
        # Instead, we check if the expected number of tools are decorated
        expected_tools = [
            "get_current_weather", "get_9_day_weather_forecast", "get_local_weather_forecast",
            "get_weather_warning_summary", "get_weather_warning_info", "get_special_weather_tips",
            "get_lightning_data", "get_visibility_data", "get_moon_times", "get_sunrise_sunset_times",
            "get_gregorian_lunar_calendar", "get_hourly_tides", "get_high_low_tides",
            "get_daily_mean_temperature", "get_daily_max_temperature", "get_daily_min_temperature",
            "get_weather_radiation_report"
        ]
        registered_tools = [func.__name__ for func in decorated_funcs]
        self.assertEqual(set(registered_tools), set(expected_tools), "Not all expected tools are registered")

if __name__ == "__main__":
    unittest.main()
