from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from problems.problem_generator import generate_problem
from models.plm_evaluator import evaluate_explanation
from models.rl_agent import RLAgent
from utils.reward import compute_reward
from utils.csv_db import init_csv, log_interaction
import ast

# Shared learner instance
from models.shared_state import learner

student_bp = Blueprint("student", __name__)
init_csv()

rl_agent = RLAgent()

# Cold start
learner.initialize_from_kaggle({
    "answered_correctly": 1,
    "prior_question_elapsed_time": 95,
    "prior_question_had_explanation": False
})


# -----------------------------
# DASHBOARD
# -----------------------------
@student_bp.route("/dashboard", methods=["GET"])
def dashboard():
    if session.get("role") != "student":
        return redirect(url_for("auth.login_page"))

    return render_template(
        "student_dashboard.html",
        proficiency=learner.proficiency
    )


# -----------------------------
# GET PROBLEM (MCQ)
# -----------------------------
@student_bp.route("/get_problem", methods=["POST"])
def get_problem():
    if session.get("role") != "student":
        return redirect(url_for("auth.login_page"))

    state = learner.get_state()
    action = rl_agent.select_action(state)

    problem = generate_problem(action)
    problem["action"] = action

    return jsonify(problem)


# -----------------------------
# SUBMIT MCQ SOLUTION
# -----------------------------
@student_bp.route("/submit", methods=["POST"])
def submit_solution():
    if session.get("role") != "student":
        return redirect(url_for("auth.login_page"))

    # MCQ inputs
    selected_option = int(request.form.get("selected_option"))
    correct_option = int(request.form.get("correct_option"))

    explanation = request.form.get("explanation", "")
    action = ast.literal_eval(request.form.get("action"))
    difficulty = request.form.get("difficulty")

    # ---------- Correctness ----------
    correct = 1 if selected_option == correct_option else 0

    # ---------- PLM Evaluation (optional explanation) ----------
    plm_result = evaluate_explanation(
        student_text=explanation,
        expected_steps=["basis", "assumptions", "balance"]
    )

    result = {
        "correct": correct,
        "time_taken": 60,
        "hint_used": False,
        "conceptual_score": plm_result["conceptual_score"],
        "difficulty": difficulty
    }

    prev_state = learner.get_state()

    # ---------- Learner Update ----------
    learner.update(result)

    # ---------- Reward ----------
    reward = compute_reward(result)

    # ---------- RL Update ----------
    rl_agent.update(
        prev_student_data=prev_state,
        action=tuple(action),
        reward=reward,
        new_student_data=learner.get_state()
    )

    # ---------- Logging ----------
    log_interaction(result, learner, reward)

    # ---------- NEXT QUESTION (PURE RL) ----------
    next_action = rl_agent.select_action(learner.get_state())
    next_problem = generate_problem(next_action)
    next_problem["action"] = next_action

    return jsonify({
        "feedback": {
            "correct": bool(correct),
            "conceptual_score": plm_result["conceptual_score"],
            "errors": plm_result["errors"],
            "message": plm_result["feedback"]
        },
        "performance": {
            "reward": reward,
            "proficiency": learner.proficiency,
            "state": learner.get_state()
        },
        "next_question": {
            "action": next_action,
            "problem_type": next_problem["problem_type"],
            "difficulty": next_problem["difficulty"],
            "question": next_problem["question"],
            "options": next_problem["options"],
            "correct_option": next_problem["correct_option"]
        }
    })
