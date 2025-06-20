import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_climate_mcp_server.app import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_climate_mcp_server.app.FastMCP')
    @patch('hkopenai.hk_climate_mcp_server.app.tool_weather')
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

        # Verify both tools were decorated
        self.assertEqual(len(decorator_calls), 2)
        self.assertEqual(len(decorated_funcs), 2)
        
        # Test both tools
        for func in decorated_funcs:
            try:
                # Try calling with region parameter (for get_current_weather)
                result = func(region="test")
                mock_tool_weather.get_current_weather.assert_called_once_with("test")
            except TypeError:
                # If TypeError, it's get_9_day_weather_forecast
                result = func()
                mock_tool_weather.get_9_day_weather_forecast.assert_called_once()

if __name__ == "__main__":
    unittest.main()
