# Minesweeper Classic

A faithful recreation of the Windows 3.11 Minesweeper game that runs cross-platform on Linux, Windows, and macOS.

## Features

- **Authentic Windows 3.11 Look**: Recreates the classic appearance and feel of the original Minesweeper
- **Cross-Platform**: Runs on any system with Python 3.8+ and Tkinter
- **Standard Difficulty Levels**: Beginner (9x9, 10 mines), Intermediate (16x16, 40 mines), Expert (30x16, 99 mines)
- **Classic Gameplay**: Left-click to reveal, right-click to flag/question mark
- **Timer and Mine Counter**: Digital displays matching the original
- **Menu System**: Game menu with difficulty selection and help

## Requirements

- Python 3.8 or higher
- Tkinter (included with most Python installations)

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TheMrFish3D/MineSweeperClassic.git
   cd MineSweeperClassic
   ```

2. **Run the game:**
   ```bash
   python3 run_minesweeper.py
   ```
   
   Or alternatively:
   ```bash
   python3 -m minesweeper.main
   ```

## Installation

For a more permanent installation:

```bash
pip install -e .
minesweeper
```

## How to Play

- **Left Click**: Reveal a cell
- **Right Click**: Flag a cell as a mine (🚩) or mark as questionable (?)
- **Goal**: Reveal all cells that don't contain mines
- **Numbers**: Show how many mines are adjacent to that cell
- **Game Over**: Hit a mine or reveal all safe cells to win

## Project Structure

```
MineSweeperClassic/
├── minesweeper/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Main entry point
│   ├── game/
│   │   └── __init__.py      # Core game logic
│   ├── gui/
│   │   └── __init__.py      # Tkinter GUI interface
│   └── utils/
│       └── __init__.py      # Utility functions and settings
├── run_minesweeper.py       # Simple launcher script
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies (none needed)
├── .gitignore              # Git ignore file
└── readme.md               # This file
```

## Development

The codebase is organized into clear modules:

- **game/**: Contains all game logic, mine placement, cell operations, and game state management
- **gui/**: Handles the Tkinter interface and Windows 3.11 styling
- **utils/**: Provides settings management and utility functions

## Windows Shortcuts

For easy launching on Windows:

- **Minesweeper.bat**: Double-click to run the game directly
- **create_shortcut.py**: Run this script to create a desktop shortcut (.lnk file)
  - Requires `pywin32` package: `pip install pywin32`
  - Creates a proper Windows shortcut on your desktop

## Contributing

This project is set up for easy contribution and extension by AI agents or developers:

1. All code is well-documented with docstrings
2. Modular design allows easy feature additions
3. Standard Python project structure
4. No external dependencies required

## License

MIT License - Feel free to use and modify as needed.

## Screenshots

The game recreates the authentic Windows 3.11 Minesweeper experience with:
- Classic gray 3D button styling
- Digital mine counter and timer displays
- Smiley face status indicator
- Traditional mine and flag symbols
- Proper color coding for numbers (blue for 1, green for 2, etc.)
