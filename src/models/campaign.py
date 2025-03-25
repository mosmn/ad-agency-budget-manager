class Campaign:
    def __init__(self, name, dayparting_hours=None):
        self.name = name
        self.is_active = False
        self.dayparting_hours = dayparting_hours if dayparting_hours else []
    
    def activate(self):
        self.is_active = True
    
    def deactivate(self):
        self.is_active = False
    
    def is_within_dayparting(self, current_time):
        for start, end in self.dayparting_hours:
            if start <= current_time <= end:
                return True
        return False
    
    def check_and_update_status(self, current_time):
        if self.is_within_dayparting(current_time):
            self.activate()
        else:
            self.deactivate()