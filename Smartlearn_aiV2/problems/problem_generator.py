import random

# -----------------------------
# MCQ TEMPLATES (CONCEPT LEVEL)
# -----------------------------

SINGLE_UNIT_TEMPLATES = {
    "easy": [
        {
            "stem": "Which is the most appropriate basis for a steady-state mixer with continuous flow?",
            "options": [
                "Energy supplied per hour",
                "Mass or molar flow rate",
                "Volume of the equipment",
                "Operating pressure"
            ],
            "answer": 1,
            "concept": "basis"
        }
    ],
    "medium": [
        {
            "stem": "For a steady-state reactor, which assumption is required to write a mass balance?",
            "options": [
                "No reaction occurs",
                "No accumulation of mass",
                "Constant temperature",
                "Equal inlet and outlet flow rates"
            ],
            "answer": 1,
            "concept": "assumptions"
        }
    ],
    "hard": [
        {
            "stem": "A steady-state unit has multiple inlet and outlet streams. Which balance must always be satisfied?",
            "options": [
                "Energy balance only",
                "Component balance only",
                "Overall mass balance",
                "Entropy balance"
            ],
            "answer": 2,
            "concept": "mass_balance"
        }
    ]
}

RECYCLE_TEMPLATES = {
    "easy": [
        {
            "stem": "What is the primary purpose of introducing a recycle stream in a process?",
            "options": [
                "Increase equipment size",
                "Reuse unreacted material",
                "Reduce system pressure",
                "Eliminate the need for separation"
            ],
            "answer": 1,
            "concept": "recycle"
        }
    ],
    "medium": [
        {
            "stem": "In a recycle process operating at steady state, which stream affects overall conversion most?",
            "options": [
                "Fresh feed",
                "Recycle stream",
                "Product stream",
                "Purge stream"
            ],
            "answer": 1,
            "concept": "recycle"
        }
    ],
    "hard": [
        {
            "stem": "Why is a purge stream required in systems with recycle?",
            "options": [
                "To increase recycle flow",
                "To prevent accumulation of inert components",
                "To reduce heat loss",
                "To maintain steady state"
            ],
            "answer": 1,
            "concept": "purge"
        }
    ]
}

ENERGY_BALANCE_TEMPLATES = {
    "easy": [
        {
            "stem": "Which term is included in a steady-state energy balance?",
            "options": [
                "Energy accumulation",
                "Heat transfer",
                "Entropy generation",
                "Mass generation"
            ],
            "answer": 1,
            "concept": "energy_balance"
        }
    ],
    "medium": [
        {
            "stem": "For a steady-state heat exchanger, which assumption is commonly made?",
            "options": [
                "No heat transfer",
                "No work interaction",
                "No mass flow",
                "No energy balance required"
            ],
            "answer": 1,
            "concept": "energy_balance"
        }
    ],
    "hard": [
        {
            "stem": "Which additional term must be considered if a heat exchanger loses heat to surroundings?",
            "options": [
                "Work done",
                "Heat loss term",
                "Mass accumulation",
                "Chemical reaction term"
            ],
            "answer": 1,
            "concept": "heat_loss"
        }
    ]
}

MULTI_UNIT_TEMPLATES = {
    "easy": [
        {
            "stem": "What is the first step in solving a multi-unit process problem?",
            "options": [
                "Write energy balances",
                "Identify units and streams",
                "Solve equations",
                "Assume conversions"
            ],
            "answer": 1,
            "concept": "process_analysis"
        }
    ],
    "medium": [
        {
            "stem": "Why are balances often written unit-by-unit in a multi-unit process?",
            "options": [
                "To simplify calculations",
                "To avoid assumptions",
                "To eliminate recycle",
                "To reduce variables"
            ],
            "answer": 0,
            "concept": "multi_unit_balance"
        }
    ],
    "hard": [
        {
            "stem": "In a coupled multi-unit system, what is the main challenge?",
            "options": [
                "Identifying units",
                "Handling interdependent streams",
                "Choosing basis",
                "Writing assumptions"
            ],
            "answer": 1,
            "concept": "coupled_systems"
        }
    ]
}


# --------------------------------
# MAIN GENERATOR (PURE RL FRIENDLY)
# --------------------------------

def generate_problem(action):
    """
    action = (problem_type, difficulty)
    """

    problem_type, difficulty = action

    if problem_type == "single_unit":
        template = random.choice(SINGLE_UNIT_TEMPLATES[difficulty])

    elif problem_type == "recycle":
        template = random.choice(RECYCLE_TEMPLATES[difficulty])

    elif problem_type == "energy_balance":
        template = random.choice(ENERGY_BALANCE_TEMPLATES[difficulty])

    elif problem_type == "multi_unit":
        template = random.choice(MULTI_UNIT_TEMPLATES[difficulty])

    else:
        # fallback (should never happen)
        template = random.choice(SINGLE_UNIT_TEMPLATES["easy"])

    return {
        "problem_type": problem_type,
        "difficulty": difficulty,
        "question": template["stem"],
        "options": template["options"],
        "correct_option": template["answer"],
        "concepts": [template["concept"]]
    }
