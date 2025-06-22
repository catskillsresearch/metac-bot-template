import forecasting_tools
from extract_forecast import *

def extract_only_forecast(id_to_question, forecasts, id):
    question = id_to_question[id]
    question_type = type(question)
    forecast = forecasts[id]
    if question_type == forecasting_tools.data_models.questions.BinaryQuestion:
        prediction = extract_probability_from_response_as_percentage_not_decimal(forecast)/100.0
    elif question_type == forecasting_tools.data_models.questions.MultipleChoiceQuestion:
        options = question.options
        option_probabilities = extract_option_probabilities_from_response(forecast, options)
        prediction = generate_multiple_choice_forecast(options, option_probabilities)
    elif question_type == forecasting_tools.data_models.questions.NumericQuestion:
        prediction = extract_percentile_numbers(forecast)
    return prediction