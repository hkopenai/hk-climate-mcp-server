"""
Live unit tests for astronomical data fetching functions.

This module tests the functionality of fetching real-time astronomical data such as sunrise/sunset times and Gregorian-Lunar calendar conversions from the Hong Kong Observatory API.
"""

import unittest
import os
from datetime import datetime
from hkopenai.hk_climate_mcp_server.tools.astronomical import (
    get_sunrise_sunset_times,
    get_gregorian_lunar_calendar,
)


class TestAstronomicalToolsLive(unittest.TestCase):
    """
    Test case class for live testing of astronomical data fetching tools and functions.
    """

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_sunrise_sunset_times_live(self):
        """
        Live test to fetch actual sunrise and sunset times data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_sunrise_sunset_times_live --live-tests
        """
        current_year = datetime.now().year
        result = get_sunrise_sunset_times(year=current_year)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_sunrise_sunset_times_invalid_year_live(self):
        """
        Live test to check error handling for an invalid year in get_sunrise_sunset_times.
        """
        result = get_sunrise_sunset_times(
            year=2000
        )  # An invalid year outside the 2018-2024 range

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result, "Result should contain an error field for invalid year"
        )
        self.assertIn("Failed to fetch data", result["error"])

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_gregorian_lunar_calendar_live(self):
        """
        Live test to fetch actual gregorian lunar calendar data from Hong Kong Observatory.
        """
        current_year = datetime.now().year
        result = get_gregorian_lunar_calendar(year=current_year)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_gregorian_lunar_calendar_invalid_year_live(self):
        """
        Live test to check error handling for an invalid year in get_gregorian_lunar_calendar.
        """
        result = get_gregorian_lunar_calendar(
            year=1800
        )  # An invalid year outside the 1901-2100 range

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result, "Result should contain an error field for invalid year"
        )
        self.assertIn("Failed to fetch data", result["error"])


if __name__ == "__main__":
    unittest.main()
