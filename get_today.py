from datetime import datetime

def get_today():
    return int(str(datetime.now())[0:10].replace('-',''))