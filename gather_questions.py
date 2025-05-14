from load_questions import load_questions
from datetime import datetime

def gather_questions(num_questions, perennial, live):
    questions, df = load_questions(num_questions, perennial = perennial, live = live)
    if questions is None:
        print("No live unforecasted questions available at", str(datetime.now()))
        return None, None
    else:
        print("Got", len(questions), "questions")
    return questions, df
