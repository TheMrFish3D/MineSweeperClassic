"""
Create Windows shortcut for Minesweeper Classic.
Run this script on Windows to create a desktop shortcut.
"""
import os
import sys

def create_windows_shortcut():
    """Create a Windows .lnk shortcut file."""
    try:
        import win32com.client
        
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Create shortcut object
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(os.path.join(os.path.expanduser("~"), "Desktop", "Minesweeper Classic.lnk"))
        
        # Set shortcut properties
        shortcut.Targetpath = sys.executable  # Python executable
        shortcut.Arguments = os.path.join(current_dir, "run_minesweeper.py")
        shortcut.WorkingDirectory = current_dir
        shortcut.IconLocation = sys.executable
        shortcut.Description = "Minesweeper Classic - Windows 3.11 Style"
        
        # Save the shortcut
        shortcut.save()
        print("Desktop shortcut created successfully!")
        
    except ImportError:
        print("pywin32 module not found. Please install it with: pip install pywin32")
        print("Alternatively, use the provided Minesweeper.bat file")
    except Exception as e:
        print(f"Error creating shortcut: {e}")
        print("You can manually create a shortcut to run_minesweeper.py")

if __name__ == "__main__":
    if os.name == 'nt':  # Windows
        create_windows_shortcut()
    else:
        print("This script is for Windows only.")
        print("On other systems, you can run: python run_minesweeper.py")