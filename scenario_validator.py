class ScenarioValidator:
    @staticmethod
    def validate(scenario):
        # 1. Check required fields
        if "id" not in scenario or "statements" not in scenario:
            return False, "Missing required fields: 'id' or 'statements'"
        
        statements = scenario["statements"]
        if not isinstance(statements, list) or len(statements) == 0:
            return False, "Statements must be a non-empty list"

        # 2. Logic Check: Count false statements
        false_count = 0
        for stmt in statements:
            # 3. Check statement structure
            if "is_true" not in stmt:
                return False, "Statement missing 'is_true' field"
            
            if not stmt["is_true"]:
                false_count += 1
        
        # 4. Ensure exactly one false statement
        if false_count != 1:
            return False, f"Scenario must have exactly one false statement, found {false_count}"
        
        return True, "Valid"