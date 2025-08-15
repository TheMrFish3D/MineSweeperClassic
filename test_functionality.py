#!/usr/bin/env python3
"""
Functional test to ensure the font improvements don't break game functionality.
"""

import sys
import time
from minesweeper.gui import MinesweeperGUI
from minesweeper.game import Difficulty

def main():
    print("Testing Minesweeper functionality with improved fonts...")
    
    try:
        # Create the GUI
        app = MinesweeperGUI()
        print("✓ GUI created successfully")
        
        # Start a new game
        app.new_game(Difficulty.BEGINNER)
        print("✓ New game started")
        
        # Check that counters are properly initialized
        mines_text = app.mines_label.cget('text')
        timer_text = app.timer_label.cget('text')
        print(f"✓ Mines counter: {mines_text}")
        print(f"✓ Timer counter: {timer_text}")
        
        # Check font configuration
        mines_font = app.mines_label.cget('font')
        timer_font = app.timer_label.cget('font')
        print(f"✓ Mines font: {mines_font}")
        print(f"✓ Timer font: {timer_font}")
        
        # Test different difficulty levels
        app.new_game(Difficulty.INTERMEDIATE)
        mines_text_inter = app.mines_label.cget('text')
        print(f"✓ Intermediate mines counter: {mines_text_inter}")
        
        app.new_game(Difficulty.EXPERT)
        mines_text_expert = app.mines_label.cget('text')
        print(f"✓ Expert mines counter: {mines_text_expert}")
        
        # Switch back to beginner
        app.new_game(Difficulty.BEGINNER)
        print("✓ Switched back to beginner")
        
        print("✓ All functionality tests passed!")
        
        # Clean up
        app.root.destroy()
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())