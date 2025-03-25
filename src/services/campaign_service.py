class CampaignService:
    def __init__(self):
        self.campaigns = []

    def add_campaign(self, campaign):
        self.campaigns.append(campaign)

    def activate_campaign(self, campaign):
        if self.is_within_dayparting(campaign):
            campaign.status = 'active'

    def deactivate_campaign(self, campaign):
        campaign.status = 'inactive'

    def manage_campaigns(self):
        for campaign in self.campaigns:
            if campaign.is_budget_exceeded():
                self.deactivate_campaign(campaign)
            else:
                self.activate_campaign(campaign)

    def is_within_dayparting(self, campaign):
        current_time = self.get_current_time()
        return campaign.start_hour <= current_time.hour < campaign.end_hour

    def get_current_time(self):
        from datetime import datetime
        return datetime.now()