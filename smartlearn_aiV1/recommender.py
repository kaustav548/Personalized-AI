content_bank = {
    "Fractions": {
        "Easy": [
            "Visual fraction introduction",
            "Basic fraction addition"
        ],
        "Medium": [
            "Fraction addition",
            "Fraction subtraction"
        ],
        "Hard": [
            "Word problems",
            "Real-life fraction applications"
        ]
    }
}

def recommend(topic, difficulty):
    return content_bank[topic][difficulty]
