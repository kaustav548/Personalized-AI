import numpy as np
import matplotlib.pyplot as plt

# Import the shared learner model (real model state)
from models.shared_state import learner


def evaluate_model():
    """
    Computes all evaluation metrics and generates graphs
    using the real learner model (no hard-coded values).
    """

    # =========================
    # SAFETY CHECK
    # =========================
    if len(learner.accuracy_history) < 2:
        raise ValueError(
            "Not enough learner data. Run student interactions first."
        )

    # =========================
    # DATA EXTRACTION
    # =========================
    accuracy = np.array(learner.accuracy_history)
    concept_scores = np.array(learner.concept_scores)
    hint_history = np.array(learner.hint_history)
    time_history = np.array(learner.time_history)

    attempts = np.arange(len(accuracy))

    # =========================
    # 1️⃣ ACCURACY METRICS
    # =========================
    mean_accuracy = accuracy.mean()
    final_accuracy = accuracy[-1]
    accuracy_gain = final_accuracy - accuracy[0]

    # =========================
    # 2️⃣ NORMALIZED LEARNING GAIN
    # =========================
    learning_gain = (final_accuracy - accuracy[0]) / (1 - accuracy[0])

    # =========================
    # 3️⃣ CONVERGENCE RATE
    # =========================
    convergence_rate = np.polyfit(attempts, accuracy, 1)[0]

    # =========================
    # 4️⃣ CONCEPTUAL UNDERSTANDING
    # =========================
    mean_concept_score = concept_scores.mean() if len(concept_scores) else 0
    recent_concept_score = (
        concept_scores[-5:].mean() if len(concept_scores) >= 5 else mean_concept_score
    )

    # =========================
    # 5️⃣ HINT DEPENDENCY REDUCTION
    # =========================
    hint_initial = hint_history[:5].mean()
    hint_final = hint_history[-5:].mean()
    hint_reduction = hint_initial - hint_final

    # =========================
    # 6️⃣ TIME EFFICIENCY IMPROVEMENT
    # =========================
    time_initial = time_history[:5].mean()
    time_final = time_history[-5:].mean()
    time_improvement = time_initial - time_final

    # =========================
    # 7️⃣ RISK LEVEL
    # =========================
    if mean_accuracy < 0.5:
        risk_level = "High"
    elif mean_accuracy < 0.7:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # =========================
    # PRINT METRICS (FOR REPORT)
    # =========================
    print("\n===== MODEL EVALUATION RESULTS =====")
    print(f"Mean Accuracy           : {mean_accuracy:.3f}")
    print(f"Final Accuracy          : {final_accuracy:.3f}")
    print(f"Accuracy Gain           : {accuracy_gain:.3f}")
    print(f"Learning Gain           : {learning_gain:.3f}")
    print(f"Convergence Rate        : {convergence_rate:.4f}")
    print(f"Mean Concept Score      : {mean_concept_score:.3f}")
    print(f"Recent Concept Score    : {recent_concept_score:.3f}")
    print(f"Hint Reduction          : {hint_reduction:.3f}")
    print(f"Time Improvement (sec)  : {time_improvement:.2f}")
    print(f"Risk Level              : {risk_level}")
    print(f"Final Proficiency Level : {learner.proficiency}")

    # =========================
    # 📊 GRAPHS
    # =========================

    # Accuracy Progression
    plt.figure()
    plt.plot(accuracy)
    plt.xlabel("Attempt")
    plt.ylabel("Accuracy")
    plt.title("Learner Accuracy Progression")
    plt.show()

    # Conceptual Understanding
    if len(concept_scores):
        plt.figure()
        plt.plot(concept_scores)
        plt.xlabel("Attempt")
        plt.ylabel("Conceptual Score")
        plt.title("PLM-Based Conceptual Understanding")
        plt.show()

    # Hint Dependency
    plt.figure()
    plt.plot(hint_history)
    plt.xlabel("Attempt")
    plt.ylabel("Hint Used (0/1)")
    plt.title("Hint Dependency Trend")
    plt.show()

    # Time Efficiency
    plt.figure()
    plt.plot(time_history)
    plt.xlabel("Attempt")
    plt.ylabel("Time Taken (seconds)")
    plt.title("Time Efficiency Improvement")
    plt.show()


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    evaluate_model()
