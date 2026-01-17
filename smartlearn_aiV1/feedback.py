def generate_feedback(correct, learner_type):
    if correct:
        if learner_type == "Advanced":
            return "Excellent! Try a more challenging problem."
        return "Good job! Keep going."

    if learner_type == "Struggling":
        return "Let’s slow down. Focus on matching denominators first."
    elif learner_type == "Average":
        return "You’re close. Re-check your steps."
    else:
        return "Interesting mistake. Try solving it differently."
