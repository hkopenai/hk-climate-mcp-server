import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server import (
    get_current_weather,
    get_9_day_weather_forecast,
    get_local_weather_forecast,
    get_weather_warning_summary,
    get_weather_warning_info,
    get_special_weather_tips,
    get_visibility_data,
    get_lightning_data,
    get_moon_times,
    get_hourly_tides,
    get_high_low_tides
)

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
        result = get_current_weather(lang="en")
        self.assertEqual(result['weatherObservation']['temperature']['value'], 29)
        self.assertEqual(result['weatherObservation']['temperature']['unit'], "C")
        self.assertEqual(result['weatherObservation']['temperature']['recordTime'], "2025-06-07T22:00:00+08:00")
        self.assertEqual(result['weatherObservation']['humidity']['value'], 79)
        self.assertEqual(result['weatherObservation']['humidity']['unit'], "percent")
        self.assertEqual(result['weatherObservation']['humidity']['recordTime'], "2025-06-07T22:00:00+08:00")
        self.assertEqual(result['weatherObservation']['rainfall']['value'], 0)
        self.assertEqual(result['weatherObservation']['rainfall']['startTime'], "2025-06-07T20:45:00+08:00")
        self.assertEqual(result['weatherObservation']['rainfall']['endTime'], "2025-06-07T21:45:00+08:00")
        self.assertEqual(result['generalSituation'], 'The Very Hot weather Warning is now in force. Prolonged heat alert! Please drink sufficient water. If feeling unwell, take rest or seek help immediately. If needed, seek medical advice as soon as possible.')
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"
        )

    @patch("requests.get")
    def test_get_current_weather_with_region(self, mock_get):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = self.default_mock_response
        mock_get.return_value = mock_response

        # Test
        result = get_current_weather("Cheung Chau", lang="en")
        self.assertEqual(result['weatherObservation']['temperature']['value'], 27)
        self.assertEqual(result['weatherObservation']['temperature']['unit'], "C")
        self.assertEqual(result['weatherObservation']['temperature']['recordTime'], "2025-06-07T22:00:00+08:00")
        self.assertEqual(result['weatherObservation']['humidity']['value'], 79)
        self.assertEqual(result['weatherObservation']['humidity']['unit'], "percent")
        self.assertEqual(result['weatherObservation']['humidity']['recordTime'], "2025-06-07T22:00:00+08:00")
        self.assertEqual(result['weatherObservation']['rainfall']['value'], 0)
        self.assertEqual(result['weatherObservation']['rainfall']['startTime'], "2025-06-07T20:45:00+08:00")
        self.assertEqual(result['weatherObservation']['rainfall']['endTime'], "2025-06-07T21:45:00+08:00")
        self.assertEqual(result['generalSituation'], 'The Very Hot weather Warning is now in force. Prolonged heat alert! Please drink sufficient water. If feeling unwell, take rest or seek help immediately. If needed, seek medical advice as soon as possible.')
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"
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

    @patch("requests.get")
    def test_get_local_weather_forecast(self, mock_get):
        example_json = {
            "generalSituation": "A southerly airstream is bringing showers to the coast of Guangdong and the northern part of the South China Sea. Locally, around 5 millimetres of rainfall were recorded over many places in the past couple of hours.",
            "forecastPeriod": "Weather forecast for today",
            "forecastDesc": "Mainly cloudy with a few showers. More showers with isolated thunderstorms at first. Hot with sunny periods during the day with a maximum temperature of around 32 degrees. Moderate southerly winds.",
            "outlook": "Mainly fine and very hot in the next couple of days. Showers will increase gradually in the middle and latter parts of next week.",
            "updateTime": "2025-06-21T07:45:00+08:00"
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_local_weather_forecast()
        self.assertEqual(result["forecastDesc"], example_json["forecastDesc"])
        self.assertEqual(result["outlook"], example_json["outlook"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        self.assertEqual(result["forecastPeriod"], example_json["forecastPeriod"])
        self.assertEqual(result["generalSituation"], example_json["generalSituation"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=flw&lang=en"
        )

    @patch("requests.get")
    def test_get_weather_warning_summary(self, mock_get):
        example_json = {
            "warningMessage": [
                "The Very Hot Weather Warning is in force.",
                "Thunderstorm Warning is in force."
            ],
            "updateTime": "2025-06-20T07:50:00+08:00"
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_weather_warning_summary()
        self.assertEqual(result["warningMessage"], example_json["warningMessage"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en"
        )

    @patch("requests.get")
    def test_get_weather_warning_info(self, mock_get):
        example_json = {
            "warningStatement": "The Thunderstorm Warning was issued at 7:50 a.m.",
            "updateTime": "2025-06-20T07:50:00+08:00"
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_weather_warning_info()
        self.assertEqual(result["warningStatement"], example_json["warningStatement"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang=en"
        )

    @patch("requests.get")
    def test_get_special_weather_tips(self, mock_get):
        example_json = {
            "specialWeatherTips": [
                "Hot weather may cause heat stroke. Avoid prolonged exposure to sunlight.",
                "Heavy rain may cause flooding in low-lying areas."
            ],
            "updateTime": "2025-06-20T07:50:00+08:00"
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_special_weather_tips()
        self.assertEqual(result["specialWeatherTips"], example_json["specialWeatherTips"])
        self.assertEqual(result["updateTime"], example_json["updateTime"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=swt&lang=en"
        )

    @patch("requests.get")
    def test_get_visibility_data(self, mock_get):
        example_json = {
            "fields": ["Date time", "Automatic Weather Station", "10 minute mean visibility"],
            "data": [
                ["202506231320", "Central", "35 km"],
                ["202506231320", "Chek Lap Kok", "50 km"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_visibility_data()
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LTMV&lang=en&rformat=json"
        )

    @patch("requests.get")
    def test_get_lightning_data(self, mock_get):
        example_json = {
            "fields": ["DateTime", "Type", "Region", "lightning count"],
            "data": [
                ["202506231200-202506231259", "Cloud-to-ground", "New Territories West", "0"],
                ["202506231200-202506231259", "Cloud-to-ground", "Hong Kong Island and Kowloon", "0"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_lightning_data()
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php?dataType=LHL&lang=en&rformat=json"
        )

    @patch("requests.get")
    def test_get_moon_times(self, mock_get):
        example_json = {
            "fields": ["Date", "Moonrise", "Moon transit", "Moonset"],
            "data": [
                ["2025-06-23", "05:30", "12:45", "20:00"],
                ["2025-06-24", "06:15", "13:30", "21:15"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_moon_times(year=2025, month=6)
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                'dataType': 'MRS',
                'lang': 'en',
                'rformat': 'json',
                'year': 2025,
                'month': 6
            }
        )

    @patch("requests.get")
    def test_get_hourly_tides(self, mock_get):
        example_json = {
            "fields": ["Date time", "Station", "Height"],
            "data": [
                ["2025-06-23 01:00", "CCH", "1.2"],
                ["2025-06-23 02:00", "CCH", "1.5"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_hourly_tides(station="CCH", year=2025, month=6)
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                'dataType': 'HHOT',
                'lang': 'en',
                'rformat': 'json',
                'station': 'CCH',
                'year': 2025,
                'month': 6
            }
        )

    @patch("requests.get")
    def test_get_high_low_tides(self, mock_get):
        example_json = {
            "fields": ["Date time", "Station", "Type", "Height"],
            "data": [
                ["2025-06-23 06:30", "CCH", "High", "2.1"],
                ["2025-06-23 12:45", "CCH", "Low", "0.8"]
            ]
        }
        mock_response = MagicMock()
        mock_response.json.return_value = example_json
        mock_get.return_value = mock_response

        result = get_high_low_tides(station="CCH", year=2025, month=6)
        self.assertEqual(result["fields"], example_json["fields"])
        self.assertEqual(result["data"], example_json["data"])
        mock_get.assert_called_once_with(
            "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php",
            params={
                'dataType': 'HLT',
                'lang': 'en',
                'rformat': 'json',
                'station': 'CCH',
                'year': 2025,
                'month': 6
            }
        )

if __name__ == "__main__":
    unittest.main()
