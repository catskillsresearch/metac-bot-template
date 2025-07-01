from extract_forecast import *

def make_median_forecast(question_type, prompt2, model):

    from call_local_llm import call_local_llm
    a_1 = call_local_llm(prompt2, model)
    a_2 = call_local_llm(prompt2, model)
    a_3 = call_local_llm(prompt2, model)
    answers = [a_1, a_2, a_3]
 
    if question_type == 'binary':
        forecasts = [extract_probability_from_response_as_percentage_not_decimal(x)/100.0 for x in answers]
        import numpy as np
        forecast = float(np.median(forecasts))
    else:
        from median_dictionaries import median_dictionaries
        if question_type == 'multiple_choice':
            forecasts = [generate_multiple_choice_forecast(options,extract_option_probabilities_from_response(x, options))
                         for x in answers]
        elif question_type == 'numeric':
            forecasts = [extract_percentile_numbers(x) for x in [answer_mistral, answer_mistral2, answer_mistral3]]
        else:
            raise "unknown question type"

        forecast = median_dictionaries(forecasts)

    from make_rationale import make_rationale
    rationale = make_rationale(forecast, answers, model)
    
    return forecast, rationale
