import json
import os

class ScenarioLoader:
    """
    Service to load logic puzzle scenarios from the data directory.
    """
    def __init__(self):
        # Determine search paths for scenario files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.search_paths = [
            os.path.abspath(os.path.join(current_dir, '..')),           # app/
            os.path.abspath(os.path.join(current_dir, '..', '..', 'data')), # data/ (root)
            os.path.abspath(os.path.join(current_dir, '..', 'data'))    # app/data/
        ]

    def load_scenario(self, filename: str) -> dict | None:
        """
        Loads a JSON scenario file.
        Returns the dictionary data or None if file not found/invalid.
        """
        for path in self.search_paths:
            file_path = os.path.join(path, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue
        
        # Debugging: Print if file not found
        print(f"Warning: {filename} not found in search paths.")
        return None