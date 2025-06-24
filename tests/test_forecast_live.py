import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.forecast import get_9_day_weather_forecast

class TestForecastToolsLive(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_9_day_weather_forecast_live(self):
        """
        Live test to fetch actual 9-day weather forecast data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_9_day_weather_forecast_live --live-tests
        """
        result = get_9_day_weather_forecast(lang="en")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

if __name__ == "__main__":
    unittest.main()
