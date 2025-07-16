def urls_to_ticker(urls):
    accum = []
    for url in urls:
        if 'VIX' in url:
            return [('yahoo', '^VIX', 'price')]
        elif 'stlouisfed' in url:
            return [('stlouisfed', url.split('/')[-1], 'series')]
        elif 'marketcap' in url or 'investopedia' in url or 'search-filings' in url:
            continue
        elif 'https://finance.yahoo.com/quote' in url:
            accum.append(('yahoo', url.split('/')[4:][0], 'price'))
        elif 'macrotrends' in url:
            accum.append(('macrotrends', url.split('/')[-2].upper(), url.split('/')[-1]))
        else:
            print('DK', url)
    subs = {'APPLE': 'AAPL',
            'AMD': 'AMD',
            'AMAZON': 'AMZN',
            'META-PLATFORMS': 'META',
            'MICROSOFT': 'MSFT',
            'NVIDIA': 'NVDA',
            'TESLA': 'TSLA'}
    accum = [(x, subs[y] if y in subs else y, z) for x,y,z in accum]
    return accum