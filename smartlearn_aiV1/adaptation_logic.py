def adapt_learning(learner_type):
    if learner_type == "Struggling":
        return {
            "difficulty": "Easy",
            "format": "Visual + Step-by-Step",
            "hints": True
        }
    elif learner_type == "Advanced":
        return {
            "difficulty": "Hard",
            "format": "Challenge Problems",
            "hints": False
        }
    else:
        return {
            "difficulty": "Medium",
            "format": "Standard Practice",
            "hints": True
        }
