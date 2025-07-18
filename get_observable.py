def get_observable(ifp):
    title = ifp['title']
    if 'maximum intraday' in title:
        return 'High'
    elif 'ending value' in title:
        return 'Close'
    elif 'stock price returns' in title:
        return 'stock price Close return'
    elif 'Futures total price returns' in title:
        return 'futures total price Close return'
    elif 'earnings per share' in title:
        return 'quarter diluted eps'
    elif 'revenue' in title:
        return 'quarter total revenue'
    raise Exception('NIY')