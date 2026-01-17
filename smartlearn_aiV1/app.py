import streamlit as st
import pandas as pd
import joblib

from adaptation_logic import adapt_learning
from recommender import recommend
from feedback import generate_feedback

st.set_page_config(page_title="SmartLearn AI", layout="centered")

model = joblib.load("learner_model.pkl")
data = pd.read_csv("data/student_features.csv")

st.title("📘 SmartLearn AI – Personalized Tutor")

student_id = st.selectbox("Select Student ID", data["student_id"].unique())

student = data[data["student_id"] == student_id]

X = student[["accuracy", "avg_time", "avg_attempts", "hint_rate"]]
learner_type = model.predict(X)[0]

st.subheader(f"👤 Learner Type: {learner_type}")

adaptation = adapt_learning(learner_type)
st.write("### 🔧 Learning Adaptation")
st.json(adaptation)

content = recommend("Fractions", adaptation["difficulty"])
st.write("### 📚 Recommended Content")
for c in content:
    st.write("-", c)

st.write("### 📝 Practice Question")
user_answer = st.number_input("What is 1/2 + 1/4 ?", step=.1,format="%.2f")
print(user_answer)
if st.button("Submit Answer"):
    correct_answer = 0.75
    correct = abs(user_answer - correct_answer) < 0.01
    feedback = generate_feedback(correct, learner_type)

    if correct:
        st.success("Correct!")
    else:
        st.error("Incorrect.")

    st.info(feedback)
