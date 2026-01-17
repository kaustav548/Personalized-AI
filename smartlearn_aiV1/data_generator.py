import pandas as pd
import random

students = [f"S{i:03d}" for i in range(1, 101)]
topics = ["Fractions"]

data = []

for student in students:
    skill = random.choice(["low", "medium", "high"])

    for q in range(1, 21):
        if skill == "low":
            correct = random.choices([0, 1], [0.7, 0.3])[0]
            time_spent = random.randint(60, 120)
            attempts = random.randint(2, 4)
            hints = random.randint(1, 3)
        elif skill == "medium":
            correct = random.choices([0, 1], [0.4, 0.6])[0]
            time_spent = random.randint(40, 80)
            attempts = random.randint(1, 3)
            hints = random.randint(0, 2)
        else:
            correct = random.choices([0, 1], [0.2, 0.8])[0]
            time_spent = random.randint(20, 50)
            attempts = random.randint(1, 2)
            hints = random.randint(0, 1)

        data.append([
            student,
            "Fractions",
            f"Q{q}",
            correct,
            time_spent,
            attempts,
            hints
        ])

df = pd.DataFrame(data, columns=[
    "student_id", "topic", "question_id",
    "correct", "time_spent", "attempts", "hints_used"
])

df.to_csv("data/student_interactions.csv", index=False)
print("Dataset generated successfully.")
