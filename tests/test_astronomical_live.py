import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.astronomical import get_sunrise_sunset_times

class TestAstronomicalToolsLive(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_sunrise_sunset_times_live(self):
        """
        Live test to fetch actual sunrise and sunset times data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_sunrise_sunset_times_live --live-tests
        """
        from datetime import datetime
        current_year = datetime.now().year
        result = get_sunrise_sunset_times(year=current_year)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        
        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse('error' in result, result)

    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_sunrise_sunset_times_invalid_year_live(self):
        """
        Live test to check error handling for an invalid year in get_sunrise_sunset_times.
        """
        result = get_sunrise_sunset_times(year=2000) # An invalid year outside the 2018-2024 range
        
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue('error' in result, "Result should contain an error field for invalid year")
        self.assertIn("Failed to fetch data", result['error'])

if __name__ == "__main__":
    unittest.main()