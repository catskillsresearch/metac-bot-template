def get_period_type(ifp):
    title = ifp['title']
    if 'ending value' in title:
        return 'last day of biweekly period'
    elif 'return' in title:
        return 'return on last vs first day of biweekly period'
    elif 'biweekly' in title:
        return 'any day in biweekly period'
    elif 'after' in title:
        return 'next SEC filing date'
    elif 'before' in title:
        return 'question end date'
    else:
        raise Exception('unknown period type: ' + title)