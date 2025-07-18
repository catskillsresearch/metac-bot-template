def get_observable(ifp):
    title = ifp['title']
    if 'maximum intraday' in title:
        return 'daily High'
    elif 'ending value' in title:
        return 'last day Close'
    elif 'stock price returns' in title:
        return 'period stock price return'
    elif 'Futures total price returns' in title:
        return 'period futures total price return'
    elif 'earnings per share' in title:
        return 'quarter diluted eps'
    elif 'revenue' in title:
        return 'quarter total revenue'
    raise Exception('NIY')