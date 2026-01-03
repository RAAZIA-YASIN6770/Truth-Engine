class LogicEngine:
    @staticmethod
    def evaluate(scenario, selected_id):
        """
        Evaluates if the selected option matches the correct option in the scenario solution.
        """
        # Get solution data safely
        solution = scenario.get('solution', {})
        correct_id = solution.get('false_statement_id')
        
        is_correct = (selected_id == correct_id)
        
        return {
            "success": is_correct,
            "message": "Correct Answer!" if is_correct else "Incorrect Answer.",
            "details": solution.get('explanation', '')
        }