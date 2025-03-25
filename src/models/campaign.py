class Campaign:
    def __init__(self, name, dayparting_hours):
        self.name = name
        self.is_active = False
        self.dayparting_hours = dayparting_hours

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def is_within_dayparting(self, current_time):
        start_hour, end_hour = self.dayparting_hours
        return start_hour <= current_time.hour < end_hour