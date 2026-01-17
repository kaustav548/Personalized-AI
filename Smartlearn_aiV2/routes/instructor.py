from flask import Blueprint, jsonify
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from flask import session
from flask import session, render_template, redirect, url_for


# Import learner model instance
from models.shared_state import learner

instructor_bp = Blueprint("instructor", __name__)

@instructor_bp.route("/progress", methods=["GET"])
def learning_progress():
    if session.get("role") != "instructor":
        return redirect(url_for("auth.login_page"))

    """
    Visualizes learner accuracy trend over time
    """

    acc = learner.accuracy_history

    if not acc:
        return jsonify({"message": "No learner data available yet"}), 400

    plt.figure()
    plt.plot(acc)
    plt.xlabel("Attempt")
    plt.ylabel("Accuracy")
    plt.title("Student Learning Progress")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    return jsonify({"plot": img_base64})


@instructor_bp.route("/concepts", methods=["GET"])
def concept_analysis():
    if session.get("role") != "instructor":
        return redirect(url_for("auth.login_page"))

    """
    Provides conceptual mastery based on PLM scores
    """

    scores = learner.concept_scores

    if not scores:
        return jsonify({"message": "No concept evaluation data yet"}), 400

    concept_mastery = {
        "overall_conceptual_score": round(float(np.mean(scores)), 3),
        "recent_conceptual_score": round(float(np.mean(scores[-5:])), 3)
    }

    return jsonify({
        "concept_mastery": concept_mastery,
        "proficiency_level": learner.proficiency
    })


@instructor_bp.route("/risk", methods=["GET"])
def risk_detection():
    if session.get("role") != "instructor":
        return redirect(url_for("auth.login_page"))

    """
    Detects learner risk level based on recent performance
    """

    acc = learner.accuracy_history

    if not acc:
        return jsonify({"risk_level": "Unknown"}), 400

    avg_accuracy = np.mean(acc[-5:])

    if avg_accuracy < 0.5:
        risk = "High"
    elif avg_accuracy < 0.7:
        risk = "Medium"
    else:
        risk = "Low"

    return jsonify({
        "average_accuracy": round(float(avg_accuracy), 2),
        "risk_level": risk,
        "proficiency": learner.proficiency
    })

@instructor_bp.route("/dashboard", methods=["GET"])
def dashboard():
    if session.get("role") != "instructor":
        return redirect(url_for("auth.login_page"))

    return render_template(
        "instructor_dashboard.html",
        title="Instructor Dashboard"
    )
