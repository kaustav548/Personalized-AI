import pandas as pd

"""
KaggleDatasetLoader is used for offline learner simulation,
cold-start initialization, and experimental evaluation.
"""

class KaggleDatasetLoader:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.data = None

    def load(self):
        self.data = pd.read_csv(self.dataset_path)
        return self.data

    def preprocess(self):
        if self.data is None:
            raise ValueError("Dataset not loaded")

        processed = []

        for _, row in self.data.iterrows():
            record = {
                "answered_correctly": int(row.get("answered_correctly", 0)),
                "prior_question_elapsed_time": (
                    row.get("prior_question_elapsed_time", 100)
                    if pd.notna(row.get("prior_question_elapsed_time", None))
                    else 100
                ),
                "prior_question_had_explanation": bool(
                    row.get("prior_question_had_explanation", False)
                )
            }
            processed.append(record)

        return processed

    def sample_learners(self, n=1):
        processed_data = self.preprocess()

        learners = []
        chunk_size = max(1, len(processed_data) // n)

        for i in range(n):
            learners.append(
                processed_data[i * chunk_size : (i + 1) * chunk_size]
            )

        return learners
