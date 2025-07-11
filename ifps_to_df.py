import pandas as pd

def ifps_to_df(ifps):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    df = pd.DataFrame([(ifp['id'], ifp['symbol'], ifp['dates']['startDay'], ifp['dates']['endDay'], 
                        ifp['props']['shortTitle']) for ifp in ifps], columns = ['id', 'challenge', 'startDay', 'endDay', 'title'])
    
    return df.sort_values(by=['challenge', 'endDay', 'title'])