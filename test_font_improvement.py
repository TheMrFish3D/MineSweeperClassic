#!/usr/bin/env python3
"""
Test script to run the minesweeper game and capture a screenshot
to validate the font improvements.
"""

import sys
import os
import time
import subprocess
from minesweeper.gui import MinesweeperGUI

def main():
    print("Testing Minesweeper with improved font sizes...")
    
    try:
        # Create the GUI
        app = MinesweeperGUI()
        print("✓ GUI created successfully")
        
        # Update the display
        app.root.update()
        print("✓ GUI updated")
        
        # Give it a moment to render
        app.root.after(2000, lambda: take_screenshot_and_quit(app))
        
        # Start the main loop
        app.root.mainloop()
        print("✓ Test completed")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

def take_screenshot_and_quit(app):
    """Take a screenshot and quit the application"""
    try:
        # Take screenshot using import command
        subprocess.run(['import', '-window', 'root', 'font_improvements_test.png'], 
                      env=dict(os.environ, DISPLAY=':99'), check=True)
        print("✓ Screenshot taken")
    except Exception as e:
        print(f"! Could not take screenshot: {e}")
    
    # Quit the application
    app.root.quit()

if __name__ == '__main__':
    sys.exit(main())