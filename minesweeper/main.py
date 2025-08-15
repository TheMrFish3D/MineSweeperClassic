#!/usr/bin/env python3
"""
Main entry point for the Minesweeper Classic game.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from minesweeper.gui import main as gui_main


def main():
    """Main entry point for the application."""
    try:
        gui_main()
    except KeyboardInterrupt:
        print("\\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()