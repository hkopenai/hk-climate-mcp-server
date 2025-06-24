import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_climate_mcp_server.server import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_climate_mcp_server.server.FastMCP')
    @patch('hkopenai.hk_climate_mcp_server.server.tool_weather')
    def test_create_mcp_server(self, mock_tool_weather, mock_fastmcp):
        # Setup mocks
        mock_server = unittest.mock.Mock()
        
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
        mock_tool_weather.get_current_weather.return_value = {'test': 'data'}

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify all tools were decorated
        self.assertEqual(len(decorator_calls), 17)
        self.assertEqual(len(decorated_funcs), 17)
        
        # Test all tools
        for func in decorated_funcs:
            func_name = func.__name__
            try:
                if func_name == "get_current_weather":
                    result = func(region="test")
                    mock_tool_weather.get_current_weather.assert_called_once_with("test")
                elif func_name in ["get_9_day_weather_forecast", "get_local_weather_forecast",
                                 "get_weather_warning_summary", "get_weather_warning_info",
                                 "get_special_weather_tips"]:
                    result = func(lang="en")
                    getattr(mock_tool_weather, func_name).assert_called_once_with("en")
                elif func_name == "get_lightning_data":
                    result = func(lang="en", rformat="json")
                    getattr(mock_tool_weather, func_name).assert_called_once_with("en", "json")
                elif func_name == "get_visibility_data":
                    result = func(lang="en", rformat="json")
                    getattr(mock_tool_weather, func_name).assert_called_once_with("en", "json")
                elif func_name in ["get_moon_times", "get_sunrise_sunset_times",
                                 "get_gregorian_lunar_calendar"]:
                    result = func(year=2023, month=None, day=None, lang="en", rformat="json")
                    getattr(mock_tool_weather, func_name).assert_called_once_with(
                        year=2023, month=None, day=None, lang="en", rformat="json")
                elif func_name in ["get_hourly_tides", "get_high_low_tides"]:
                    result = func(station="HKO", year=2023, month=None, day=None, hour=None, lang="en", rformat="json")
                    getattr(mock_tool_weather, func_name).assert_called_once_with(
                        station="HKO", year=2023, month=None, day=None, hour=None, lang="en", rformat="json")
                elif func_name in ["get_daily_mean_temperature", "get_daily_max_temperature",
                                 "get_daily_min_temperature"]:
                    result = func(station="HKO", year=None, month=None, lang="en", rformat="json")
                    getattr(mock_tool_weather, func_name).assert_called_once_with(
                        station="HKO", year=None, month=None, lang="en", rformat="json")
                elif func_name == "get_weather_radiation_report":
                    result = func()
                    getattr(mock_tool_weather, func_name).assert_called_once()
                else:
                    result = func()
            except Exception as e:
                raise AssertionError(f"Failed to call {func_name}: {str(e)}")

if __name__ == "__main__":
    unittest.main()
