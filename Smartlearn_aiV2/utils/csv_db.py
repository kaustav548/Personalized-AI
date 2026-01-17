import csv
import os
from datetime import datetime

CSV_PATH = "data/learner_logs.csv"


def init_csv():
    """
    Initialize CSV database with header if missing
    """
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "correct",
                "conceptual_score",
                "time_taken",
                "hint_used",
                "proficiency",
                "accuracy",
                "reward"
            ])


def log_interaction(result, learner, reward):
    """
    Append learner interaction to CSV
    """

    accuracy = (
        sum(learner.accuracy_history) / len(learner.accuracy_history)
        if learner.accuracy_history else 0
    )

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            int(result.get("correct", 0)),
            round(float(result.get("conceptual_score", 0)), 3),
            result.get("time_taken", 0),
            int(result.get("hint_used", False)),
            learner.proficiency,
            round(accuracy, 3),
            round(float(reward), 3)
        ])
