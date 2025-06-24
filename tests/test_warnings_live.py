import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.warnings import get_weather_warning_summary

class TestWarningsToolsLive(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_weather_warning_summary_live(self):
        """
        Live test to fetch actual weather warning summary data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_weather_warning_summary_live --live-tests
        """
        result = get_weather_warning_summary(lang="en")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

if __name__ == "__main__":
    unittest.main()
