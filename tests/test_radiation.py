import unittest
import requests
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.radiation import get_weather_radiation_report


class TestRadiationTools(unittest.TestCase):
    EXAMPLE_JSON = {
        "ChekLapKokLocationName": "Chek Lap Kok",
        "ChekLapKokMaxTemp": "32.7",
        "ChekLapKokMicrosieverts": "0.15",
        "ChekLapKokMinTemp": "28.2",
        "BulletinTime": "0015",
        "BulletinDate": "20250624",
        "ReportTimeInfoDate": "20250623",
        "HongKongDesc": "Average ambient gamma radiation dose rate taken outdoors in Hong Kong ranged from 0.08 to 0.15 microsievert per hour.  These are within the normal range of fluctuation of the background radiation level in Hong Kong.",
        "NoteDesc": "From readings taken at various locations in Hong Kong in the past, the hourly mean ambient gamma radiation dose rate may vary between 0.06 and 0.3 microsievert per hour. (1 microsievert = 0.000001 sievert = 0.001 millisievert)",
        "NoteDesc1": "Temporal variations are generally caused by changes in meteorological conditions such as rainfall, wind and barometric pressure.",
        "NoteDesc2": "Spatial variations are generally caused by differences in the radioactive content of local rock and soil.",
        "NoteDesc3": "The data displayed is provisional. Only limited data validation has been carried out.",
    }

    @patch("requests.get")
    def test_get_weather_radiation_report(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = self.EXAMPLE_JSON
        mock_get.return_value = mock_response

        result = get_weather_radiation_report(date="20250623", station="HKO")
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={"dataType": "RYES", "lang": "en", 'rformat': 'json', "date": "20250623", "station": "HKO"},
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn("ChekLapKokLocationName", result, "Result should contain expected keys")

    def test_get_weather_radiation_report_missing_station(self):
        result = get_weather_radiation_report(date="20250623", station="")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn("error", result, "Result should contain error message for missing station")

    def test_get_weather_radiation_report_invalid_station(self):
        result = get_weather_radiation_report(date="20250623", station="INVALID")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn("error", result, "Result should contain error message for invalid station")

    def test_get_weather_radiation_report_missing_date(self):
        result = get_weather_radiation_report(date="", station="HKO")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn("error", result, "Result should contain error message for missing date")

    def test_get_weather_radiation_report_invalid_date_format(self):
        result = get_weather_radiation_report(date="2025-06-23", station="HKO")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn("error", result, "Result should contain error message for invalid date format")

    @patch("hkopenai.hk_climate_mcp_server.tools.radiation.is_date_in_future")
    @patch("requests.get")
    def test_get_weather_radiation_report_yesterday_valid(self, mock_get, mock_date_check):
        mock_date_check.return_value = False
        mock_response = MagicMock()
        mock_response.json.return_value = self.EXAMPLE_JSON
        mock_get.return_value = mock_response

        result = get_weather_radiation_report(date="20250623", station="HKO")
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={"dataType": "RYES", "lang": "en", 'rformat': 'json', "date": "20250623", "station": "HKO"},
        )
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertNotIn("error", result, "Result should not contain error for yesterday's date")
        self.assertIn("ChekLapKokLocationName", result, "Result should contain expected keys")

    @patch("hkopenai.hk_climate_mcp_server.tools.radiation.is_date_in_future")
    def test_get_weather_radiation_report_date_in_future(self, mock_date_check):
        mock_date_check.return_value = True
        result = get_weather_radiation_report(date="20250625", station="HKO")
        self.assertIsInstance(result, dict, "Result should be a dictionary")
        self.assertIn("error", result, "Result should contain error message for date being in the future")
        self.assertIn("Date must be yesterday or before", result["error"], "Error message should mention date must be yesterday or before")

    @patch('requests.get')
    def test_get_weather_radiation_report_non_json_response(self, mock_get):
        """Test error handling for non-JSON response."""
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result = get_weather_radiation_report(date="20230618", station="HKO")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Failed to parse JSON. Invalid params or data not updated. Try again.")

    @patch('requests.get')
    def test_get_weather_radiation_report_request_exception(self, mock_get):
        """Test error handling for request exceptions."""
        mock_get.side_effect = requests.RequestException("Network error")

        result = get_weather_radiation_report(date="20230618", station="HKO")
        self.assertIn("error", result)
        self.assertTrue(result["error"].startswith("Failed to fetch data: Network error"))

if __name__ == "__main__":
    unittest.main()
