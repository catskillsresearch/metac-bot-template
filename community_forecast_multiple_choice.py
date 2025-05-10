def community_forecast_multiple_choice(question):
    options = question.options
    probs = question.api_json['question']['aggregations']['recency_weighted']['latest']['forecast_values']
    return dict(zip(options, probs))