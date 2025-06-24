import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.tides import get_high_low_tides

class TestTidesToolsLive(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_high_low_tides_live(self):
        """
        Live test to fetch actual high and low tides data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_high_low_tides_live --live-tests
        """
        from datetime import datetime
        current_year = datetime.now().year
        result = get_high_low_tides(station="QUB", year=current_year)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

if __name__ == "__main__":
    unittest.main()
