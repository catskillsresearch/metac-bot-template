from forecasting_tools import MetaculusApi

# List of Metaculus question IDs you want to fetch
question_ids = [578, 14333, 22427]

# Fetch questions by ID
questions = [MetaculusApi.get_question_by_id(qid) for qid in question_ids]

print(questions[0])
