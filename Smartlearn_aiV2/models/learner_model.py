import numpy as np

class LearnerModel:
    def __init__(self):
        self.accuracy_history = []
        self.time_history = []
        self.hint_history = []
        self.concept_scores = []

        self.recent_results = []   # sliding window
        self.proficiency = "medium"

    def initialize_from_kaggle(self, kaggle_row):
        self.accuracy_history.append(kaggle_row["answered_correctly"])
        self.time_history.append(kaggle_row["prior_question_elapsed_time"])
        self.hint_history.append(
            1 if kaggle_row["prior_question_had_explanation"] else 0
        )

    def update(self, result):
        """
        result = {
            correct: 0/1
            time_taken: seconds
            hint_used: bool
            conceptual_score: float
        }
        """

        # ✅ Track ALL signals
        self.accuracy_history.append(result["correct"])
        self.time_history.append(result.get("time_taken", 100))
        self.hint_history.append(1 if result.get("hint_used", False) else 0)
        self.concept_scores.append(result["conceptual_score"])

        # Sliding window for stability
        self.recent_results.append(result["correct"])
        if len(self.recent_results) > 5:
            self.recent_results.pop(0)

        self._update_proficiency()

    def _update_proficiency(self):
        """
        Slow, stable proficiency update
        """
        if len(self.recent_results) < 3:
            return

        avg = np.mean(self.recent_results)

        if avg >= 0.75:
            self.proficiency = "high"
        elif avg >= 0.45:
            self.proficiency = "medium"
        else:
            self.proficiency = "low"

    def get_state(self):
        accuracy = (
            np.mean(self.accuracy_history[-5:])
            if self.accuracy_history else 0.5
        )

        avg_time = (
            np.mean(self.time_history[-5:])
            if self.time_history else 100
        )

        hint_rate = (
            np.mean(self.hint_history[-5:])
            if self.hint_history else 0.5
        )

        return {
            "proficiency": self.proficiency,
            "accuracy": round(float(accuracy), 3),
            "avg_time": round(float(avg_time), 1),
            "hint_rate": round(float(hint_rate), 3)
        }
