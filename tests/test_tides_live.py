import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.tides import (
    get_high_low_tides,
    get_hourly_tides,
)


class TestTidesToolsLive(unittest.TestCase):
    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
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

        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_hourly_tides_live(self):
        """
        Live test to fetch actual hourly tides data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_hourly_tides_live --live-tests
        """
        from datetime import datetime

        current_year = datetime.now().year
        result = get_hourly_tides(station="QUB", year=current_year)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_high_low_tides_invalid_station_live(self):
        """
        Live test to check error handling for an invalid station code in get_high_low_tides.
        """
        from datetime import datetime

        current_year = datetime.now().year
        result = get_high_low_tides(station="INVALID", year=current_year)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result,
            "Result should contain an error field for invalid station",
        )
        self.assertIn("Invalid or missing station code", result["error"])


if __name__ == "__main__":
    unittest.main()
