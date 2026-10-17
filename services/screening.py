"""Ranks job applicants from their CV text. Used to shortlist candidates for recruiters."""

KEYWORDS = ["python", "sql", "leadership", "degree"]


def rank_candidates(cv_text):
    text = cv_text.lower()
    score = sum(10 for word in KEYWORDS if word in text)
    return min(score, 100)
