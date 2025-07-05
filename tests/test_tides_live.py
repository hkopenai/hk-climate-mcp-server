"""
Unit Tests for Tides Tools (Live)

This module contains live unit tests for the tides tools provided by the HKO MCP Server.
It tests the functionality of fetching high/low and hourly tides data using real API calls.
These tests are skipped by default unless the RUN_LIVE_TESTS environment variable is set to 'true'.
"""

import unittest
import os
from datetime import datetime
from hkopenai.hk_climate_mcp_server.tools.tides import (
    get_high_low_tides,
    get_hourly_tides,
)


class TestTidesToolsLive(unittest.TestCase):
    """
    Test case class for live testing of tides tools.
    
    This class contains test methods to verify the correct functioning of 
    tides data retrieval functions using real API calls to the Hong Kong Observatory.
    Tests are skipped unless the RUN_LIVE_TESTS environment variable is set to 'true'.
    """
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
