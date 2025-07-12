import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.radiation import _get_weather_radiation_report
from datetime import datetime, timedelta


class TestRadiationToolsLive(unittest.TestCase):
    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_weather_radiation_report_live(self):
        """
        Live test to fetch actual weather radiation data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_weather_radiation_report_live --live-tests
        """
        # Use yesterday's date in YYYYMMDD format
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        result = _get_weather_radiation_report(date=yesterday, station="HKO")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("Failed" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_weather_radiation_report_invalid_date_format_live(self):
        """
        Live test to check error handling for an invalid date format in get_weather_radiation_report.
        """
        result = _get_weather_radiation_report(
            date="2025-06-18", station="HKO"
        )  # Invalid date format

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result,
            "Result should contain an error field for invalid date format",
        )
        self.assertIn("Invalid date format", result["error"])

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_weather_radiation_report_future_date_live(self):
        """
        Live test to check error handling for a future date in get_weather_radiation_report.
        """
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
        result = _get_weather_radiation_report(
            date=tomorrow, station="HKO"
        )  # Future date

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result, "Result should contain an error field for future date"
        )
        self.assertIn("Date must be yesterday or before", result["error"])

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_weather_radiation_report_invalid_station_live(self):
        """
        Live test to check error handling for an invalid station in get_weather_radiation_report.
        """
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        result = _get_weather_radiation_report(
            date=yesterday, station="INVALID"
        )  # Invalid station

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result,
            "Result should contain an error field for invalid station",
        )
        self.assertIn("Invalid or missing station code", result["error"])


if __name__ == "__main__":
    unittest.main()
