import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None) 

def add_category_to_markets(markets, field = 'name'):
    df_markets = pd.DataFrame(markets).sort_values(by='conid')
    df_markets.loc[df_markets[field].apply(lambda x: 'rimary' in x or 'lection' in x or 'Race Outcome' in x or 'President' in x or 'overnor' in x or 'andidate' in x), 'category'] = 'Election'
    df_markets.loc[df_markets[field].apply(lambda x: 'Forecast' in x or 'Index' in x), 'category'] = 'Index'
    df_markets.loc[df_markets[field].apply(lambda x: 'Exchange Rate' in x ), 'category'] = 'FX'
    df_markets.loc[df_markets[field].apply(lambda x: 'Shutdown' in x or 'Drought' in x or 'Decision' in x or 'Recession' in x or 'Sovereignty Transfer ' in x or 'Winner' in x), 'category'] = 'Event'
    df_markets.loc[df_markets[field].str.endswith(' Price') & df_markets[field].apply(lambda name: len(name.split(' ')) == 2) & df_markets['category'].isna(), 'category'] = 'Crypto'
    df_markets.loc[df_markets['category'].isna() & df_markets.name.str.contains('Rate'), 'category'] = 'Rates'
    df_markets.loc[df_markets['category'].isna() & df_markets.name.apply(lambda x: 'Electric' in x or 'Coal' in x or 'Gas' in x), 'category'] = 'Energy'
    df_markets.loc[df_markets['category'].isna() & df_markets.name.apply(lambda x: 'Carbon' in x or 'Temperature' in x or 'Hurricane' in x or 'storm' in x or 'Sea Level' in x or 'Tornado' in x), 'category'] = 'Climate'
    df_markets.loc[df_markets['category'].isna() & df_markets.name.apply(lambda x: 'Crop ' in x ), 'category'] = 'Climate'
    df_markets.loc[df_markets['category'].isna() , 'category'] = 'Macro'
    return df_markets