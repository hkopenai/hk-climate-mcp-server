"""Unit tests for the radiation data retrieval functionality.

This module contains tests for the get_weather_radiation_report function,
ensuring it handles various input scenarios and API responses correctly.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests
from hkopenai.hk_climate_mcp_server.tools.radiation import (
    register,
    _get_weather_radiation_report,
)


class TestRadiationTools(unittest.TestCase):
    """Test case class for radiation data retrieval tools."""

    EXAMPLE_JSON = {
        "ChekLapKokLocationName": "Chek Lap Kok",
        "ChekLapKokMaxTemp": "32.7",
        "ChekLapKokMicrosieverts": "0.15",
        "ChekLapKokMinTemp": "28.2",
        "BulletinTime": "0015",
        "BulletinDate": "20250624",
        "ReportTimeInfoDate": "20250623",
        "HongKongDesc": "Average ambient gamma radiation dose rate taken outdoors in Hong "
        "Kong ranged from 0.08 to 0.15 microsievert per hour. These are "
        "within the normal range of fluctuation of the background radiation "
        "level in Hong Kong.",
        "NoteDesc": "From readings taken at various locations in Hong Kong in the past, "
        "the hourly mean ambient gamma radiation dose rate may vary between "
        "0.06 and 0.3 microsievert per hour. (1 microsievert = 0.000001 "
        "sievert = 0.001 millisievert)",
        "NoteDesc1": "Temporal variations are generally caused by changes in meteorological "
        "conditions such as rainfall, wind and barometric pressure.",
        "NoteDesc2": "Spatial variations are generally caused by differences in the radioactive "
        "content of local rock and soil.",
        "NoteDesc3": "The data displayed is provisional. Only limited data validation has been "
        "carried out.",
    }

    @patch("requests.get")
    def test_get_weather_radiation_report(self, mock_get):
        """Test retrieval of radiation report with valid parameters."""
        mock_response = MagicMock()
        mock_response.json.return_value = self.EXAMPLE_JSON
        mock_get.return_value = mock_response

        result = _get_weather_radiation_report(date="20250623", station="HKO")
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                "dataType": "RYES",
                "lang": "en",
                "rformat": "json",
                "date": "20250623",
                "station": "HKO",
            },
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a " "dictionary")
        self.assertIn(
            "ChekLapKokLocationName", result, "Result should contain expected keys"
        )

    def test_get_weather_radiation_report_missing_station(self):
        """Test handling of missing station parameter."""
        result = _get_weather_radiation_report(date="20250623", station="")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn(
            "error", result, "Result should contain error message for missing station"
        )

    def test_get_weather_radiation_report_invalid_station(self):
        """Test handling of invalid station parameter."""
        result = _get_weather_radiation_report(date="20250623", station="INVALID")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn(
            "error", result, "Result should contain error message for invalid station"
        )

    def test_get_weather_radiation_report_missing_date(self):
        """Test handling of missing date parameter."""
        result = _get_weather_radiation_report(date="", station="HKO")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn(
            "error", result, "Result should contain error message for missing date"
        )

    def test_get_weather_radiation_report_invalid_date_format(self):
        """Test handling of invalid date format."""
        result = _get_weather_radiation_report(date="2025-06-23", station="HKO")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn(
            "error",
            result,
            "Result should contain error message for invalid date format",
        )

    @patch("hkopenai.hk_climate_mcp_server.tools.radiation.is_date_in_future")
    @patch("requests.get")
    def test_get_weather_radiation_report_yesterday_valid(
        self, mock_get, mock_date_check
    ):
        """Test retrieval of radiation report for yesterday's date."""
        mock_date_check.return_value = False
        mock_response = MagicMock()
        mock_response.json.return_value = self.EXAMPLE_JSON
        mock_get.return_value = mock_response

        result = _get_weather_radiation_report(date="20250623", station="HKO")
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                "dataType": "RYES",
                "lang": "en",
                "rformat": "json",
                "date": "20250623",
                "station": "HKO",
            },
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertNotIn(
            "error", result, "Result should not contain error for yesterday's date"
        )
        self.assertIn(
            "ChekLapKokLocationName", result, "Result should contain expected keys"
        )

    @patch("hkopenai.hk_climate_mcp_server.tools.radiation.is_date_in_future")
    def test_get_weather_radiation_report_date_in_future(self, mock_date_check):
        """Test handling of future date input for radiation report."""
        mock_date_check.return_value = True
        result = _get_weather_radiation_report(date="20250625", station="HKO")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn(
            "error",
            result,
            "Result should contain error message " "for date being in the future",
        )
        self.assertIn(
            "Date must be yesterday or before",
            result["error"],
            "Error must note date must be yesterday or prior",
        )

    @patch("requests.get")
    def test_get_weather_radiation_report_non_json_response(self, mock_get):
        """Test error handling for non-JSON response."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = _get_weather_radiation_report(date="20230618", station="HKO")
        self.assertIn("error", result)
        self.assertEqual(
            result["error"],
            "Failed to parse JSON response from API. The API might have returned non-JSON data or an empty response.",
        )

    @patch("requests.get")
    def test_get_weather_radiation_report_request_exception(self, mock_get):
        """Test error handling for request exceptions."""
        mock_get.side_effect = requests.RequestException("Network error")

        result = _get_weather_radiation_report(date="20230618", station="HKO")
        self.assertIn("error", result)
        self.assertTrue(
            result["error"].startswith("An unexpected error occurred during the request:")
        )

    def test_register_tool(self):
        """Tests that the radiation tools are correctly registered."""
        mock_mcp = MagicMock()
        register(mock_mcp)

        # Verify that mcp.tool was called for each tool function
        self.assertEqual(mock_mcp.tool.call_count, 2)

        # Get the decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_mcp.tool.return_value.call_args_list
        }

        # Test get_weather_radiation_report
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.radiation._get_weather_radiation_report"
        ) as mock_get_weather_radiation_report:
            decorated_funcs["get_weather_radiation_report"](
                date="20250629", station="HKO"
            )
            mock_get_weather_radiation_report.assert_called_once_with(
                date="20250629", station="HKO", lang="en"
            )

        # Test get_radiation_station_codes
        with patch(
            "hkopenai.hk_climate_mcp_server.tools.radiation._get_radiation_station_codes"
        ) as mock_get_radiation_station_codes:
            decorated_funcs["get_radiation_station_codes"](lang="en")
            mock_get_radiation_station_codes.assert_called_once_with(lang="en")


if __name__ == "__main__":
    unittest.main()
