from flask import Blueprint, render_template, request, flash  # type: ignore
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

    if request.method == 'POST':
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
                    flash(result['message'], 'danger')
            except ValueError:
                flash("Invalid input detected.", 'warning')
        else:
            flash("Please select a statement.", 'warning')

    return render_template('scenario.html', scenario=scenario)