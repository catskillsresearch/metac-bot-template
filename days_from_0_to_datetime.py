from datetime import datetime, timedelta

def days_from_0_to_datetime(day):
    ## Dates expressed as offsets from Unix day 0
    seconds_per_day =  86400
    days_in_s = (day-1) * seconds_per_day
    dt = datetime.fromtimestamp(days_in_s)-timedelta(hours=19)
    idt = int(str(dt)[0:10].replace('-',''))
    return idt

if __name__=="__main__":
    # should map 20104 to Jan. 14, 2025 and 20454 to Dec. 30, 2025. 
    print([(x, days_from_0_to_datetime(x)) for x in [20104, 20454]])