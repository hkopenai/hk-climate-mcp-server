import unittest
from unittest.mock import patch, MagicMock
from hko_tools import get_current_weather


class TestHKOTools(unittest.TestCase):
    # @patch("hko_tools.requests.get")
    # def test_get_weather_warning(self, mock_get):
    #     # Setup mock response
    #     mock_response = MagicMock()
    #     mock_response.json.return_value = {
    #         "WHOT": {
    #             "name": "Very Hot Weather Warning",
    #             "code": "WHOT",
    #             "actionCode": "REISSUE",
    #             "issueTime": "2025-06-07T12:15:00+08:00",
    #             "updateTime": "2025-06-07T16:20:00+08:00",
    #         }
    #     }
    #     mock_get.return_value = mock_response

    #     # Test
    #     result = HKOTools.get_weather_warning()
    #     self.assertEqual(result, {"warningStatement": "No warning in force"})
    #     mock_get.assert_called_once_with(
    #         "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum"
    #     )

    # @patch("hko_tools.requests.get")
    # def test_get_9day_forecast(self, mock_get):
    #     # Setup mock response
    #     mock_response = MagicMock()
    #     mock_response.json.return_value = {
    #         "generalSituation": "Under the influence of an anticyclone aloft, the weather will be mainly fine over southern China in the next couple of days. It will be very hot during the day. Meanwhile, a broad trough of low pressure will bring unsettled weather to the central part of the South China Sea to the seas east of the Philippines. An area of low pressure may develop near Luzon within the broad trough of low pressure early to midweek next week, and move in the general direction of the seas east of Taiwan to the vicinity of the coast of southeastern China in the middle and latter parts of next week. Its chance of development over the South China Sea still cannot be ruled out, but remains rather uncertain.",
    #         "weatherForecast": [
    #             {
    #                 "forecastDate": "20250608",
    #                 "week": "Sunday",
    #                 "forecastWind": "South force 2 to 3.",
    #                 "forecastWeather": "Mainly fine. Very hot during the day.",
    #                 "forecastMaxtemp": {"value": 33, "unit": "C"},
    #                 "forecastMintemp": {"value": 28, "unit": "C"},
    #                 "forecastMaxrh": {"value": 90, "unit": "percent"},
    #                 "forecastMinrh": {"value": 60, "unit": "percent"},
    #                 "ForecastIcon": 90,
    #                 "PSR": "Low",
    #             },
    #             {
    #                 "forecastDate": "20250609",
    #                 "week": "Monday",
    #                 "forecastWind": "South to southeast force 3.",
    #                 "forecastWeather": "Mainly fine. Very hot with isolated showers during the day.",
    #                 "forecastMaxtemp": {"value": 33, "unit": "C"},
    #                 "forecastMintemp": {"value": 28, "unit": "C"},
    #                 "forecastMaxrh": {"value": 90, "unit": "percent"},
    #                 "forecastMinrh": {"value": 60, "unit": "percent"},
    #                 "ForecastIcon": 90,
    #                 "PSR": "Low",
    #             },
    #             {
    #                 "forecastDate": "20250610",
    #                 "week": "Tuesday",
    #                 "forecastWind": "East to southeast force 2 to 3.",
    #                 "forecastWeather": "Mainly fine. Very hot during the day. Isolated showers later.",
    #                 "forecastMaxtemp": {"value": 33, "unit": "C"},
    #                 "forecastMintemp": {"value": 28, "unit": "C"},
    #                 "forecastMaxrh": {"value": 90, "unit": "percent"},
    #                 "forecastMinrh": {"value": 60, "unit": "percent"},
    #                 "ForecastIcon": 90,
    #                 "PSR": "Low",
    #             },
    #             {
    #                 "forecastDate": "20250611",
    #                 "week": "Wednesday",
    #                 "forecastWind": "East to northeast force 4.",
    #                 "forecastWeather": "Sunny periods and one or two showers. Hot during the day.",
    #                 "forecastMaxtemp": {"value": 32, "unit": "C"},
    #                 "forecastMintemp": {"value": 27, "unit": "C"},
    #                 "forecastMaxrh": {"value": 90, "unit": "percent"},
    #                 "forecastMinrh": {"value": 65, "unit": "percent"},
    #                 "ForecastIcon": 53,
    #                 "PSR": "Low",
    #             },
    #             {
    #                 "forecastDate": "20250612",
    #                 "week": "Thursday",
    #                 "forecastWind": "East to northeast force 4, occasionally force 5.",
    #                 "forecastWeather": "Sunny intervals and a few showers. Isolated thunderstorms later.",
    #                 "forecastMaxtemp": {"value": 31, "unit": "C"},
    #                 "forecastMintemp": {"value": 27, "unit": "C"},
    #                 "forecastMaxrh": {"value": 95, "unit": "percent"},
    #                 "forecastMinrh": {"value": 75, "unit": "percent"},
    #                 "ForecastIcon": 54,
    #                 "PSR": "Medium Low",
    #             },
    #             {
    #                 "forecastDate": "20250613",
    #                 "week": "Friday",
    #                 "forecastWind": "East force 4 to 5.",
    #                 "forecastWeather": "Mainly cloudy with a few showers and isolated thunderstorms.",
    #                 "forecastMaxtemp": {"value": 29, "unit": "C"},
    #                 "forecastMintemp": {"value": 26, "unit": "C"},
    #                 "forecastMaxrh": {"value": 95, "unit": "percent"},
    #                 "forecastMinrh": {"value": 75, "unit": "percent"},
    #                 "ForecastIcon": 62,
    #                 "PSR": "Medium",
    #             },
    #             {
    #                 "forecastDate": "20250614",
    #                 "week": "Saturday",
    #                 "forecastWind": "South to southeast force 4 to 5.",
    #                 "forecastWeather": "Mainly cloudy with a few showers and isolated thunderstorms.",
    #                 "forecastMaxtemp": {"value": 30, "unit": "C"},
    #                 "forecastMintemp": {"value": 27, "unit": "C"},
    #                 "forecastMaxrh": {"value": 95, "unit": "percent"},
    #                 "forecastMinrh": {"value": 75, "unit": "percent"},
    #                 "ForecastIcon": 62,
    #                 "PSR": "Medium",
    #             },
    #             {
    #                 "forecastDate": "20250615",
    #                 "week": "Sunday",
    #                 "forecastWind": "South to southwest force 3 to 4.",
    #                 "forecastWeather": "Mainly cloudy with a few showers. Sunny intervals during the day.",
    #                 "forecastMaxtemp": {"value": 31, "unit": "C"},
    #                 "forecastMintemp": {"value": 27, "unit": "C"},
    #                 "forecastMaxrh": {"value": 95, "unit": "percent"},
    #                 "forecastMinrh": {"value": 70, "unit": "percent"},
    #                 "ForecastIcon": 54,
    #                 "PSR": "Medium Low",
    #             },
    #             {
    #                 "forecastDate": "20250616",
    #                 "week": "Monday",
    #                 "forecastWind": "South to southwest force 3 to 4.",
    #                 "forecastWeather": "Mainly cloudy with a few showers. Sunny intervals during the day.",
    #                 "forecastMaxtemp": {"value": 31, "unit": "C"},
    #                 "forecastMintemp": {"value": 27, "unit": "C"},
    #                 "forecastMaxrh": {"value": 95, "unit": "percent"},
    #                 "forecastMinrh": {"value": 70, "unit": "percent"},
    #                 "ForecastIcon": 54,
    #                 "PSR": "Medium Low",
    #             },
    #         ],
    #         "updateTime": "2025-06-07T16:30:00+08:00",
    #         "seaTemp": {
    #             "place": "North Point",
    #             "value": 27,
    #             "unit": "C",
    #             "recordTime": "2025-06-07T14:00:00+08:00",
    #         },
    #         "soilTemp": [
    #             {
    #                 "place": "Hong Kong Observatory",
    #                 "value": 28,
    #                 "unit": "C",
    #                 "recordTime": "2025-06-07T07:00:00+08:00",
    #                 "depth": {"unit": "metre", "value": 0.5},
    #             },
    #             {
    #                 "place": "Hong Kong Observatory",
    #                 "value": 27.6,
    #                 "unit": "C",
    #                 "recordTime": "2025-06-07T07:00:00+08:00",
    #                 "depth": {"unit": "metre", "value": 1},
    #             },
    #         ],
    #     }
    #     mock_get.return_value = mock_response

    #     # Test
    #     result = HKOTools.get_9day_forecast()
    #     self.assertEqual(
    #         result,
    #         {
    #             "weatherForecast": [
    #                 {"forecastDate": "2025-06-08", "forecastWeather": "Sunny"}
    #             ]
    #         },
    #     )
    #     mock_get.assert_called_once_with(
    #         "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd"
    #     )

    @patch("hko_tools.requests.get")
    def test_get_current_weather(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
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
                "The Very Hot Weather Warning is now in force. Prolonged heat alert! Please drink sufficient water. If feeling unwell, take rest or seek help immediately. If needed, seek medical advice as soon as possible."
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
        self.assertEqual(result['warning'], 'The Very Hot Weather Warning is now in force. Prolonged heat alert! Please drink sufficient water. If feeling unwell, take rest or seek help immediately. If needed, seek medical advice as soon as possible.')    
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread"
        )


if __name__ == "__main__":
    unittest.main()
