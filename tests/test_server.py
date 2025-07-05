import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_climate_mcp_server.server import create_mcp_server

class TestApp(unittest.TestCase):
    @patch('hkopenai.hk_climate_mcp_server.server.FastMCP')
    @patch('hkopenai.hk_climate_mcp_server.server.current_weather')
    @patch('hkopenai.hk_climate_mcp_server.server.forecast')
    @patch('hkopenai.hk_climate_mcp_server.server.warnings')
    @patch('hkopenai.hk_climate_mcp_server.server.lightning')
    @patch('hkopenai.hk_climate_mcp_server.server.visibility')
    @patch('hkopenai.hk_climate_mcp_server.server.tides')
    @patch('hkopenai.hk_climate_mcp_server.server.temperature')
    @patch('hkopenai.hk_climate_mcp_server.server.radiation')
    @patch('hkopenai.hk_climate_mcp_server.server.astronomical')
    def test_create_mcp_server(self, mock_astronomical, mock_radiation, mock_temperature, mock_tides, mock_visibility, mock_lightning, mock_warnings, mock_forecast, mock_current_weather, mock_fastmcp):
        # Setup mocks
        mock_server = Mock()
        
        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify that the tool decorator was called for each tool function
        self.assertEqual(mock_server.tool.call_count, 19)

        # Get all decorated functions
        decorated_funcs = {call.args[0].__name__: call.args[0] for call in mock_server.tool.return_value.call_args_list}
        self.assertEqual(len(decorated_funcs), 19)

        # Call each decorated function and verify that the correct underlying function is called
        
        decorated_funcs['get_current_weather'](region="test")
        mock_current_weather.get_current_weather.assert_called_once_with("test")

        decorated_funcs['get_9_day_weather_forecast'](lang="tc")
        mock_forecast.get_9_day_weather_forecast.assert_called_once_with("tc")

        decorated_funcs['get_local_weather_forecast'](lang="sc")
        mock_forecast.get_local_weather_forecast.assert_called_once_with("sc")

        decorated_funcs['get_weather_warning_summary']()
        mock_warnings.get_weather_warning_summary.assert_called_once_with("en")

        decorated_funcs['get_weather_warning_info']()
        mock_warnings.get_weather_warning_info.assert_called_once_with("en")

        decorated_funcs['get_special_weather_tips']()
        mock_warnings.get_special_weather_tips.assert_called_once_with("en")

        decorated_funcs['get_visibility_data']()
        mock_visibility.get_visibility_data.assert_called_once_with("en")

        decorated_funcs['get_lightning_data']()
        mock_lightning.get_lightning_data.assert_called_once_with("en")

        decorated_funcs['get_moon_times'](year=2025, month=6, day=30)
        mock_astronomical.get_moon_times.assert_called_once_with(year=2025, month=6, day=30, lang="en")

        decorated_funcs['get_hourly_tides'](station="TBT", year=2025, options={"month": 6, "day": 30})
        mock_tides.get_hourly_tides.assert_called_once_with(station="TBT", year=2025, month=6, day=30, hour=None, lang="en")

        decorated_funcs['get_high_low_tides'](station="TBT", year=2025, options={"month": 6})
        mock_tides.get_high_low_tides.assert_called_once_with(station="TBT", year=2025, month=6, day=None, hour=None, lang="en")

        decorated_funcs['get_tide_station_codes']()
        mock_tides.get_tide_station_codes.assert_called_once_with("en")

        decorated_funcs['get_sunrise_sunset_times'](year=2025)
        mock_astronomical.get_sunrise_sunset_times.assert_called_once_with(year=2025, month=None, day=None, lang="en")

        decorated_funcs['get_gregorian_lunar_calendar'](year=2025, month=6)
        mock_astronomical.get_gregorian_lunar_calendar.assert_called_once_with(year=2025, month=6, day=None, lang="en")

        decorated_funcs['get_daily_mean_temperature'](station="HKO", year=2025)
        mock_temperature.get_daily_mean_temperature.assert_called_once_with(station="HKO", year=2025, month=None, lang="en")

        decorated_funcs['get_daily_max_temperature'](station="HKO", year=2025, month=6)
        mock_temperature.get_daily_max_temperature.assert_called_once_with(station="HKO", year=2025, month=6, lang="en")

        decorated_funcs['get_daily_min_temperature'](station="HKO")
        mock_temperature.get_daily_min_temperature.assert_called_once_with(station="HKO", year=None, month=None, lang="en")

        decorated_funcs['get_weather_radiation_report'](date="20250629", station="HKO")
        mock_radiation.get_weather_radiation_report.assert_called_once_with(date="20250629", station="HKO", lang="en")

        decorated_funcs['get_radiation_station_codes'](lang="en")
        mock_radiation.get_radiation_station_codes.assert_called_once_with("en")


if __name__ == "__main__":
    unittest.main()
