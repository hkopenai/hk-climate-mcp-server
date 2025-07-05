"""
Module for testing MCP client simulation with hk-climate-mcp-server.

This module contains a comprehensive test suite for simulating client interactions
with the MCP server to ensure that various weather data tools function correctly.
Tests are skipped unless the environment variable RUN_MCP_CLIENT_TESTS is set to 'true'.
"""

import unittest
import subprocess
import json
import sys
import os
import time
import asyncio
import socket
import logging
from datetime import datetime, timedelta
from mcp.client.streamable_http import streamablehttp_client  # Added for MCP SDK communication
from mcp import ClientSession

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level),
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                     "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
class TestMCPClientSimulation(unittest.TestCase):
    """Test class for MCP client simulation with hk-climate-mcp-server."""
    
    server_process = None
    SERVER_URL = "http://127.0.0.1:8000/mcp/"  # Updated server URL for MCP API

    # Need a fresh mcp server to avoid lock up
    def setUp(self):
        """Set up the test environment by starting the MCP server subprocess."""
        logger.debug("Starting MCP server subprocess for HTTP communication...")
        # Start the MCP server as a subprocess. It should expose an HTTP endpoint.
        self.server_process = subprocess.Popen(
            [sys.executable, "-m", "hkopenai.hk_climate_mcp_server", "--sse"],
            # No stdin/stdout/stderr pipes needed for HTTP communication,
            # but keep for server logs
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.debug("MCP server subprocess started. Giving it a moment to "
                     "start up and listen on HTTP...")
        # Give the server a moment to start up and listen on the port
        time.sleep(5)  # Increased sleep time for server to fully initialize HTTP server

        # Check if the server is actually listening on the port
        for _ in range(10):
            try:
                with socket.create_connection(("127.0.0.1", 8000), timeout=1):
                    logger.debug("Server is listening on port 8000.")
                    break
            except OSError as e:
                logger.debug("Waiting for server to start: %s", e)
                time.sleep(1)
        else:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            if self.server_process.poll() is None:
                self.server_process.kill()
            raise Exception("Server did not start listening on port 8000 in time.")

        logger.debug("Server setup complete.")

    def tearDown(self):
        """Tear down the test environment by terminating the MCP server subprocess."""
        # Terminate the server process
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            if self.server_process.poll() is None:
                logger.debug("Tear down complete.")
                self.server_process.kill()
            
            # Print any remaining stderr output from the server process
            if self.server_process.stdout:
                self.server_process.stdout.close()
            if self.server_process.stderr:
                stderr_output = self.server_process.stderr.read()
                if stderr_output:
                    logger.debug("Server stderr (remaining):\n%s", stderr_output)
                else:
                    logger.debug("Server stderr (remaining): (empty)")
                self.server_process.stderr.close()
            logger.info("Tear down complete.")

    async def _call_tool_and_assert(self, tool_name, params):
        """
        Call a specified tool with given parameters and assert the response.

        Args:
            tool_name (str): The name of the tool to call.
            params (dict): Parameters to pass to the tool.

        Returns:
            dict: The response data from the tool call.
        """
        async with streamablehttp_client(self.SERVER_URL) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                response = await session.call_tool(tool_name, params)
                logger.info("'%s' tool response: %s...", tool_name, str(response)[:500])

                json_text = "{}"
                if response.content:
                    content = response.content[0]
                    try:
                        json_text = getattr(content, 'text', "{}")
                    except AttributeError:
                        json_text = "{}"
                data = json.loads(json_text)
                self.assertIsInstance(data, dict, "Result should be a dictionary")
                self.assertNotIn("error", data, f"Result should not contain an error: {data}")
                return data

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_current_weather_tool(self):
        """Test the 'get_current_weather' tool functionality."""
        logger.debug("Testing 'get_current_weather' tool...")
        asyncio.run(self._call_tool_and_assert("get_current_weather", {}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_9_day_weather_forecast_tool(self):
        """Test the 'get_9_day_weather_forecast' tool functionality."""
        logger.debug("Testing 'get_9_day_weather_forecast' tool...")
        asyncio.run(self._call_tool_and_assert("get_9_day_weather_forecast",
                                              {"lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_local_weather_forecast_tool(self):
        """Test the 'get_local_weather_forecast' tool functionality."""
        logger.debug("Testing 'get_local_weather_forecast' tool...")
        asyncio.run(self._call_tool_and_assert("get_local_weather_forecast",
                                              {"lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_weather_warning_summary_tool(self):
        """Test the 'get_weather_warning_summary' tool functionality."""
        logger.debug("Testing 'get_weather_warning_summary' tool...")
        asyncio.run(self._call_tool_and_assert("get_weather_warning_summary",
                                              {"lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_weather_warning_info_tool(self):
        """Test the 'get_weather_warning_info' tool functionality."""
        logger.debug("Testing 'get_weather_warning_info' tool...")
        asyncio.run(self._call_tool_and_assert("get_weather_warning_info",
                                              {"lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_special_weather_tips_tool(self):
        """Test the 'get_special_weather_tips' tool functionality."""
        logger.debug("Testing 'get_special_weather_tips' tool...")
        asyncio.run(self._call_tool_and_assert("get_special_weather_tips",
                                              {"lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_visibility_data_tool(self):
        """Test the 'get_visibility_data' tool functionality."""
        logger.debug("Testing 'get_visibility_data' tool...")
        asyncio.run(self._call_tool_and_assert("get_visibility_data", {"lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_lightning_data_tool(self):
        """Test the 'get_lightning_data' tool functionality."""
        logger.debug("Testing 'get_lightning_data' tool...")
        asyncio.run(self._call_tool_and_assert("get_lightning_data", {"lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_moon_times_tool(self):
        """Test the 'get_moon_times' tool functionality."""
        logger.debug("Testing 'get_moon_times' tool...")
        current_year = datetime.now().year
        asyncio.run(self._call_tool_and_assert("get_moon_times",
                                              {"year": current_year, "lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_hourly_tides_tool(self):
        """Test the 'get_hourly_tides' tool functionality."""
        logger.debug("Testing 'get_hourly_tides' tool...")
        current_year = datetime.now().year
        asyncio.run(self._call_tool_and_assert("get_hourly_tides",
                                              {"station": "QUB", "year": current_year,
                                               "lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_high_low_tides_tool(self):
        """Test the 'get_high_low_tides' tool functionality."""
        logger.debug("Testing 'get_high_low_tides' tool...")
        current_year = datetime.now().year
        asyncio.run(self._call_tool_and_assert("get_high_low_tides",
                                              {"station": "QUB", "year": current_year,
                                               "lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_tide_station_codes_tool(self):
        """Test the 'get_tide_station_codes' tool functionality."""
        logger.debug("Testing 'get_tide_station_codes' tool...")
        asyncio.run(self._call_tool_and_assert("get_tide_station_codes", {"lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_sunrise_sunset_times_tool(self):
        """Test the 'get_sunrise_sunset_times' tool functionality."""
        logger.debug("Testing 'get_sunrise_sunset_times' tool...")
        current_year = datetime.now().year
        asyncio.run(self._call_tool_and_assert("get_sunrise_sunset_times",
                                              {"year": current_year, "lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_gregorian_lunar_calendar_tool(self):
        """Test the 'get_gregorian_lunar_calendar' tool functionality."""
        logger.debug("Testing 'get_gregorian_lunar_calendar' tool...")
        current_date = datetime.now()
        asyncio.run(self._call_tool_and_assert("get_gregorian_lunar_calendar",
                                              {"year": current_date.year,
                                               "month": current_date.month,
                                               "day": current_date.day, "lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_daily_mean_temperature_tool(self):
        """Test the 'get_daily_mean_temperature' tool functionality."""
        logger.debug("Testing 'get_daily_mean_temperature' tool...")
        asyncio.run(self._call_tool_and_assert("get_daily_mean_temperature",
                                              {"station": "HKO", "lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_daily_max_temperature_tool(self):
        """Test the 'get_daily_max_temperature' tool functionality."""
        logger.debug("Testing 'get_daily_max_temperature' tool...")
        asyncio.run(self._call_tool_and_assert("get_daily_max_temperature",
                                              {"station": "HKO", "lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_daily_min_temperature_tool(self):
        """Test the 'get_daily_min_temperature' tool functionality."""
        logger.debug("Testing 'get_daily_min_temperature' tool...")
        asyncio.run(self._call_tool_and_assert("get_daily_min_temperature",
                                              {"station": "HKO", "lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_weather_radiation_report_tool(self):
        """Test the 'get_weather_radiation_report' tool functionality."""
        logger.debug("Testing 'get_weather_radiation_report' tool...")
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        asyncio.run(self._call_tool_and_assert("get_weather_radiation_report",
                                              {"date": yesterday, "station": "HKO",
                                               "lang": "en"}))

    @unittest.skipUnless(os.environ.get('RUN_MCP_CLIENT_TESTS') == 'true',
                         "Set RUN_MCP_CLIENT_TESTS=true to run live tests")
    def test_get_radiation_station_codes_tool(self):
        """Test the 'get_radiation_station_codes' tool functionality."""
        logger.debug("Testing 'get_radiation_station_codes' tool...")
        asyncio.run(self._call_tool_and_assert("get_radiation_station_codes",
                                              {"lang": "en"}))

if __name__ == "__main__":
    unittest.main()
