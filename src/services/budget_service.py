class BudgetService:
    def __init__(self):
        self.brands = {}

    def add_brand(self, brand):
        self.brands[brand.name] = brand

    def update_daily_spend(self, brand_name, amount):
        brand = self.brands.get(brand_name)
        if brand:
            brand.current_daily_spend += amount
            self.check_daily_budget(brand)

    def update_monthly_spend(self, brand_name, amount):
        brand = self.brands.get(brand_name)
        if brand:
            brand.current_monthly_spend += amount
            self.check_monthly_budget(brand)

    def check_daily_budget(self, brand):
        if brand.current_daily_spend >= brand.daily_budget:
            brand.deactivate_campaigns()
            print(f"Daily budget exceeded for {brand.name}. Campaigns deactivated.")

    def check_monthly_budget(self, brand):
        if brand.current_monthly_spend >= brand.monthly_budget:
            brand.deactivate_campaigns()
            print(f"Monthly budget exceeded for {brand.name}. Campaigns deactivated.")

    def reset_daily_budgets(self):
        for brand in self.brands.values():
            brand.current_daily_spend = 0

    def reset_monthly_budgets(self):
        for brand in self.brands.values():
            brand.current_monthly_spend = 0

    def reset_budgets(self):
        self.reset_daily_budgets()
        self.reset_monthly_budgets()