"""Live unit tests for weather warnings data retrieval functionality."""

import os
import unittest
from hkopenai.hk_climate_mcp_server.tools.warnings import (
    _get_weather_warning_summary,
    _get_weather_warning_info,
    _get_special_weather_tips,
)


class TestWarningsToolsLive(unittest.TestCase):
    """Live tests for weather warnings data retrieval functionality."""

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_weather_warning_summary_live(self):
        """
        Live test to fetch actual weather warning summary data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_weather_warning_summary_live --live-tests
        """
        result = _get_weather_warning_summary(lang="en")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_weather_warning_summary_invalid_lang_live(self):
        """
        Live test to check error handling for an invalid language in get_weather_warning_summary.
        """
        lang = "xx"
        result = _get_weather_warning_summary(lang=lang)  # An invalid language code

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse(
            "error" in result, result
        )  # No error key expected for invalid language
        self.assertEqual(result["warningMessage"], [])
        self.assertEqual(result["updateTime"], "")

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_weather_warning_info_live(self):
        """
        Live test to fetch actual weather warning info data from Hong Kong Observatory.
        """
        result = _get_weather_warning_info(lang="en")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_weather_warning_info_invalid_lang_live(self):
        """
        Live test to check error handling for an invalid language in get_weather_warning_info.
        """
        lang = "xx"
        result = _get_weather_warning_info(lang=lang)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_special_weather_tips_live(self):
        """
        Live test to fetch actual special weather tips data from Hong Kong Observatory.
        """
        result = _get_special_weather_tips(lang="en")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_special_weather_tips_invalid_lang_live(self):
        """
        Live test to check error handling for an invalid language in get_special_weather_tips.
        """
        lang = "xx"
        result = _get_special_weather_tips(lang=lang)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertFalse("error" in result, result)


if __name__ == "__main__":
    unittest.main()
