# IMPORTANT: This test file must run sequentially and not in parallel to avoid conflicts with the MCP server subprocess.
import unittest
import subprocess
import json
import sys
import os
import time
import asyncio
import socket
import logging

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level),
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from mcp.client.streamable_http import streamablehttp_client # Added for MCP SDK communication
from mcp import ClientSession


class TestMCPClientSimulation(unittest.TestCase):
    server_process = None
    SERVER_URL = "http://127.0.0.1:8000/mcp/" # Updated server URL for MCP API

    @classmethod
    def setUpClass(cls):
        logger.debug("Starting MCP server subprocess for HTTP communication...")
        # Start the MCP server as a subprocess. It should expose an HTTP endpoint.
        cls.server_process = subprocess.Popen(
            [sys.executable, "-m", "hkopenai.hk_climate_mcp_server", "--sse"],
            # No stdin/stdout/stderr pipes needed for HTTP communication, but keep for server logs
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.debug("MCP server subprocess started. Giving it a moment to start up and listen on HTTP...")
        # Give the server a moment to start up and listen on the port
        time.sleep(5) # Increased sleep time for server to fully initialize HTTP server

        # Check if the server is actually listening on the port
        for _ in range(10):
            try:
                with socket.create_connection(("127.0.0.1", 8000), timeout=1):
                    logger.debug("Server is listening on port 8000.")
                    break
            except OSError as e:
                logger.debug(f"Waiting for server to start: {e}")
                time.sleep(1)
        else:
            self.fail("Server did not start listening on port 8000 in time.")

        logger.debug(f"Server setup complete.")

    @classmethod
    def tearDownClass(cls):
        # Terminate the server process
        if cls.server_process:
            logger.debug("Tear down complete.")
            cls.server_process.terminate()
            cls.server_process.wait(timeout=5)
            if cls.server_process.poll() is None:
                logger.debug("Tear down complete.")
                cls.server_process.kill()
            
            # Print any remaining stderr output from the server process
            if cls.server_process.stderr:
                stderr_output = cls.server_process.stderr.read()
                if stderr_output:
                    logger.debug(f"Server stderr (remaining):\n{stderr_output}")
                else:
                    logger.debug("Server stderr (remaining): (empty)")
            logger.debug("Tear down complete.")

    def test_get_current_weather_tool(self):
        logger.debug("Testing 'get_current_weather' tool...")
        try:
            async def _run_test():
                async with streamablehttp_client(self.SERVER_URL) as (read_stream, write_stream, _):
                    async with ClientSession(read_stream, write_stream) as session:
                        await session.initialize()
                        # Call the 'get_current_weather' tool
                        response = await session.call_tool("get_current_weather", {})
                        logger.info(f"'get_current_weather' tool response: {response}")

                        # Extract the JSON text from the response content
                        json_text = response.content[0].text if response.content else "{}"
                        data = json.loads(json_text)

                        # Assert that the response contains expected keys
                        self.assertIn("generalSituation", data)
                        self.assertIn("updateTime", data)
                        self.assertIn("icon", data)

                        # Further assert on nested structure
                        self.assertIn("weatherObservation", data)
                        self.assertIn("temperature", data["weatherObservation"])
                        self.assertIn("place", data["weatherObservation"]["temperature"])
                        self.assertIn("value", data["weatherObservation"]["temperature"])
                        self.assertIn("unit", data["weatherObservation"]["temperature"])

                        logger.debug("'get_current_weather' tool test passed.")
            asyncio.run(_run_test())
        except Exception as e:
            self.fail(f"'get_current_weather' tool test failed: {e}")

if __name__ == "__main__":
    unittest.main()
