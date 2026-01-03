class ScenarioLoader:
    def load_scenario(self, scenario_id):
        # Mock implementation for MVP
        return {
            "id": 1, 
            "correct_answer": "Option A",
            "statements": [
                {"text": "Sky is blue", "is_true": True},
                {"text": "Water is dry", "is_true": False}, # The lie
                {"text": "Fire is hot", "is_true": True}
            ]
        }