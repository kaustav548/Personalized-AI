import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

df = pd.read_csv("data/student_features.csv")

X = df[["accuracy", "avg_time", "avg_attempts", "hint_rate"]]
y = df["learner_type"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = DecisionTreeClassifier(max_depth=4)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

joblib.dump(model, "learner_model.pkl")
print("Model saved successfully.")
