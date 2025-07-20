"""
Live Tests for Forecast Tools - Testing weather forecast data retrieval from HKO.

This module contains live tests for the forecast tools, making actual API calls to the
Hong Kong Observatory to retrieve weather forecast data. These tests are conditional
and run only when the environment variable RUN_LIVE_TESTS is set to 'true'.
"""

import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.forecast import _get_9_day_weather_forecast


class TestForecastToolsLive(unittest.TestCase):
    """
    Test case class for live testing of forecast data retrieval tools.

    This class contains test methods that make actual API calls to the Hong Kong Observatory
    to verify the functionality of forecast data retrieval functions. Tests are skipped unless
    the RUN_LIVE_TESTS environment variable is set to 'true'.
    """

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_9_day_weather_forecast_live(self):
        """
        Live test to fetch actual 9-day weather forecast data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_9_day_weather_forecast_live --live-tests
        """
        result = _get_9_day_weather_forecast(lang="en")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_9_day_weather_forecast_invalid_lang_live(self):
        """
        Live test to check error handling for an invalid language in get_9_day_weather_forecast.
        """
        lang = "xx"
        result = _get_9_day_weather_forecast(lang=lang)  # An invalid language code

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse(
            "error" in result, result
        )  # No error key expected for invalid language
        self.assertEqual(result["generalSituation"], "")
        self.assertEqual(result["weatherForecast"], [])


if __name__ == "__main__":
    unittest.main()
