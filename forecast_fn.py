import os

def forecast_fn(row):
    dfn = f'glimt/forecast/{row['forecast_date']}/{row['platform']}'
    os.makedirs(dfn, exist_ok=True)
    fn = f"{dfn}/{row['id_of_question']}.json"
    return fn