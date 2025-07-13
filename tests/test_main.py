import unittest
from unittest.mock import patch, MagicMock
import os
from hkopenai.hk_climate_mcp_server.__main__ import cli_main

class TestMain(unittest.TestCase):
    """
    Test class for verifying __main__.py's handling of command-line arguments
    and environment variables.
    """

    def setUp(self):
        # Store original os.environ and clear it for each test to ensure isolation
        self._original_environ = os.environ.copy()
        os.environ.clear()

    def tearDown(self):
        # Restore original os.environ after each test
        os.environ.clear()
        os.environ.update(self._original_environ)

    @patch('argparse.ArgumentParser')
    @patch('hkopenai.hk_climate_mcp_server.__main__.main')
    def test_default_behavior(self, mock_main, mock_arg_parser):
        """
        Test that the server runs with default host and port when no
        command-line arguments or environment variables are provided.
        """
        # Configure mocks for argparse
        mock_args = MagicMock(sse=False, port=8000, host='127.0.0.1')
        mock_parser_instance = MagicMock()
        mock_parser_instance.parse_args.return_value = mock_args
        mock_parser_instance.get_default.side_effect = lambda arg: {
            'host': '127.0.0.1',
            'port': 8000
        }.get(arg)
        mock_arg_parser.return_value = mock_parser_instance

        # Ensure no relevant environment variables are set
        with patch.dict(os.environ, {}, clear=True):
            # Run the main function
            with patch('sys.argv', ['__main__.py']):
                cli_main()

        # Assertions
        mock_main.assert_called_once_with(host='127.0.0.1', port=8000, sse=False)
        mock_parser_instance.parse_args.assert_called_once()
        mock_parser_instance.get_default.assert_any_call('host')
        mock_parser_instance.get_default.assert_any_call('port')

    @patch('argparse.ArgumentParser')
    @patch('hkopenai.hk_climate_mcp_server.__main__.main')
    def test_command_line_arguments(self, mock_main, mock_arg_parser):
        """
        Test that command-line arguments override default values and environment variables.
        """
        # Set environment variables that should be overridden
        with patch.dict(os.environ, {'TRANSPORT_MODE': 'stdio', 'HOST': '0.0.0.0', 'PORT': '9000'}):
            # Configure mocks for argparse
            mock_args = MagicMock(sse=True, port=8080, host='192.168.1.1')
            mock_parser_instance = MagicMock()
            mock_parser_instance.parse_args.return_value = mock_args
            mock_parser_instance.get_default.side_effect = lambda arg: {
                'host': '127.0.0.1',
                'port': 8000
            }.get(arg)
            mock_arg_parser.return_value = mock_parser_instance

            # Run the main function
            with patch('sys.argv', ['__main__.py', '-s', '-p', '8080', '--host', '192.168.1.1']):
                cli_main()

            # Assertions
            mock_main.assert_called_once_with(host='192.168.1.1', port=8080, sse=True)
            mock_parser_instance.parse_args.assert_called_once()
            mock_parser_instance.get_default.assert_any_call('host')
            mock_parser_instance.get_default.assert_any_call('port')

    @patch('argparse.ArgumentParser')
    @patch('hkopenai.hk_climate_mcp_server.__main__.main')
    def test_environment_variables(self, mock_main, mock_arg_parser):
        """
        Test that environment variables override default values when no
        command-line arguments are provided.
        """
        # Set environment variables
        with patch.dict(os.environ, {'TRANSPORT_MODE': 'sse', 'HOST': '0.0.0.0', 'PORT': '9000'}):
            # Configure mocks for argparse
            mock_args = MagicMock(sse=False, port=8000, host='127.0.0.1') # Default args from argparse
            mock_parser_instance = MagicMock()
            mock_parser_instance.parse_args.return_value = mock_args
            mock_parser_instance.get_default.side_effect = lambda arg: {
                'host': '127.0.0.1',
                'port': 8000
            }.get(arg)
            mock_arg_parser.return_value = mock_parser_instance

            # Run the main function
            with patch('sys.argv', ['__main__.py']):
                cli_main()

            # Assertions
            mock_main.assert_called_once_with(host='0.0.0.0', port=9000, sse=True)
            mock_parser_instance.parse_args.assert_called_once()
            mock_parser_instance.get_default.assert_any_call('host')
            mock_parser_instance.get_default.assert_any_call('port')

    @patch('argparse.ArgumentParser')
    @patch('hkopenai.hk_climate_mcp_server.__main__.main')
    def test_sse_mode_from_env(self, mock_main, mock_arg_parser):
        """
        Test that SSE mode is activated via environment variable.
        """
        # Set environment variable for SSE
        with patch.dict(os.environ, {'TRANSPORT_MODE': 'sse'}):
            # Configure mocks for argparse
            mock_args = MagicMock(sse=False, port=8000, host='127.0.0.1')
            mock_parser_instance = MagicMock()
            mock_parser_instance.parse_args.return_value = mock_args
            mock_parser_instance.get_default.side_effect = lambda arg: {
                'host': '127.0.0.1',
                'port': 8000
            }.get(arg)
            mock_arg_parser.return_value = mock_parser_instance

            # Run the main function
            with patch('sys.argv', ['__main__.py']):
                cli_main()

            # Assertions
            mock_main.assert_called_once_with(host='127.0.0.1', port=8000, sse=True)
            mock_parser_instance.parse_args.assert_called_once()
            mock_parser_instance.get_default.assert_any_call('host')
            mock_parser_instance.get_default.assert_any_call('port')

    @patch('argparse.ArgumentParser')
    @patch('hkopenai.hk_climate_mcp_server.__main__.main')
    def test_invalid_port_env_variable(self, mock_main, mock_arg_parser):
        """
        Test that an invalid PORT environment variable does not cause an error
        and the default port is used.
        """
        with patch.dict(os.environ, {'PORT': 'invalid_port'}):
            mock_args = MagicMock(sse=False, port=8000, host='127.0.0.1')
            mock_parser_instance = MagicMock()
            mock_parser_instance.parse_args.return_value = mock_args
            mock_parser_instance.get_default.side_effect = lambda arg: {
                'host': '127.0.0.1',
                'port': 8000
            }.get(arg)
            mock_arg_parser.return_value = mock_parser_instance

            with patch('sys.argv', ['__main__.py']):
                cli_main()

            mock_main.assert_called_once_with(host='127.0.0.1', port=8000, sse=False)
            mock_parser_instance.parse_args.assert_called_once()
            mock_parser_instance.get_default.assert_any_call('host')
            mock_parser_instance.get_default.assert_any_call('port')

if __name__ == '__main__':
    unittest.main()
