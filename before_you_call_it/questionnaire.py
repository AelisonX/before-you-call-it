"""Seven human answers, held only in memory."""
QUESTIONS = (
    ("task", "What were you trying to do?"),
    ("symptom", "What happened instead?"),
    ("error", "What did the error say? (optional)"),
    ("started", "When did this start? (just now / today / recently / after a change / not sure)"),
    ("changes", "Did anything change recently? (update / application / network / account / device / not sure)"),
    ("others", "Who else is affected? (only me / coworkers / don't know / not applicable)"),
    ("tried", "What have you already tried? (nothing yet is fine)"),
)


def ask(input_fn=input):
    return {key: input_fn(prompt + "\n> ").strip() for key, prompt in QUESTIONS}
