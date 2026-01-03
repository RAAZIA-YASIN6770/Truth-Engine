from flask import Flask, request, jsonify, session
import os
from logic_engine import LogicEngine

def create_app():
    app = Flask(__name__)
    # Use environment variable or default for testing
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

    # Initialize Logic Engine
    logic_engine = LogicEngine()

    # Mock Database / Scenario for MVP
    current_scenario = {
        "id": 1, 
        "correct_answer": "Option A",
        "statements": [
            {"text": "Sky is blue", "is_true": True},
            {"text": "Water is dry", "is_true": False}, # The lie
            {"text": "Fire is hot", "is_true": True}
        ]
    }

    @app.route('/')
    def index():
        return "Truth Engine Interface Active", 200

    @app.route('/submit', methods=['POST'])
    def submit():
        # Check lock state
        if session.get('locked'):
            return jsonify({"error": "Maximum attempts reached. Scenario locked."}), 403

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_selection = data.get('selection')
        
        # Evaluate
        is_correct = logic_engine.evaluate(user_selection, current_scenario)

        if is_correct:
            session['attempts'] = 0
            return jsonify({"correct": True, "message": "Success!"})
        else:
            attempts = session.get('attempts', 0) + 1
            session['attempts'] = attempts
            
            if attempts >= 3:
                session['locked'] = True
                return jsonify({"correct": False, "locked": True, "message": "Locked out"}), 403
            
            return jsonify({"correct": False, "attempts": attempts})

    @app.route('/reset', methods=['POST'])
    def reset():
        session.clear()
        return jsonify({"message": "Scenario reset"}), 200

    @app.route('/status', methods=['GET'])
    def status():
        return jsonify({
            "attempts": session.get('attempts', 0),
            "locked": session.get('locked', False)
        })

    return app

# Expose 'app' for WSGI or simple imports if needed
app = create_app()