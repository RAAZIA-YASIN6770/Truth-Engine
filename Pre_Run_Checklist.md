# Pre-Run Validation Checklist

## 1. System Requirements (SRS) Compliance
- [ ] **Logic Engine**: Verified that the engine correctly identifies true/false statements and behaves deterministically.
  - *Test Coverage*: `tests/test_evaluator.py`
- [ ] **Scenario Integrity**: Verified that scenarios must have exactly one false statement and valid schema.
  - *Test Coverage*: `tests/test_scenario_validation.py`
- [ ] **User Interface Flow**: Verified that the web controller handles submissions and resets correctly.
  - *Test Coverage*: `tests/test_routes.py`
- [ ] **Game Rules (Security)**: Verified that the "Three Strikes" rule locks the session and prevents bypass via refresh.
  - *Test Coverage*: `tests/test_attempt_limit.py`

## 2. Defect Verification
- [ ] **Unit Tests**: Run `python -m unittest discover tests` and ensure all tests pass (Green).
- [ ] **Static Analysis**: No critical Pylance/Linting errors remaining in source code.
- [ ] **Edge Cases**: Confirmed handling of empty inputs, ambiguous scenarios, and session manipulation.

## 3. Operational Safety
- [ ] **Environment**: Python 3.x installed and virtual environment active.
- [ ] **Dependencies**: Flask installed (`pip install flask`).
- [ ] **Configuration**: `SECRET_KEY` is set for session management.

## 4. Final Sign-Off
- **Status**: Ready for Implementation Phase.