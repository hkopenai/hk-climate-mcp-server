import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.visibility import get_visibility_data

class TestVisibilityToolsLive(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_visibility_data_live(self):
        """
        Live test to fetch actual visibility data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_visibility_data_live --live-tests
        """
        result = get_visibility_data(lang="en")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        
        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse('error' in result, result)

if __name__ == "__main__":
    unittest.main()
