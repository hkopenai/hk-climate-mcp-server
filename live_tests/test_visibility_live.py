"""Live unit tests for visibility data fetching functions."""

import os
import unittest
from hkopenai.hk_climate_mcp_server.tools.visibility import _get_visibility


class TestVisibilityToolsLive(unittest.TestCase):
    """Live tests for visibility data fetching functions."""

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_visibility_live(self):
        """
        Live test to fetch actual visibility data from Hong Kong Observatory.
        This test makes a real API call and should be run selectively.
        To run this test with pytest, use: pytest -k test_get_visibility_live --live-tests
        """
        result = _get_visibility(lang="en")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")

        # Check if the response contains an error field, which indicates a failure in data retrieval
        self.assertFalse("error" in result, result)

    @unittest.skipUnless(
        os.environ.get("RUN_LIVE_TESTS") == "true",
        "Set RUN_LIVE_TESTS=true to run live tests",
    )
    def test_get_visibility_invalid_lang_live(self):
        """
        Live test to check error handling for an invalid language in get_visibility.
        """
        result = _get_visibility(lang="xx")  # An invalid language code

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertTrue(
            "error" in result,
            "Result should contain an error field for invalid language",
        )
        self.assertIn("Failed to parse JSON response from API", result["error"])


if __name__ == "__main__":
    unittest.main()
