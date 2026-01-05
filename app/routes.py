from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify  # type: ignore
from app.services.scenario_loader import ScenarioLoader  # type: ignore
from app.services.logic_engine import LogicEngine  # type: ignore

bp = Blueprint('main', __name__)

def get_scenario_hint(scenario):
    """
    Helper method to extract hint from scenario data.
    Checks both 'solution.hint' and root 'hint'.
    """
    return scenario.get('solution', {}).get('hint') or scenario.get('hint') or "Hint: Review the statements carefully."

def get_levels():
    """Helper to get list of levels with titles."""
    loader = ScenarioLoader()
    levels = []
    for i in range(1, 11):
        scenario = loader.load_scenario(f"scenario_{i}.json")
        title = scenario.get('title', 'Locked') if scenario else "Locked"
        levels.append({'id': i, 'title': title})
    return levels

@bp.route('/complete')
def complete():
    """
    Displays the completion screen after all levels are finished.
    """
    return render_template('completion.html')

@bp.route('/')
def index():
    """
    Landing page with game rules and scenario selection.
    """
    return render_template('index.html', levels=get_levels())

@bp.route('/scenario/<scenario_id>', methods=['GET', 'POST'])
def play_scenario(scenario_id):
    """
    Main game interface.
    Loads the scenario and handles user submissions.
    """
    # Try to parse scenario_id as int, otherwise keep as string
    try:
        scenario_id_int = int(scenario_id)
        load_id = scenario_id_int
    except ValueError:
        scenario_id_int = None
        load_id = scenario_id

    loader = ScenarioLoader()
    scenario = loader.load_scenario(f"scenario_{load_id}.json")

    if not scenario:
        return "System Error: Scenario data could not be loaded.", 500

    # Session key for tracking attempts on this specific scenario
    attempt_key = f'attempts_{load_id}'
    if attempt_key not in session:
        session[attempt_key] = 0

    if request.method == 'POST':
        selected_id = request.form.get('statement_id')
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if selected_id:
            try:
                s_id = int(selected_id)
                result = LogicEngine.evaluate(scenario, s_id)
                
                if result['success']:
                    session[attempt_key] = 0  # Reset attempts on success
                    
                    # Check if next level exists for auto-redirect
                    if scenario_id_int is not None:
                        next_id = scenario_id_int + 1
                        next_scenario = loader.load_scenario(f"scenario_{next_id}.json")
                        
                        if next_scenario:
                            msg = f"Correct! {result.get('details', '')}"
                            flash(msg, 'success')
                            
                            if is_ajax:
                                return jsonify({'success': True, 'redirect': url_for('main.play_scenario', scenario_id=next_id)})
                            return redirect(url_for('main.play_scenario', scenario_id=next_id))
                    
                    # Game Complete or Non-integer ID finished: Redirect to completion page
                    flash(f"Correct! {result.get('details', '')}", 'success')
                    
                    if is_ajax:
                        return jsonify({'success': True, 'redirect': url_for('main.complete')})
                    
                    return redirect(url_for('main.complete'))
                else:
                    session[attempt_key] += 1
                    
                    # Calculate hint text using the new method
                    hint_text = None
                    if session[attempt_key] >= 2:
                        hint_text = get_scenario_hint(scenario)
                        print(f"DEBUG: Hint triggered for Level {load_id}. Text: {hint_text}")

                    if is_ajax:
                        response_data = {'success': False, 'message': result['message']}
                        if hint_text:
                            response_data['show_hint'] = True
                            response_data['hint_text'] = hint_text
                        return jsonify(response_data)
                    
                    flash(result['message'], 'danger')
                    # Force hint display via flash message as a fallback
                    if hint_text:
                        flash(f"💡 Hint: {hint_text}", 'warning')
            except Exception as e:
                # Catch ALL errors to prevent 500 crash and refresh
                if is_ajax:
                    return jsonify({'success': False, 'message': f"System Error: {str(e)}"})
                flash(f"System Error: {str(e)}", 'danger')
        else:
            if is_ajax:
                return jsonify({'success': False, 'message': "Please select a statement."})
            flash("Please select a statement.", 'warning')

    # Check if hint should be shown
    show_hint = False
    hint_text = ""
    if session.get(attempt_key, 0) >= 2:
        show_hint = True
        hint_text = get_scenario_hint(scenario)

    # Check if next level exists
    has_next_level = False
    next_id = None
    if scenario_id_int is not None:
        next_id = scenario_id_int + 1
        has_next_level = loader.load_scenario(f"scenario_{next_id}.json") is not None

    return render_template('index.html', scenario=scenario, show_hint=show_hint, hint_text=hint_text, next_id=next_id, has_next_level=has_next_level, current_id=load_id, levels=get_levels())