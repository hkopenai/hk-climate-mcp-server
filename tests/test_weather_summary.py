"""
Unit tests for the aggregated weather summary tool.

Mirrors the conventions in test_current_weather.py and test_forecast.py:
unittest.TestCase, @patch the underlying per-section helpers (not the
HTTP layer), and assert on the consolidated structure returned by
get_weather_summary.
"""

import asyncio
import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from hkopenai.hk_climate_mcp_server.tools.weather_summary import (
    _aggregate,
    register,
)


class TestWeatherSummaryTool(unittest.TestCase):
    """Test case class for the aggregated weather summary tool."""

    def test_register_tool(self):
        """Tests that the aggregator tool is correctly registered on a FastMCP mock."""
        mock_mcp = MagicMock()
        register(mock_mcp)
        self.assertEqual(mock_mcp.tool.call_count, 1)
        decorated_func = mock_mcp.tool.return_value.call_args[0][0]
        self.assertEqual(decorated_func.__name__, "get_weather_summary")

    def test_aggregate_returns_all_sections(self):
        """All configured sections appear in the response, even if some failed."""
        # Arrange: every per-section helper returns a tiny valid payload,
        # except one which raises an exception. Each side_effect accepts
        # the same positional/keyword signature as the underlying helper.
        def ok_current(region, lang):
            return {"weatherObservation": {"temperature": {"value": 30, "unit": "C"}}}

        def ok_local(lang):
            return {"forecastDesc": "Sunny."}

        def ok_nine_day(lang):
            return {"weatherForecast": [{"forecastDate": "20261002"}]}

        def ok_warnings(lang):
            return {"warningMessage": ["Thunderstorm Warning."]}

        def ok_warning_info(lang):
            return {"warningStatement": "Details..."}

        def ok_tides(station, year, month, day, lang):
            return {"fields": ["hour", "height"], "data": [[0, 1.2]]}

        def boom_warnings(lang):
            raise RuntimeError("upstream timeout")

        with patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.current_weather._get_current_weather",
            side_effect=ok_current,
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.forecast._get_local_weather_forecast",
            side_effect=ok_local,
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.forecast._get_9_day_weather_forecast",
            side_effect=ok_nine_day,
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.warnings._get_weather_warning_summary",
            side_effect=boom_warnings,
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.warnings._get_weather_warning_info",
            side_effect=ok_warning_info,
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.tides._get_hourly_tides",
            side_effect=ok_tides,
        ):
            # Act
            payload = asyncio.run(_aggregate("en"))

        # Assert: every section is present
        for key in (
            "current",
            "local_forecast",
            "nine_day",
            "warnings",
            "warning_info",
            "tides",
            "_meta",
        ):
            self.assertIn(key, payload, f"missing section {key!r}")

        # The failing section surfaces an error key instead of crashing
        self.assertIn("error", payload["warnings"])
        self.assertIn("RuntimeError", payload["warnings"]["error"])

        # The healthy sections carry the mocked payload
        self.assertEqual(payload["current"]["weatherObservation"]["temperature"]["value"], 30)
        self.assertEqual(payload["local_forecast"]["forecastDesc"], "Sunny.")
        self.assertEqual(payload["nine_day"]["weatherForecast"][0]["forecastDate"], "20261002")
        self.assertEqual(payload["warning_info"]["warningStatement"], "Details...")
        self.assertEqual(payload["tides"]["data"][0][1], 1.2)

        # Meta is well-formed
        meta = payload["_meta"]
        self.assertEqual(meta["lang"], "en")
        self.assertEqual(
            meta["sections"],
            [
                "current",
                "local_forecast",
                "nine_day",
                "warnings",
                "warning_info",
                "tides",
            ],
        )
        self.assertEqual(meta["generated_at"], date.today().isoformat())

    def test_aggregate_passes_lang_to_sections(self):
        """The lang arg flows through to every per-section helper."""
        captured_kwargs: list[dict] = []

        def capture_current(*args, **kwargs):
            captured_kwargs.append(("current", kwargs))
            return {}

        def capture_tides(*args, **kwargs):
            captured_kwargs.append(("tides", kwargs))
            return {}

        with patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.current_weather._get_current_weather",
            side_effect=capture_current,
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.forecast._get_local_weather_forecast",
            return_value={},
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.forecast._get_9_day_weather_forecast",
            return_value={},
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.warnings._get_weather_warning_summary",
            return_value={},
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.warnings._get_weather_warning_info",
            return_value={},
        ), patch(
            "hkopenai.hk_climate_mcp_server.tools.weather_summary.tides._get_hourly_tides",
            side_effect=capture_tides,
        ):
            asyncio.run(_aggregate("tc"))

        by_name = dict(captured_kwargs)
        self.assertEqual(by_name["current"]["lang"], "tc")
        self.assertEqual(by_name["tides"]["lang"], "tc")
        self.assertEqual(by_name["tides"]["station"], "QUB")


if __name__ == "__main__":
    unittest.main()
