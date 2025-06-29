import unittest
import os
import subprocess
import sys
from hkopenai.hk_climate_mcp_server.tools.temperature import get_daily_mean_temperature, get_daily_max_temperature, get_daily_min_temperature

class TestTemperatureToolsLive(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_daily_mean_temperature_live(self):
        """
        Live test to fetch actual daily mean temperature data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_daily_mean_temperature_live --live-tests
        """
        result = get_daily_mean_temperature(station="HKO")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        
        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse('error' in result, result)

    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_daily_max_temperature_live(self):
        """
        Live test to fetch actual daily maximum temperature data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        """
        result = get_daily_max_temperature(station="HKO")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        
        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse('error' in result, result)

    @unittest.skipUnless(os.environ.get('RUN_LIVE_TESTS') == 'true', "Set RUN_LIVE_TESTS=true to run live tests")
    def test_get_daily_min_temperature_live(self):
        """
        Live test to fetch actual daily minimum temperature data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        """
        result = get_daily_min_temperature(station="HKO")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        
        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse('error' in result, result)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--run-all-live-tests":
        print("Running all live tests...")
        os.environ['RUN_LIVE_TESTS'] = 'true'
        test_files = [f for f in os.listdir('tests/') if '_live' in f and f.endswith('.py')]
        pytest_args = ['pytest', '-v'] + test_files
        print(f"Running live tests with command: {' '.join(pytest_args)}")
        result = subprocess.run(pytest_args, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    else:
        unittest.main()
