"""
Core game logic for Minesweeper.
Handles mine placement, cell operations, and game state.
"""

import random
from enum import Enum
from typing import List, Tuple, Set


class CellState(Enum):
    """Represents the state of a cell in the minesweeper grid."""
    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"
    QUESTIONED = "questioned"


class GameState(Enum):
    """Represents the current state of the game."""
    NOT_STARTED = "not_started"
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class Difficulty:
    """Predefined difficulty levels matching Windows 3.11 Minesweeper."""
    BEGINNER = {"width": 9, "height": 9, "mines": 10}
    INTERMEDIATE = {"width": 16, "height": 16, "mines": 40}
    EXPERT = {"width": 30, "height": 16, "mines": 99}


class Cell:
    """Represents a single cell in the minesweeper grid."""
    
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.is_questioned = False
        self.adjacent_mines = 0
        
    @property
    def state(self) -> CellState:
        """Get the current state of the cell."""
        if self.is_flagged:
            return CellState.FLAGGED
        elif self.is_questioned:
            return CellState.QUESTIONED
        elif self.is_revealed:
            return CellState.REVEALED
        else:
            return CellState.HIDDEN
    
    def flag(self):
        """Toggle flag state of the cell."""
        if not self.is_revealed:
            if self.is_flagged:
                self.is_flagged = False
                self.is_questioned = True
            elif self.is_questioned:
                self.is_questioned = False
            else:
                self.is_flagged = True
    
    def reveal(self) -> bool:
        """Reveal the cell. Returns True if it's a mine."""
        if not self.is_flagged and not self.is_revealed:
            self.is_revealed = True
            return self.is_mine
        return False


class MinesweeperGame:
    """Main game logic class for Minesweeper."""
    
    def __init__(self, width: int = 9, height: int = 9, mines: int = 10):
        self.width = width
        self.height = height
        self.mine_count = mines
        self.grid: List[List[Cell]] = []
        self.game_state = GameState.NOT_STARTED
        self.flags_placed = 0
        self.cells_revealed = 0
        self.start_time = None
        self.end_time = None
        
        self._initialize_grid()
    
    def _initialize_grid(self):
        """Initialize the game grid with empty cells."""
        self.grid = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
    
    def _place_mines(self, first_click_row: int, first_click_col: int):
        """Place mines randomly on the grid, avoiding the first clicked cell."""
        mines_placed = 0
        while mines_placed < self.mine_count:
            row = random.randint(0, self.height - 1)
            col = random.randint(0, self.width - 1)
            
            # Don't place mine on first click or if already has mine
            if (row == first_click_row and col == first_click_col) or self.grid[row][col].is_mine:
                continue
                
            self.grid[row][col].is_mine = True
            mines_placed += 1
        
        self._calculate_adjacent_mines()
    
    def _calculate_adjacent_mines(self):
        """Calculate the number of adjacent mines for each cell."""
        for row in range(self.height):
            for col in range(self.width):
                if not self.grid[row][col].is_mine:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if (0 <= nr < self.height and 0 <= nc < self.width and 
                                self.grid[nr][nc].is_mine):
                                count += 1
                    self.grid[row][col].adjacent_mines = count
    
    def _get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all valid neighboring cell coordinates."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    neighbors.append((nr, nc))
        return neighbors
    
    def click_cell(self, row: int, col: int) -> bool:
        """
        Click on a cell to reveal it.
        Returns True if game continues, False if game ends (mine hit).
        """
        if (row < 0 or row >= self.height or col < 0 or col >= self.width or
            self.game_state in [GameState.WON, GameState.LOST]):
            return True
        
        cell = self.grid[row][col]
        
        # First click - initialize mines
        if self.game_state == GameState.NOT_STARTED:
            self.game_state = GameState.PLAYING
            self._place_mines(row, col)
        
        # Can't click flagged cells
        if cell.is_flagged:
            return True
        
        # Reveal the cell
        if cell.reveal():
            # Hit a mine
            self.game_state = GameState.LOST
            self._reveal_all_mines()
            return False
        
        # If it's an empty cell (no adjacent mines), reveal neighbors
        if cell.adjacent_mines == 0:
            self._reveal_empty_area(row, col)
        
        self._update_revealed_count()
        self._check_win_condition()
        return True
    
    def _reveal_empty_area(self, row: int, col: int):
        """Recursively reveal empty areas (flood fill)."""
        stack = [(row, col)]
        visited = set()
        
        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))
            
            cell = self.grid[r][c]
            if not cell.is_revealed and not cell.is_flagged:
                cell.is_revealed = True
                
                # If this cell has no adjacent mines, add its neighbors
                if cell.adjacent_mines == 0:
                    for nr, nc in self._get_neighbors(r, c):
                        if (nr, nc) not in visited:
                            stack.append((nr, nc))
    
    def _reveal_all_mines(self):
        """Reveal all mines when the game is lost."""
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col].is_mine:
                    self.grid[row][col].is_revealed = True
    
    def _update_revealed_count(self):
        """Update the count of revealed cells."""
        self.cells_revealed = sum(
            1 for row in self.grid for cell in row if cell.is_revealed
        )
    
    def _check_win_condition(self):
        """Check if the player has won the game."""
        total_cells = self.width * self.height
        if self.cells_revealed == total_cells - self.mine_count:
            self.game_state = GameState.WON
    
    def flag_cell(self, row: int, col: int):
        """Toggle flag on a cell."""
        if (row < 0 or row >= self.height or col < 0 or col >= self.width or
            self.game_state in [GameState.WON, GameState.LOST]):
            return
        
        cell = self.grid[row][col]
        old_flagged = cell.is_flagged
        cell.flag()
        
        # Update flag count
        if cell.is_flagged and not old_flagged:
            self.flags_placed += 1
        elif not cell.is_flagged and old_flagged:
            self.flags_placed -= 1
    
    def get_remaining_mines(self) -> int:
        """Get the number of mines remaining (mines - flags)."""
        return self.mine_count - self.flags_placed
    
    def reset_game(self, width: int = None, height: int = None, mines: int = None):
        """Reset the game with new parameters."""
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if mines is not None:
            self.mine_count = mines
            
        self.game_state = GameState.NOT_STARTED
        self.flags_placed = 0
        self.cells_revealed = 0
        self.start_time = None
        self.end_time = None
        self._initialize_grid()