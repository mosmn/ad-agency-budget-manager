class Brand:
    def __init__(self, name, monthly_budget, daily_budget):
        self.name = name
        self.monthly_budget = monthly_budget
        self.daily_budget = daily_budget
        self.current_monthly_spend = 0
        self.current_daily_spend = 0
        self.campaigns = []

    def add_campaign(self, campaign):
        self.campaigns.append(campaign)

    def check_monthly_budget(self):
        return self.current_monthly_spend >= self.monthly_budget

    def check_daily_budget(self):
        return self.current_daily_spend >= self.daily_budget

    def reset_daily_budget(self):
        self.current_daily_spend = 0

    def reset_monthly_budget(self):
        self.current_monthly_spend = 0