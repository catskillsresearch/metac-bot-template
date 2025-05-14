from post_forecast import post_forecast

def post_forecasts(df, perennial, live):
    if perennial or live:
        df.apply(post_forecast, axis=1)
    if live:
        return df[['title', 'question_type', 'prediction']]
    else:
        return df[['title', 'question_type', 'prediction', 'crowd', 'error']]
