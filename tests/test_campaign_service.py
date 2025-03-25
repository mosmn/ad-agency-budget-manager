from src.models.brand import Brand
from src.models.campaign import Campaign
from src.services.budget_service import BudgetService
from src.services.campaign_service import CampaignService
import unittest
from unittest.mock import patch
from datetime import datetime

class TestCampaignService(unittest.TestCase):

    def setUp(self):
        self.brand = Brand(name="Test Brand", daily_budget=100, monthly_budget=3000)
        self.campaign = Campaign(name="Test Campaign", dayparting_hours=[(9, 17)])  # 9 AM to 5 PM
        self.campaign_service = CampaignService()

    def test_activate_campaign_within_dayparting(self):
        self.campaign_service.activate_campaign(self.campaign, self.brand)
        self.assertTrue(self.campaign.is_active)

    @patch('src.utils.date_utils.datetime')
    def test_deactivate_campaign_outside_dayparting(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 1, 18, 0)  # 6 PM
        self.campaign_service.activate_campaign(self.campaign, self.brand)
        self.campaign_service.check_dayparting(self.campaign)
        self.assertFalse(self.campaign.is_active)

    def test_deactivate_campaign_when_budget_exceeded(self):
        self.brand.current_daily_spend = 100  # Simulate daily budget reached
        self.campaign_service.activate_campaign(self.campaign, self.brand)
        self.campaign_service.check_budget(self.campaign, self.brand)
        self.assertFalse(self.campaign.is_active)

    def test_reactivate_campaign_next_day(self):
        self.brand.current_daily_spend = 0  # Reset for new day
        self.campaign_service.activate_campaign(self.campaign, self.brand)
        self.assertTrue(self.campaign.is_active)

    def test_campaign_dayparting(self):
        self.campaign_service.activate_campaign(self.campaign, self.brand)
        self.assertTrue(self.campaign.is_active)
        self.campaign_service.check_dayparting(self.campaign)
        self.assertTrue(self.campaign.is_active)  # Should still be active within dayparting

if __name__ == '__main__':
    unittest.main()