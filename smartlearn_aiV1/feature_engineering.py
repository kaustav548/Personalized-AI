import pandas as pd

df = pd.read_csv("data/student_interactions.csv")

features = df.groupby("student_id").agg(
    accuracy=("correct", "mean"),
    avg_time=("time_spent", "mean"),
    avg_attempts=("attempts", "mean"),
    hint_rate=("hints_used", "mean")
).reset_index()

def label_student(row):
    if row["accuracy"] < 0.4:
        return "Struggling"
    elif row["accuracy"] < 0.75:
        return "Average"
    else:
        return "Advanced"

features["learner_type"] = features.apply(label_student, axis=1)

features.to_csv("data/student_features.csv", index=False)
print("Features generated successfully.")
