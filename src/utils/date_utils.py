def is_within_dayparting(start_hour, end_hour):
    from datetime import datetime
    
    current_time = datetime.now().time()
    return start_hour <= current_time <= end_hour

def get_current_date():
    from datetime import datetime
    
    return datetime.now().date()

def get_current_time():
    from datetime import datetime
    
    return datetime.now().time()