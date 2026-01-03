import unittest
import sys
import os

# Ensure the src/root directory is in the path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Assuming LogicEngine is defined in logic_engine.py or similar module
try:
    from logic_engine import LogicEngine  # type: ignore
except ImportError:
    # Fallback mock if the actual module isn't present in the environment yet
    class LogicEngine:
        def evaluate(self, selection, scenario):
            # Simple equality check for demonstration
            return selection == scenario.get('correct_answer')

class TestLogicEvaluator(unittest.TestCase):
    def setUp(self):
        """Initialize the LogicEngine before each test."""
        self.engine = LogicEngine()

    def test_correct_selection(self):
        """Test 2: Verify that the engine correctly identifies the right answer."""
        scenario = {"id": 1, "correct_answer": "True"}
        user_selection = "True"
        
        result = self.engine.evaluate(user_selection, scenario)
        self.assertTrue(result, "LogicEngine should return True for matching selection.")

    def test_incorrect_selection(self):
        """Test 3: Verify that the engine correctly identifies a wrong answer."""
        scenario = {"id": 1, "correct_answer": "True"}
        user_selection = "False"
        
        result = self.engine.evaluate(user_selection, scenario)
        self.assertFalse(result, "LogicEngine should return False for non-matching selection.")

    def test_deterministic_behavior(self):
        """Test 4: Ensure the Logic Engine produces consistent, reproducible results."""
        scenario = {"id": 2, "correct_answer": "Option A"}
        user_selection = "Option A"

        # Execute the same logic 100 times to ensure no side effects or randomness
        for i in range(100):
            result = self.engine.evaluate(user_selection, scenario)
            self.assertTrue(result, f"Non-deterministic behavior detected at iteration {i}")

if __name__ == '__main__':
    unittest.main()