"""
Live Tests for Lightning Tools - Testing lightning data retrieval from HKO.

This module contains live tests for the lightning tools, making actual API calls to the
Hong Kong Observatory to retrieve lightning data. These tests are conditional and run
only when the environment variable RUN_LIVE_TESTS is set to 'true'.
"""

import unittest
import os
from hkopenai.hk_climate_mcp_server.tools.lightning import _get_lightning_data


class TestLightningToolsLive(unittest.TestCase):
    """
    Test case class for live testing of lightning data retrieval tools.

    This class contains test methods that make actual API calls to the Hong Kong Observatory
    to verify the functionality of lightning data retrieval functions. Tests are skipped unless
    the RUN_LIVE_TESTS environment variable is set to 'true'.
    """

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_lightning_data_live(self):
        """
        Live test to fetch actual lightning data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_lightning_data_live --live-tests
        """
        result = _get_lightning_data(lang="en")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_lightning_data_invalid_lang_live(self):
        """
        Live test to check error handling for an invalid language in get_lightning_data.
        """
        result = _get_lightning_data(lang="xx")  # An invalid language code

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result,
            "Result should contain an error field for invalid language",
        )
        self.assertIn("Failed to fetch data", result["error"])


if __name__ == "__main__":
    unittest.main()
