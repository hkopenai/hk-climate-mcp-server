"""Live unit tests for temperature data fetching functions."""

import os
import subprocess
import sys
import unittest
from hkopenai.hk_climate_mcp_server.tools.temperature import (
    _get_daily_mean_temperature,
    _get_daily_max_temperature,
    _get_daily_min_temperature,
)


class TestTemperatureToolsLive(unittest.TestCase):
    """Live tests for temperature data fetching functions."""

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_daily_mean_temperature_live(self):
        """
        Live test to fetch actual daily mean temperature data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_daily_mean_temperature_live --live-tests
        """
        result = _get_daily_mean_temperature(station="HKO")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_daily_max_temperature_live(self):
        """
        Live test to fetch actual daily maximum temperature data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        """
        result = _get_daily_max_temperature(station="HKO")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_daily_min_temperature_live(self):
        """
        Live test to fetch actual daily minimum temperature data from Hong Kong Observatory.
        """
        result = _get_daily_min_temperature(station="HKO")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        # Check if the response contains an.error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_daily_mean_temperature_invalid_station_live(self):
        """
        Live test to check error handling for an invalid station in get_daily_mean_temperature.
        """
        result = _get_daily_mean_temperature(station="INVALID")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result,
            "Result should contain an error field for invalid station",
        )
        self.assertIn("Failed to parse JSON response from API", result["error"])

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_daily_max_temperature_invalid_year_live(self):
        """
        Live test to check error handling for an invalid year in get_daily_max_temperature.
        """
        result = _get_daily_max_temperature(station="HKO", year=2050)  # Invalid year
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result, "Result should contain an error field for invalid year"
        )
        self.assertIn("Failed to parse JSON response from API", result["error"])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--run-all-live-tests":
        print("Running all live tests...")
        os.environ["RUN_LIVE_TESTS"] = "true"
        test_files = [
            f for f in os.listdir("tests/") if "_live" in f and f.endswith(".py")
        ]
        pytest_args = ["pytest", "-v"] + test_files
        print(f"Running live tests with command: {' '.join(pytest_args)}")
        result = subprocess.run(pytest_args, text=True, capture_output=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)
    else:
        unittest.main()
