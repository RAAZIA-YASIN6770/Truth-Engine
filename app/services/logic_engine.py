class LogicEngine:
    """
    Deterministic rule-based engine to validate user logic choices.
    """
    
    @staticmethod
    def evaluate(scenario: dict, selected_statement_id: int) -> dict:
        """
        Validates if the selected statement is the logically false one.
        
        Args:
            scenario (dict): The loaded scenario data.
            selected_statement_id (int): The ID of the statement selected by the user.
            
        Returns:
            dict: Result containing 'success' (bool) and 'message' (str).
        """
        # 1. Validate Scenario Integrity
        if "solution" not in scenario or "false_statement_id" not in scenario["solution"]:
            return {
                "success": False,
                "message": "System Error: Scenario solution data missing."
            }
            
        correct_id = scenario["solution"]["false_statement_id"]
        
        # 2. Deterministic Evaluation
        if selected_statement_id == correct_id:
            return {
                "success": True,
                "message": "LOGIC VERIFIED. Contradiction successfully isolated.",
                "details": scenario["solution"].get("explanation", "Correct.")
            }
        else:
            return {
                "success": False,
                "message": "LOGIC FAILURE. The selected statement does not resolve the contradiction.",
                # No hints provided as per requirements
            }