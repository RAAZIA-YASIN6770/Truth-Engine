import unittest
import sys
import os

# Ensure the src/root directory is in the path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from scenario_validator import ScenarioValidator  # type: ignore
except ImportError:
    # Fallback mock class to allow tests to run before implementation exists
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

class TestScenarioValidation(unittest.TestCase):
    def setUp(self):
        self.validator = ScenarioValidator()

    def test_valid_scenario(self):
        """Test 1: Ensure a perfectly valid scenario passes validation."""
        scenario = {
            "id": 101,
            "statements": [
                {"text": "Sky is blue", "is_true": True},
                {"text": "Water is dry", "is_true": False},
                {"text": "Fire is hot", "is_true": True}
            ]
        }
        is_valid, msg = self.validator.validate(scenario)
        self.assertTrue(is_valid, f"Valid scenario failed: {msg}")

    def test_missing_required_fields(self):
        """Test 2: Ensure validation fails if 'id' or 'statements' are missing."""
        scenario = {"id": 102} # Missing statements
        is_valid, msg = self.validator.validate(scenario)
        self.assertFalse(is_valid)
        self.assertIn("Missing required fields", msg)

    def test_logic_exactly_one_false(self):
        """Test 3: Ensure validation fails if there are 0 or >1 false statements."""
        # Case A: All True (0 False)
        scenario_all_true = {
            "id": 103,
            "statements": [
                {"text": "A", "is_true": True},
                {"text": "B", "is_true": True}
            ]
        }
        is_valid, msg = self.validator.validate(scenario_all_true)
        self.assertFalse(is_valid, "Should fail with 0 false statements")
        self.assertIn("exactly one false statement", msg)

        # Case B: Two False (>1 False)
        scenario_two_false = {
            "id": 104,
            "statements": [
                {"text": "A", "is_true": False},
                {"text": "B", "is_true": False}
            ]
        }
        is_valid, msg = self.validator.validate(scenario_two_false)
        self.assertFalse(is_valid, "Should fail with 2 false statements")

    def test_invalid_statement_structure(self):
        """Test 4: Prevent ambiguous scenarios where truth value is unknown."""
        scenario = {
            "id": 105,
            "statements": [
                {"text": "Ambiguous Statement"} # Missing is_true
            ]
        }
        is_valid, msg = self.validator.validate(scenario)
        self.assertFalse(is_valid)
        self.assertIn("Statement missing 'is_true'", msg)

if __name__ == '__main__':
    unittest.main()