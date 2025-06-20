import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server import get_current_weather
from hkopenai.hk_climate_mcp_server import get_9_day_weather_forecast

class TestWeatherTools(unittest.TestCase):
    default_mock_response = {
            "rainfall": {
                "data": [
                    {
                        "unit": "mm",
                        "place": "Central & Western District",
                        "max": 0,
                        "main": "FALSE",
                    },
                    {
                        "unit": "mm",
                        "place": "Eastern District",
                        "max": 0,
                        "main": "FALSE",
                    },
                    {"unit": "mm", "place": "Kwai Tsing", "max": 0, "main": "FALSE"},
                    {
                        "unit": "mm",
                        "place": "Islands District",
                        "max": 0,
                        "main": "FALSE",
                    },
                    {
                        "unit": "mm",
                        "place": "North District",
                        "max": 0,
                        "main": "FALSE",
                    },
                    {"unit": "mm", "place": "Sai Kung", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Sha Tin", "max": 0, "main": "FALSE"},
                    {
                        "unit": "mm",
                        "place": "Southern District",
                        "max": 0,
                        "main": "FALSE",
                    },
                    {"unit": "mm", "place": "Tai Po", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Tsuen Wan", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Tuen Mun", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Wan Chai", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Yuen Long", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Yau Tsim Mong", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Sham Shui Po", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Kowloon City", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Wong Tai Sin", "max": 0, "main": "FALSE"},
                    {"unit": "mm", "place": "Kwun Tong", "max": 0, "main": "FALSE"},
                ],
                "startTime": "2025-06-07T20:45:00+08:00",
                "endTime": "2025-06-07T21:45:00+08:00",
            },
            "icon": [72],
            "iconUpdateTime": "2025-06-07T18:00:00+08:00",
            "uvindex": "",
            "updateTime": "2025-06-07T22:02:00+08:00",
            "temperature": {
                "data": [
                    {"place": "King's Park", "value": 28, "unit": "C"},
                    {"place": "Hong Kong Observatory", "value": 29, "unit": "C"},
                    {"place": "Wong Chuk Hang", "value": 28, "unit": "C"},
                    {"place": "Ta Kwu Ling", "value": 28, "unit": "C"},
                    {"place": "Lau Fau Shan", "value": 28, "unit": "C"},
                    {"place": "Tai Po", "value": 29, "unit": "C"},
                    {"place": "Sha Tin", "value": 29, "unit": "C"},
                    {"place": "Tuen Mun", "value": 29, "unit": "C"},
                    {"place": "Tseung Kwan O", "value": 27, "unit": "C"},
                    {"place": "Sai Kung", "value": 28, "unit": "C"},
                    {"place": "Cheung Chau", "value": 27, "unit": "C"},
                    {"place": "Chek Lap Kok", "value": 29, "unit": "C"},
                    {"place": "Tsing Yi", "value": 28, "unit": "C"},
                    {"place": "Shek Kong", "value": 29, "unit": "C"},
                    {"place": "Tsuen Wan Ho Koon", "value": 27, "unit": "C"},
                    {"place": "Tsuen Wan Shing Mun Valley", "value": 28, "unit": "C"},
                    {"place": "Hong Kong Park", "value": 28, "unit": "C"},
                    {"place": "Shau Kei Wan", "value": 28, "unit": "C"},
                    {"place": "Kowloon City", "value": 29, "unit": "C"},
                    {"place": "Happy Valley", "value": 29, "unit": "C"},
                    {"place": "Wong Tai Sin", "value": 29, "unit": "C"},
                    {"place": "Stanley", "value": 28, "unit": "C"},
                    {"place": "Kwun Tong", "value": 28, "unit": "C"},
                    {"place": "Sham Shui Po", "value": 29, "unit": "C"},
                    {"place": "Kai Tak Runway Park", "value": 29, "unit": "C"},
                    {"place": "Yuen Long Park", "value": 28, "unit": "C"},
                    {"place": "Tai Mei Tuk", "value": 28, "unit": "C"},
                ],
                "recordTime": "2025-06-07T22:00:00+08:00",
            },
            "warningMessage": [
                "The Very Hot weather Warning is now in force. Prolonged heat alert! Please drink sufficient water. If feeling unwell, take rest or seek help immediately. If needed, seek medical advice as soon as possible."
            ],
            "mintempFrom00To09": "",
            "rainfallFrom00To12": "",
            "rainfallLastMonth": "",
            "rainfallJanuaryToLastMonth": "",
            "tcmessage": "",
            "humidity": {
                "recordTime": "2025-06-07T22:00:00+08:00",
                "data": [
                    {"unit": "percent", "value": 79, "place": "Hong Kong Observatory"}
                ],
            },
        }

    @patch("requests.get")
    def test_get_current_weather(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = self.default_mock_response
        mock_get.return_value = mock_response

        # Test
        result = get_current_weather()
        self.assertEqual(result['temperature']['value'], 29)
        self.assertEqual(result['temperature']['unit'], "C")
        self.assertEqual(result['temperature']['recordTime'],  "2025-06-07T22:00:00+08:00",)
        self.assertEqual(result['humidity']['value'], 79)
        self.assertEqual(result['humidity']['unit'], "percent")
        self.assertEqual(result['humidity']['recordTime'],  "2025-06-07T22:00:00+08:00",)        
        self.assertEqual(result['rainfall']['value'], 0)
        self.assertEqual(result['rainfall']['startTime'], "2025-06-07T20:45:00+08:00")
        self.assertEqual(result['rainfall']['endTime'], "2025-06-07T21:45:00+08:00")          
        self.assertEqual(result['warning'], 'The Very Hot weather Warning is now in force. Prolonged heat alert! Please drink sufficient water. If feeling unwell, take rest or seek help immediately. If needed, seek medical advice as soon as possible.')    
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread"
        )

    @patch("requests.get")
    def test_get_current_weather_with_region(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = self.default_mock_response
        mock_get.return_value = mock_response

        # Test
        result = get_current_weather("Cheung Chau")
        self.assertEqual(result['temperature']['value'], 27)
        self.assertEqual(result['temperature']['unit'], "C")
        self.assertEqual(result['temperature']['recordTime'],  "2025-06-07T22:00:00+08:00",)
        self.assertEqual(result['humidity']['value'], 79)
        self.assertEqual(result['humidity']['unit'], "percent")
        self.assertEqual(result['humidity']['recordTime'],  "2025-06-07T22:00:00+08:00",)        
        self.assertEqual(result['rainfall']['value'], 0)
        self.assertEqual(result['rainfall']['startTime'], "2025-06-07T20:45:00+08:00")
        self.assertEqual(result['rainfall']['endTime'], "2025-06-07T21:45:00+08:00")          
        self.assertEqual(result['warning'], 'The Very Hot weather Warning is now in force. Prolonged heat alert! Please drink sufficient water. If feeling unwell, take rest or seek help immediately. If needed, seek medical advice as soon as possible.')    
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread"
        )

    @patch("requests.get")
    def test_get_9_day_weather_forecast(self, mock_get):
        example_json = {
            "generalSituation": "A southerly airstream...",
            "weatherForecast": [
                {
                    "forecastDate": "20250620",
                    "week": "Friday",
                    "forecastWind": "South force 3 to 4.",
                    "forecastWeather": "Mainly cloudy with occasional showers.",
                    "forecastMaxtemp": {"value": 31, "unit": "C"},
                    "forecastMintemp": {"value": 27, "unit": "C"},
                    "forecastMaxrh": {"value": 95, "unit": "percent"},
                    "forecastMinrh": {"value": 70, "unit": "percent"},
                    "ForecastIcon": 54,
                    "PSR": "Medium"
                }
            ],
            "updateTime": "2025-06-20T07:50:00+08:00",
            "seaTemp": {
                "place": "North Point",
                "value": 28,
                "unit": "C",
                "recordTime": "2025-06-20T07:00:00+08:00"
            },
            "soilTemp": [
                {
                    "place": "Hong Kong Observatory",
                    "value": 29.2,
                    "unit": "C",
                    "recordTime": "2025-06-20T07:00:00+08:00",
                    "depth": {"unit": "metre", "value": 0.5}
                }
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_9_day_weather_forecast()
        self.assertEqual(result["generalSituation"], example_json["generalSituation"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        self.assertEqual(result["seaTemp"], example_json["seaTemp"])
        self.assertEqual(result["soilTemp"], example_json["soilTemp"])
        self.assertIsInstance(result["weatherForecast"], list)
        self.assertEqual(result["weatherForecast"][0]["forecastDate"], "20250620")
        self.assertEqual(result["weatherForecast"][0]["week"], "Friday")
        self.assertEqual(result["weatherForecast"][0]["forecastWind"], "South force 3 to 4.")
        self.assertEqual(result["weatherForecast"][0]["forecastWeather"], "Mainly cloudy with occasional showers.")

if __name__ == "__main__":
    unittest.main()
