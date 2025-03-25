class BudgetService:
    def __init__(self, brand):
        self.brand = brand

    def update_daily_spend(self, amount):
        self.brand.current_daily_spend += amount
        if self.brand.check_daily_budget():
            self.deactivate_campaigns()

    def update_monthly_spend(self, amount):
        self.brand.current_monthly_spend += amount
        if self.brand.check_monthly_budget():
            self.deactivate_campaigns()

    def deactivate_campaigns(self):
        for campaign in self.brand.campaigns:
            campaign.deactivate()