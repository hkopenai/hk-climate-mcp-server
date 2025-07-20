"""
Live unit tests for current weather data fetching functions.

This module tests the functionality of fetching real-time current weather data from the Hong Kong Observatory API.
"""

import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.current_weather import _get_current_weather


class TestCurrentWeatherToolsLive(unittest.TestCase):
    """Live tests for current weather data fetching functions."""

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_current_weather_live(self):
        """Tests fetching current weather data live."""
        result = _get_current_weather(region="Hong Kong Observatory")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_current_weather_invalid_region_live(self):
        """Tests fetching current weather data with an invalid region live."""
        result = _get_current_weather(region="Invalid Region")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse("error" in result, result)
        self.assertEqual(
            result["weatherObservation"]["temperature"]["place"],
            "Hong Kong Observatory",
        )
        self.assertEqual(
            result["weatherObservation"]["humidity"]["place"], "Hong Kong Observatory"
        )


if __name__ == "__main__":
    unittest.main()
