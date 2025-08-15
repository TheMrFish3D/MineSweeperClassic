"""
Tkinter GUI for Minesweeper that recreates the Windows 3.11 appearance.
"""

import tkinter as tk
from tkinter import messagebox, Menu, font
import time
from typing import Optional

from ..game import MinesweeperGame, GameState, Difficulty, CellState


def _get_best_digital_font():
    """Get the best available digital-style font for counters."""
    # Try digital-style fonts in order of preference
    candidates = [
        ('Consolas', 22, 'bold'),
        ('Monaco', 22, 'bold'), 
        ('Lucida Console', 22, 'bold'),
        ('Courier New', 22, 'bold'),
        ('monospace', 22, 'bold')
    ]
    
    for font_spec in candidates:
        try:
            # Test if font is available
            test_font = font.Font(family=font_spec[0], size=font_spec[1], weight=font_spec[2])
            if test_font.actual()['family']:  # Font is available
                return font_spec
        except:
            continue
    
    # Fallback to default
    return ('TkDefaultFont', 20, 'bold')


class MinesweeperGUI:
    """Main GUI class for the Minesweeper game."""
    
    # Windows 3.11 color scheme
    COLORS = {
        'background': '#c0c0c0',
        'button_face': '#c0c0c0',
        'button_highlight': '#ffffff',
        'button_shadow': '#808080',
        'button_dark_shadow': '#404040',
        'text': '#000000',
        'mine_red': '#ff0000',
        'flag_red': '#ff0000',
        'numbers': {
            1: '#0000ff',  # Blue
            2: '#008000',  # Green
            3: '#ff0000',  # Red
            4: '#000080',  # Navy
            5: '#800000',  # Maroon
            6: '#008080',  # Teal
            7: '#000000',  # Black
            8: '#808080',  # Gray
        }
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.game: Optional[MinesweeperGame] = None
        self.cell_buttons = []
        self.mines_label = None
        self.timer_label = None
        self.smiley_button = None
        self.start_time = None
        self.timer_running = False
        self.last_cell_states = {}  # Track cell states to minimize updates
        self.digital_font = _get_best_digital_font()  # Get best digital font
        
        self._setup_window()
        self._create_menu()
        self.new_game(Difficulty.BEGINNER)
    
    def _setup_window(self):
        """Configure the main window."""
        self.root.title("Minesweeper")
        self.root.configure(bg=self.COLORS['background'])
        self.root.resizable(False, False)
        
        # Set window icon (if available)
        try:
            # This would set an icon if we had one
            pass
        except:
            pass
    
    def _create_menu(self):
        """Create the menu bar."""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        game_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        
        game_menu.add_command(label="New", command=lambda: self.new_game())
        game_menu.add_separator()
        game_menu.add_command(label="Beginner", 
                             command=lambda: self.new_game(Difficulty.BEGINNER))
        game_menu.add_command(label="Intermediate", 
                             command=lambda: self.new_game(Difficulty.INTERMEDIATE))
        game_menu.add_command(label="Expert", 
                             command=lambda: self.new_game(Difficulty.EXPERT))
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _show_about(self):
        """Show the about dialog."""
        messagebox.showinfo(
            "About Minesweeper",
            "Minesweeper Classic\\n\\n"
            "A faithful recreation of the Windows 3.11 Minesweeper game.\\n\\n"
            "Left click to reveal cells\\n"
            "Right click to flag/unflag mines\\n\\n"
            "Goal: Reveal all cells without hitting mines!"
        )
    
    def new_game(self, difficulty: dict = None):
        """Start a new game with the specified difficulty."""
        if difficulty is None:
            difficulty = Difficulty.BEGINNER
            
        # Clear existing widgets
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        
        # Create new game
        self.game = MinesweeperGame(
            width=difficulty["width"],
            height=difficulty["height"],
            mines=difficulty["mines"]
        )
        
        self.timer_running = False
        self.start_time = None
        self.last_cell_states = {}  # Reset cell state tracking
        
        self._create_widgets()
        self._update_display()
        
        # Reset smiley to normal state
        if self.smiley_button:
            self.smiley_button.config(text="🙂", bg='#ffff00')
    
    def _create_widgets(self):
        """Create all the GUI widgets."""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.COLORS['background'], 
                             relief=tk.RAISED, bd=2)
        main_frame.pack(padx=5, pady=5)
        
        # Top panel with counter, smiley, and timer
        top_frame = tk.Frame(main_frame, bg=self.COLORS['background'], 
                            relief=tk.SUNKEN, bd=2)
        top_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # Mines counter
        mines_frame = tk.Frame(top_frame, bg='black', relief=tk.SUNKEN, bd=1)
        mines_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.mines_label = tk.Label(
            mines_frame, 
            text=f"{self.game.get_remaining_mines():03d}",
            bg='black',
            fg='red',
            font=self.digital_font,  # Use the best available digital font
            width=3,
            anchor='center'
        )
        self.mines_label.pack(padx=3, pady=3)
        
        # Smiley button
        self.smiley_button = tk.Button(
            top_frame,
            text="🙂",
            font=('Arial', 16),
            width=2,
            height=1,
            bg='#ffff00',  # Yellow background like classic Windows minesweeper
            relief=tk.RAISED,
            bd=2,
            command=lambda: self.new_game()
        )
        self.smiley_button.pack(side=tk.LEFT, expand=True, padx=5, pady=5)
        
        # Timer
        timer_frame = tk.Frame(top_frame, bg='black', relief=tk.SUNKEN, bd=1)
        timer_frame.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.timer_label = tk.Label(
            timer_frame,
            text="000",
            bg='black',
            fg='red',
            font=self.digital_font,  # Use the best available digital font
            width=3,
            anchor='center'
        )
        self.timer_label.pack(padx=3, pady=3)
        
        # Game grid
        grid_frame = tk.Frame(main_frame, bg=self.COLORS['background'], 
                             relief=tk.SUNKEN, bd=2)
        grid_frame.pack(padx=2, pady=2)
        
        self._create_grid(grid_frame)
        
        # Start timer updates
        self._update_timer()
    
    def _create_grid(self, parent):
        """Create the minesweeper grid."""
        self.cell_buttons = []
        
        for row in range(self.game.height):
            button_row = []
            for col in range(self.game.width):
                btn = tk.Button(
                    parent,
                    text="",
                    width=2,
                    height=1,
                    font=('Arial', 14, 'bold'),  # Optimized font size for better proportion
                    bg=self.COLORS['button_face'],
                    relief=tk.RAISED,
                    bd=2
                )
                btn.grid(row=row, column=col, padx=0, pady=0)
                
                # Bind events
                btn.bind('<Button-1>', lambda e, r=row, c=col: self._on_left_click(r, c))
                btn.bind('<Button-3>', lambda e, r=row, c=col: self._on_right_click(r, c))
                
                button_row.append(btn)
            self.cell_buttons.append(button_row)
    
    def _on_left_click(self, row: int, col: int):
        """Handle left mouse click on a cell."""
        if self.game.game_state in [GameState.WON, GameState.LOST]:
            return
            
        # Don't allow clicks on already revealed cells
        cell = self.game.grid[row][col]
        if cell.is_revealed:
            return
            
        # Start timer on first click
        if self.game.game_state == GameState.NOT_STARTED:
            self.start_time = time.time()
            self.timer_running = True
        
        # Click the cell
        continue_game = self.game.click_cell(row, col)
        
        if not continue_game:
            # Game lost
            self.timer_running = False
            self.smiley_button.config(text="😵", bg='#ffff00')
            messagebox.showinfo("Game Over", "You hit a mine! Game Over.")
        elif self.game.game_state == GameState.WON:
            # Game won
            self.timer_running = False
            self.smiley_button.config(text="😎", bg='#ffff00')
            elapsed = int(time.time() - self.start_time) if self.start_time else 0
            messagebox.showinfo("Congratulations!", 
                              f"You won! Time: {elapsed} seconds")
        
        self._update_display()
    
    def _on_right_click(self, row: int, col: int):
        """Handle right mouse click on a cell."""
        if self.game.game_state in [GameState.WON, GameState.LOST]:
            return
            
        # Don't allow right-click on already revealed cells
        cell = self.game.grid[row][col]
        if cell.is_revealed:
            return
            
        self.game.flag_cell(row, col)
        self._update_display()
    
    def _update_display(self):
        """Update the visual display of all game elements."""
        # Update mine counter
        remaining = self.game.get_remaining_mines()
        self.mines_label.config(text=f"{remaining:03d}")
        
        # Update grid - only update cells that have changed
        for row in range(self.game.height):
            for col in range(self.game.width):
                cell = self.game.grid[row][col]
                btn = self.cell_buttons[row][col]
                
                # Create a state key for this cell
                state_key = (row, col)
                current_state = (cell.state, cell.is_mine, cell.adjacent_mines, cell.is_revealed)
                
                # Only update if state has changed
                if state_key not in self.last_cell_states or self.last_cell_states[state_key] != current_state:
                    self.last_cell_states[state_key] = current_state
                    
                    if cell.state == CellState.FLAGGED:
                        btn.config(
                            text="🚩",
                            bg=self.COLORS['button_face'],
                            relief=tk.RAISED,
                            fg=self.COLORS['text'],
                            state=tk.NORMAL,  # Keep enabled for unflagging
                            bd=2
                        )
                    elif cell.state == CellState.QUESTIONED:
                        btn.config(
                            text="?",
                            bg=self.COLORS['button_face'],
                            relief=tk.RAISED,
                            fg=self.COLORS['text'],
                            state=tk.NORMAL,  # Keep enabled for cycling
                            bd=2
                        )
                    elif cell.state == CellState.REVEALED:
                        # Disable button functionality for revealed cells
                        btn.config(state=tk.DISABLED)
                        
                        if cell.is_mine:
                            # Show mine
                            btn.config(
                                text="💣",
                                bg=self.COLORS['mine_red'],
                                relief=tk.FLAT,  # Changed from SUNKEN to FLAT for flatter appearance
                                fg=self.COLORS['text'],
                                bd=1,  # Reduced border for flatter look
                                disabledforeground=self.COLORS['text']  # Ensure text shows when disabled
                            )
                        elif cell.adjacent_mines > 0:
                            # Show number
                            color = self.COLORS['numbers'].get(cell.adjacent_mines, 
                                                             self.COLORS['text'])
                            btn.config(
                                text=str(cell.adjacent_mines),
                                bg=self.COLORS['background'],
                                relief=tk.FLAT,  # Changed from SUNKEN to FLAT for flatter appearance
                                fg=color,
                                bd=1,  # Reduced border for flatter look
                                disabledforeground=color  # Ensure text shows when disabled
                            )
                        else:
                            # Empty cell
                            btn.config(
                                text="",
                                bg=self.COLORS['background'],
                                relief=tk.FLAT,  # Changed from SUNKEN to FLAT for flatter appearance
                                fg=self.COLORS['text'],
                                bd=1,  # Reduced border for flatter look
                                disabledforeground=self.COLORS['text']  # Ensure text shows when disabled
                            )
                    else:
                        # Hidden cell - ensure it's enabled
                        btn.config(
                            text="",
                            bg=self.COLORS['button_face'],
                            relief=tk.RAISED,
                            fg=self.COLORS['text'],
                            state=tk.NORMAL,  # Re-enable button
                            bd=2  # Full border for raised appearance
                        )
    
    def _update_timer(self):
        """Update the timer display."""
        if self.timer_running and self.start_time:
            elapsed = int(time.time() - self.start_time)
            elapsed = min(elapsed, 999)  # Cap at 999 like original
            self.timer_label.config(text=f"{elapsed:03d}")
        
        # Schedule next update
        self.root.after(1000, self._update_timer)
    
    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()


def main():
    """Main entry point for the GUI application."""
    app = MinesweeperGUI()
    app.run()


if __name__ == "__main__":
    main()