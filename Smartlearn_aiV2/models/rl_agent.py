import random
import numpy as np

PROBLEM_TYPES = ["single_unit", "multi_unit", "recycle", "energy_balance"]
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]

class RLAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.3):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        # Q-table: {state: {(problem_type, difficulty): Q}}
        self.q_table = {}

    def get_state(self, student_data):
        """
        PURE RL state from learner model
        """
        proficiency = student_data["proficiency"]

        accuracy_bucket = (
            "high" if student_data["accuracy"] >= 0.7
            else "medium" if student_data["accuracy"] >= 0.4
            else "low"
        )

        hint_bucket = "high" if student_data["hint_rate"] > 0.5 else "low"

        return (proficiency, accuracy_bucket, hint_bucket)

    def _init_state(self, state):
        if state not in self.q_table:
            self.q_table[state] = {}

            # 🔥 Optimistic initialization → forces exploration
            for p in PROBLEM_TYPES:
                for d in DIFFICULTY_LEVELS:
                    self.q_table[state][(p, d)] = random.uniform(0.1, 0.3)

    def select_action(self, student_data):
        state = self.get_state(student_data)
        self._init_state(state)

        # 🔁 ε-greedy exploration
        if random.random() < self.epsilon:
            return random.choice(list(self.q_table[state].keys()))

        # 🔁 RANDOM tie-breaking among best actions
        max_q = max(self.q_table[state].values())
        best_actions = [
            a for a, q in self.q_table[state].items()
            if q == max_q
        ]

        return random.choice(best_actions)

    def update(self, prev_student_data, action, reward, new_student_data):
        prev_state = self.get_state(prev_student_data)
        new_state = self.get_state(new_student_data)

        self._init_state(prev_state)
        self._init_state(new_state)

        best_future_q = max(self.q_table[new_state].values())
        old_q = self.q_table[prev_state][action]

        # 🔥 Standard Q-learning update
        self.q_table[prev_state][action] = old_q + self.alpha * (
            reward + self.gamma * best_future_q - old_q
        )
