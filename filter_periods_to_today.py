from datetime import datetime

def filter_periods_to_today(periods):
    today = int(str(datetime.now())[0:10].replace('-',''))
    filtered = []
    rejected = []
    for label, start, end in periods:
        if end < today:
            rejected.append(0.0)
            continue
        if start < today:
            start = today
        filtered.append((label, start, end))
    
    return rejected, filtered