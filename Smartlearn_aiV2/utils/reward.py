def compute_reward(result):
    """
    PURE RL reward shaping
    """

    correct = result.get("correct", 0)
    conceptual = result.get("conceptual_score", 0)
    time_taken = result.get("time_taken", 100)
    hint_used = result.get("hint_used", False)
    difficulty = result.get("difficulty", "medium")

    reward = 0.0

    # -----------------------------
    # Base correctness reward
    # -----------------------------
    if correct:
        reward += 2.0
    else:
        reward -= 2.0

    # -----------------------------
    # Conceptual understanding
    # -----------------------------
    reward += conceptual * 3.0

    # -----------------------------
    # Difficulty shaping (CRITICAL)
    # -----------------------------
    if difficulty == "easy":
        reward += 0.5 if correct else -0.2

    elif difficulty == "medium":
        reward += 1.0 if correct else -0.5

    elif difficulty == "hard":
        reward += 2.0 if correct else -2.0

    # -----------------------------
    # Time efficiency
    # -----------------------------
    if time_taken < 60:
        reward += 0.5
    elif time_taken > 180:
        reward -= 0.5

    # -----------------------------
    # Hint penalty
    # -----------------------------
    if hint_used:
        reward -= 0.7

    return round(reward, 3)
