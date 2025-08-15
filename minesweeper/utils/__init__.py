"""
Utility functions for the Minesweeper game.
"""

import json
import os
from typing import Dict, Any


class Settings:
    """Handle game settings and preferences."""
    
    def __init__(self, settings_file: str = "settings.json"):
        self.settings_file = settings_file
        self.default_settings = {
            "last_difficulty": "beginner",
            "sound_enabled": True,
            "window_position": None,
            "high_scores": {
                "beginner": None,
                "intermediate": None,
                "expert": None
            }
        }
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file or create default settings."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged = self.default_settings.copy()
                merged.update(settings)
                return merged
        except (json.JSONDecodeError, IOError):
            pass
        
        return self.default_settings.copy()
    
    def save_settings(self):
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError:
            pass  # Fail silently if we can't save settings
    
    def get(self, key: str, default=None):
        """Get a setting value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value."""
        self.settings[key] = value
        self.save_settings()
    
    def update_high_score(self, difficulty: str, time: int):
        """Update high score for a difficulty if it's better."""
        current_best = self.settings["high_scores"].get(difficulty)
        if current_best is None or time < current_best:
            self.settings["high_scores"][difficulty] = time
            self.save_settings()
            return True
        return False


def format_time(seconds: int) -> str:
    """Format time in seconds to MM:SS format."""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def validate_custom_game(width: int, height: int, mines: int) -> bool:
    """Validate custom game parameters."""
    if width < 9 or width > 30:
        return False
    if height < 9 or height > 24:
        return False
    if mines < 1 or mines >= (width * height):
        return False
    return True