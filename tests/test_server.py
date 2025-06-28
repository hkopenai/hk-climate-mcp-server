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


if __name__ == "__main__":
    unittest.main()
