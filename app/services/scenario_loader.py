import json
import os

class ScenarioLoader:
    """
    Service to load logic puzzle scenarios from the data directory.
    """
    def __init__(self):
        # Determine the absolute path to the 'data' directory
        # Structure: app/services/scenario_loader.py -> ../../data
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(current_dir, '..', '..', 'data')

    def load_scenario(self, filename: str) -> dict | None:
        """
        Loads a JSON scenario file.
        Returns the dictionary data or None if file not found/invalid.
        """
        file_path = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return None