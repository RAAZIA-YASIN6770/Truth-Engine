from flask import Flask, request, jsonify, session, render_template
import os
from logic_engine import LogicEngine

def create_app():
    app = Flask(__name__)
    # Use environment variable or default for testing
    app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

    # Initialize Logic Engine
    logic_engine = LogicEngine()

    # Mock Levels Data (For the Level Select Grid)
    levels = [
        {"id": 1, "title": "Basic Logic"},
        {"id": 7, "title": "Python Logic"},
        {"id": 10, "title": "Python Functions"}
    ]

    # Mock Database with multiple scenarios
    scenarios_db = {
        1: {
            "id": 1, 
            "title": "Basic Logic",
            "statements": [
                {"id": 1, "text": "Sky is blue", "is_true": True},
                {"id": 2, "text": "Water is dry", "is_true": False},
                {"id": 3, "text": "Fire is hot", "is_true": True}
            ],
            "solution": {"explanation": "Water is liquid and wet, not dry."}
        },
        7: {
            "id": 7, 
            "title": "Python Logic",
            "statements": [
                {"id": 1, "text": "Lists are mutable", "is_true": True},
                {"id": 2, "text": "Tuples are mutable", "is_true": False},
                {"id": 3, "text": "Dictionaries have keys", "is_true": True}
            ],
            "solution": {"explanation": "Tuples are immutable in Python."}
        },
        10: {
            "id": 10, 
            "title": "Python Functions",
            "statements": [
                {"id": 1, "text": "def creates functions", "is_true": True},
                {"id": 2, "text": "print() returns a string", "is_true": False},
                {"id": 3, "text": "return exits function", "is_true": True}
            ],
            "solution": {"explanation": "print() displays text but returns None."}
        }
    }

    @app.route('/')
    def index():
        # Show the level selection grid
        return render_template('index.html', levels=levels, scenario=None)

    @app.route('/scenario/<int:scenario_id>', methods=['GET', 'POST'])
    def scenario_route(scenario_id):
        # Load scenario from DB, default to Level 1 if not found
        if scenario_id in scenarios_db:
            scenario_data = scenarios_db[scenario_id].copy()
        else:
            scenario_data = scenarios_db[1].copy()
        scenario_data['id'] = scenario_id
        
        if request.method == 'POST':
            # Handle the form submission
            print(f"DEBUG: Form submitted for Scenario {scenario_id}")
            user_selection = request.form.get('statement_id')
            
            # Find the selected statement safely
            selected_stmt = None
            if user_selection:
                for s in scenario_data['statements']:
                    if str(s['id']) == str(user_selection):
                        selected_stmt = s
                        break
            
            is_correct = False
            # The correct answer is the FALSE statement
            if selected_stmt and selected_stmt['is_true'] is False:
                is_correct = True
            
            result = {
                "success": is_correct,
                "explanation": scenario_data['solution']['explanation'] if is_correct else "Incorrect. That statement is true."
            }
            
            print(f"DEBUG: Rendering result: {result}")
            # Render the SAME page with the result (shows Back button)
            return render_template('index.html', levels=levels, scenario=scenario_data, result=result)

        # GET request: Show form, no result yet
        return render_template('index.html', levels=levels, scenario=scenario_data, result=None)

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
        is_correct = logic_engine.evaluate(user_selection, scenarios_db[1])

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