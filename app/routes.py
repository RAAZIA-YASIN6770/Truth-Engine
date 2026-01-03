from flask import Blueprint, render_template, request, flash, session  # type: ignore
from app.services.scenario_loader import ScenarioLoader
from app.services.logic_engine import LogicEngine

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Main game interface.
    Loads the scenario and handles user submissions.
    """
    loader = ScenarioLoader()
    scenario = loader.load_scenario("scenario_1.json")

    if not scenario:
        return "System Error: Scenario data could not be loaded.", 500

    # Initialize attempt counter in session
    if 'attempts' not in session:
        session['attempts'] = 0

    # Check if system is locked
    MAX_ATTEMPTS = 3
    locked = session.get('attempts', 0) >= MAX_ATTEMPTS

    if request.method == 'POST':
        if locked:
            flash("ACCESS DENIED: System is locked due to excessive failures.", 'danger')
        else:
            selected_id = request.form.get('statement_id')
            
            if selected_id:
                try:
                    s_id = int(selected_id)
                    result = LogicEngine.evaluate(scenario, s_id)
                    
                    if result['success']:
                        flash(result['message'], 'success')
                        if result.get('details'):
                            flash(result['details'], 'info')
                    else:
                        session['attempts'] += 1
                        remaining = MAX_ATTEMPTS - session['attempts']
                        if remaining <= 0:
                            flash("CRITICAL FAILURE: Maximum attempts exceeded. System Locked.", 'danger')
                            locked = True
                        else:
                            flash(f"{result['message']} Attempts remaining: {remaining}", 'danger')
                except ValueError:
                    flash("Invalid input detected.", 'warning')
            else:
                flash("Please select a statement.", 'warning')

    return render_template('scenario.html', scenario=scenario, locked=locked, attempts=session.get('attempts', 0))