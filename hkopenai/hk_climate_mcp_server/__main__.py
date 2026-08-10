from hkopenai_common.cli_utils import cli_main
from .server import server


def main():
    """Console-script entry point for the HK Climate MCP Server."""
    cli_main(server, "HK Climate MCP Server")


if __name__ == "__main__":
    main()
