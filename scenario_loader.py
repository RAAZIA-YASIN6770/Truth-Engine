import json
import os

class ScenarioLoader:
    def load_scenario(self, filename):
        """
        Loads a scenario JSON file from the app directory.
        """
        # Look for the file in the 'app' directory or current directory
        # Adjust paths as needed based on where this script runs
        search_paths = [
            os.path.join(os.path.dirname(__file__), 'data'),
            os.path.join(os.path.dirname(__file__), 'app'),
            os.path.dirname(__file__)
        ]

        for path in search_paths:
            filepath = os.path.join(path, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
        
        return None