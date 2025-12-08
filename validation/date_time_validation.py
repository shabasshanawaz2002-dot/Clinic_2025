from datetime import datetime, date, time

def validate_date(date_str: str) -> date:
    # Expecting DD/MM/YYYY
    try:
        d = datetime.strptime(date_str, "%d/%m/%Y")
        return d.date()
    except:
        raise Exception("Invalid date format. Use DD/MM/YYYY")


def validate_time(time_str: str) -> time:
    # Expecting HH:MM (24hr)
    try:
        d = datetime.strptime(time_str, "%H:%M")
        return d.time()
    except:
        raise Exception("Invalid time format. Use HH:MM (24hr)")  