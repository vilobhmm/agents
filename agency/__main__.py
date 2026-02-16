"""
Agency - Multi-Agent Multi-Channel Coordination System

Main entry point - delegates to the comprehensive CLI system.
"""

import sys
from agency.cli import AgencyCLI


def main():
    """Main entry point - use the comprehensive CLI"""
    cli = AgencyCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()
