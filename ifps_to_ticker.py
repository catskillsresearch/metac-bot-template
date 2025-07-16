def ifps_to_ticker(urls):
    accum = []
    for url in urls:
        if 'VIX' in url:
            return [('yahoo', 'VIX')]
        elif 'stlouisfed' in url:
            return [('stlouisfed', url.split('/')[-1])]
        elif 'marketcap' in url or 'investopedia' in url or 'search-filings' in url:
            continue
        elif 'https://finance.yahoo.com/quote' in url:
            accum.append(('yahoo', url.split('/')[4:][0]))
        elif 'macrotrends' in url:
            accum.append(('macrotrends', url.split('/')[-2].upper(), url.split('/')[-1]))
        else:
            print('DK', url)
    return accum