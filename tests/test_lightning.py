import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_climate_mcp_server.tools.lightning import get_lightning_data


class TestLightningTools(unittest.TestCase):
    @patch("requests.get")
    def test_get_lightning_data(self, mock_get):
        example_json = {
            "fields": ["Date time", "Cloud-to-ground count", "Cloud-to-cloud count"],
            "data": [["202506231300", "5", "10"], ["202506231310", "3", "8"]],
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


if __name__ == "__main__":
    unittest.main()
