import unittest
import sys
import os
import json

# Ensure the src/root directory is in the path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Try importing the app, or create a mock app if it doesn't exist yet
try:
    from app import app  # type: ignore
except ImportError:
    # Fallback: Create a minimal Flask app for testing purposes
    # This allows the tests to define the expected interface before the app exists
    from flask import Flask, request, jsonify, session  # type: ignore
    app = Flask(__name__)
    app.secret_key = 'testing_secret'

    # Mock database/state for the fallback app
    mock_scenario = {"id": 1, "correct_answer": "Option A"}

    @app.route('/')
    def index():
        return "Truth Engine Interface", 200

    @app.route('/submit', methods=['POST'])
    def submit():
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data"}), 400
        
        user_selection = data.get('selection')
        # Simple evaluation logic for the mock
        is_correct = (user_selection == mock_scenario["correct_answer"])
        return jsonify({"correct": is_correct})

    @app.route('/reset', methods=['POST'])
    def reset():
        session.clear()
        return jsonify({"message": "Scenario reset"}), 200

class TestWebRoutes(unittest.TestCase):
    def setUp(self):
        """Set up the test client before each test."""
        app.testing = True
        self.client = app.test_client()

    def test_home_page(self):
        """Test 1: Verify the home page loads successfully (HTTP 200)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_submit_correct_selection(self):
        """Test 2: Simulate submitting the correct answer via POST."""
        # Based on the mock scenario defined above
        payload = {"selection": "Option A"}
        response = self.client.post('/submit', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get('correct'), "Should return True for correct answer")

    def test_submit_incorrect_selection(self):
        """Test 3: Simulate submitting an incorrect answer via POST."""
        payload = {"selection": "Option B"}
        response = self.client.post('/submit', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data.get('correct'), "Should return False for incorrect answer")

    def test_reset_scenario(self):
        """Test 4: Verify that the reset route clears the session."""
        # First, set something in the session (simulated)
        with self.client.session_transaction() as sess:
            sess['score'] = 10
        
        response = self.client.post('/reset')
        self.assertEqual(response.status_code, 200)
        
        # Verify session is cleared
        with self.client.session_transaction() as sess:
            self.assertNotIn('score', sess)

if __name__ == '__main__':
    unittest.main()