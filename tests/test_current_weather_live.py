"""
Live unit tests for current weather data fetching functions.

This module tests the functionality of fetching real-time current weather data from the Hong Kong Observatory API.
"""

import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.current_weather import get_current_weather


class TestCurrentWeatherToolsLive(unittest.TestCase):
    """
    Test case class for live testing of current weather data fetching tools and functions.
    """

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_current_weather_live(self):
        """
        Live test to fetch actual current weather data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_current_weather_live --live-tests
        """
        result = get_current_weather(region="Hong Kong Observatory")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_current_weather_invalid_region_live(self):
        """
        Live test to check behavior with an invalid region in get_current_weather.
        """
        result = get_current_weather(region="Invalid Region")

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse(
            "error" in result, result
        )  # Should not return an error, but default to HKO
        self.assertEqual(
            result["weatherObservation"]["temperature"]["place"],
            "Hong Kong Observatory",
        )
        self.assertEqual(
            result["weatherObservation"]["humidity"]["place"], "Hong Kong Observatory"
        )


if __name__ == "__main__":
    unittest.main()
