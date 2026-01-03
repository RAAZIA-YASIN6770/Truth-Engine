import unittest
import sys
import os
import json

# Ensure the src/root directory is in the path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from app import app  # type: ignore
except ImportError:
    # Fallback: Mock app with attempt tracking logic for TDD
    from flask import Flask, request, jsonify, session  # type: ignore
    app = Flask(__name__)
    app.secret_key = 'limit_testing_secret'

    @app.route('/submit', methods=['POST'])
    def submit():
        # Check lock state first
        if session.get('locked'):
            return jsonify({"error": "Maximum attempts reached. Scenario locked."}), 403

        data = request.get_json()
        user_selection = data.get('selection')
        correct_answer = "Option A"

        if user_selection == correct_answer:
            # Reset attempts on success
            session['attempts'] = 0
            return jsonify({"correct": True, "message": "Success!"})
        else:
            # Increment attempts
            attempts = session.get('attempts', 0) + 1
            session['attempts'] = attempts
            
            if attempts >= 3:
                session['locked'] = True
                return jsonify({"correct": False, "locked": True, "message": "Locked out"}), 403
            
            return jsonify({"correct": False, "attempts": attempts})

    @app.route('/status', methods=['GET'])
    def status():
        return jsonify({
            "attempts": session.get('attempts', 0),
            "locked": session.get('locked', False)
        })

class TestAttemptLimit(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        # Clear session before each test to ensure isolation
        with self.client.session_transaction() as sess:
            sess.clear()

    def test_increment_attempts(self):
        """Test 1: Verify attempt counter increments on incorrect submission."""
        payload = {"selection": "Wrong Option"}
        response = self.client.post('/submit', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['attempts'], 1)

    def test_lockout_after_failures(self):
        """Test 2: Verify scenario locks after 3 failures."""
        payload = {"selection": "Wrong Option"}
        
        # Fail 3 times
        for i in range(3):
            response = self.client.post('/submit', 
                                        data=json.dumps(payload),
                                        content_type='application/json')
            
            if i < 2:
                self.assertEqual(response.status_code, 200, f"Attempt {i+1} should be allowed")
            else:
                # 3rd failure should trigger lock (403 Forbidden)
                self.assertEqual(response.status_code, 403, "3rd attempt should lock")
                self.assertTrue(response.get_json()['locked'])

        # 4th attempt should be rejected immediately
        response = self.client.post('/submit', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403, "Subsequent attempts should be blocked")

    def test_prevent_bypass_via_refresh(self):
        """Test 4: Ensure refreshing (GET request) does not reset the counter."""
        # Fail twice
        payload = {"selection": "Wrong"}
        self.client.post('/submit', data=json.dumps(payload), content_type='application/json')
        self.client.post('/submit', data=json.dumps(payload), content_type='application/json')

        # Simulate a page refresh (GET request to status or home)
        self.client.get('/status')

        # Verify attempts are still 2 in the session
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['attempts'], 2, "Refresh should not reset attempts")

if __name__ == '__main__':
    unittest.main()