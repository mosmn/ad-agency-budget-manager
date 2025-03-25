class Brand:
    def __init__(self, name, monthly_budget, daily_budget):
        self.name = name
        self.monthly_budget = monthly_budget
        self.daily_budget = daily_budget
        self.current_monthly_spend = 0
        self.current_daily_spend = 0
        self.is_active = True

    def check_daily_budget_exceeded(self):
        return self.current_daily_spend >= self.daily_budget

    def check_monthly_budget_exceeded(self):
        return self.current_monthly_spend >= self.monthly_budget

    def reset_daily_budget(self):
        self.current_daily_spend = 0

    def reset_monthly_budget(self):
        self.current_monthly_spend = 0

    def add_daily_spend(self, amount):
        self.current_daily_spend += amount
        if self.check_daily_budget_exceeded():
            self.is_active = False

    def add_monthly_spend(self, amount):
        self.current_monthly_spend += amount
        if self.check_monthly_budget_exceeded():
            self.is_active = False

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False