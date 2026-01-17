from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()


def get_embedding(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    token_embeddings = outputs.last_hidden_state
    attention_mask = inputs["attention_mask"].unsqueeze(-1)

    masked_embeddings = token_embeddings * attention_mask
    summed = masked_embeddings.sum(dim=1)
    counts = attention_mask.sum(dim=1)

    embeddings = summed / counts
    return embeddings.numpy()


def cosine_similarity(vec1, vec2):
    return float(
        np.dot(vec1, vec2.T) /
        (np.linalg.norm(vec1) * np.linalg.norm(vec2) + 1e-8)
    )


# Chemical Engineering specific concepts
CHEME_ERRORS = {
    "basis": ["basis", "choose", "100 kmol", "feed basis"],
    "units": ["kg", "kmol", "units", "dimension"],
    "assumptions": ["steady state", "no accumulation", "assume"],
    "stoichiometry": ["reaction", "stoichiometric", "conversion"]
}


def evaluate_explanation(student_text, expected_steps):
    """
    student_text: str
    expected_steps: list of strings
    """

    # Split student answer into sentences
    student_sentences = [
        s.strip() for s in student_text.split(".") if s.strip()
    ]

    step_scores = []

    for step in expected_steps:
        step_vec = get_embedding(step)
        sentence_scores = []

        for sent in student_sentences:
            sent_vec = get_embedding(sent)
            sim = cosine_similarity(sent_vec, step_vec)
            sentence_scores.append(sim)

        if sentence_scores:
            step_scores.append(max(sentence_scores))
        else:
            step_scores.append(0.0)

    # Base conceptual score
    conceptual_score = float(np.mean(step_scores)) if step_scores else 0.0

    # -----------------------------
    # Keyword-based conceptual boost
    # -----------------------------
    keyword_bonus = 0.0
    lower_text = student_text.lower()

    detected_errors = []

    for concept, keywords in CHEME_ERRORS.items():
        if any(k in lower_text for k in keywords):
            keyword_bonus += 0.05
        else:
            detected_errors.append(concept)

    conceptual_score = min(conceptual_score + keyword_bonus, 1.0)

    feedback = generate_feedback(detected_errors, conceptual_score)

    return {
        "conceptual_score": round(conceptual_score, 3),
        "errors": detected_errors,
        "feedback": feedback
    }


def generate_feedback(errors, score):
    if score > 0.8:
        return "Good conceptual understanding. Proceed to next level."

    messages = []

    if "basis" in errors:
        messages.append("Review basis selection before starting balances.")

    if "assumptions" in errors:
        messages.append("State all assumptions clearly (steady-state, no losses).")

    if "units" in errors:
        messages.append("Check unit consistency throughout calculations.")

    if "stoichiometry" in errors:
        messages.append("Revisit reaction stoichiometry and conversions.")

    return " ".join(messages)
