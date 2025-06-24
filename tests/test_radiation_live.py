import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.radiation import get_weather_radiation_report

class TestRadiationToolsLive(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_weather_radiation_report_live(self):
        """
        Live test to fetch actual weather radiation data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_weather_radiation_report_live --live-tests
        """
        from datetime import datetime, timedelta
        # Use yesterday's date in YYYYMMDD format
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        result = get_weather_radiation_report(date=yesterday, station='HKO')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

if __name__ == "__main__":
    unittest.main()
