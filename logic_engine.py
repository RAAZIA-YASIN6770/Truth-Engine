class LogicEngine:
    def evaluate(self, selection, scenario):
        """
        Evaluates if the user selection matches the correct answer in the scenario.
        """
        return selection == scenario.get('correct_answer')