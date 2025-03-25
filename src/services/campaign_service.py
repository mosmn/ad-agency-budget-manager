class CampaignService:
    def __init__(self, brand):
        self.brand = brand

    def activate_campaigns(self, current_time):
        for campaign in self.brand.campaigns:
            if campaign.is_within_dayparting(current_time) and not self.brand.check_daily_budget() and not self.brand.check_monthly_budget():
                campaign.activate()
            else:
                campaign.deactivate()

    def deactivate_campaigns(self):
        for campaign in self.brand.campaigns:
            campaign.deactivate()