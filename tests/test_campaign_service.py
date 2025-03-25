import unittest
from unittest.mock import patch
from datetime import datetime
from src.models.brand import Brand
from src.models.campaign import Campaign
from src.services.campaign_service import CampaignService


class TestCampaignService(unittest.TestCase):
    def setUp(self):
        self.brand = Brand(name="Test Brand", monthly_budget=3000, daily_budget=100)
        self.campaign1 = Campaign(name="Day Campaign", dayparting_hours=(9, 17))  # 9 AM to 5 PM
        self.campaign2 = Campaign(name="Night Campaign", dayparting_hours=(18, 23))  # 6 PM to 11 PM
        self.campaign3 = Campaign(name="All Day", dayparting_hours=(0, 24))  # 24 hours
        
        self.brand.add_campaign(self.campaign1)
        self.brand.add_campaign(self.campaign2)
        self.brand.add_campaign(self.campaign3)
        
        self.campaign_service = CampaignService(self.brand)
    
    def test_activate_campaigns_within_dayparting(self):
        # Test morning time - Day Campaign and All Day should be active
        morning_time = datetime(2023, 1, 1, 10, 0)  # 10 AM
        self.campaign_service.activate_campaigns(morning_time)
        
        self.assertTrue(self.campaign1.is_active)  # Day Campaign
        self.assertFalse(self.campaign2.is_active)  # Night Campaign
        self.assertTrue(self.campaign3.is_active)  # All Day
    
    def test_activate_campaigns_evening(self):
        # Test evening time - Night Campaign and All Day should be active
        evening_time = datetime(2023, 1, 1, 20, 0)  # 8 PM
        self.campaign_service.activate_campaigns(evening_time)
        
        self.assertFalse(self.campaign1.is_active)  # Day Campaign
        self.assertTrue(self.campaign2.is_active)  # Night Campaign
        self.assertTrue(self.campaign3.is_active)  # All Day
    
    def test_activate_campaigns_midnight(self):
        # Test midnight - Only All Day should be active
        midnight = datetime(2023, 1, 1, 0, 0)  # 12 AM
        self.campaign_service.activate_campaigns(midnight)
        
        self.assertFalse(self.campaign1.is_active)  # Day Campaign
        self.assertFalse(self.campaign2.is_active)  # Night Campaign
        self.assertTrue(self.campaign3.is_active)  # All Day
    
    def test_activate_campaigns_with_daily_budget_exceeded(self):
        # Set daily budget to exceeded
        self.brand.current_daily_spend = 150  # exceeds 100 daily budget
        
        # Even within dayparting hours, campaigns should be inactive
        daytime = datetime(2023, 1, 1, 12, 0)  # 12 PM
        self.campaign_service.activate_campaigns(daytime)
        
        self.assertFalse(self.campaign1.is_active)
        self.assertFalse(self.campaign2.is_active)
        self.assertFalse(self.campaign3.is_active)
    
    def test_activate_campaigns_with_monthly_budget_exceeded(self):
        # Set monthly budget to exceeded
        self.brand.current_monthly_spend = 3500  # exceeds 3000 monthly budget
        
        # Even within dayparting hours, campaigns should be inactive
        daytime = datetime(2023, 1, 1, 12, 0)  # 12 PM
        self.campaign_service.activate_campaigns(daytime)
        
        self.assertFalse(self.campaign1.is_active)
        self.assertFalse(self.campaign2.is_active)
        self.assertFalse(self.campaign3.is_active)
    
    def test_deactivate_campaigns(self):
        # First activate campaigns
        daytime = datetime(2023, 1, 1, 12, 0)  # 12 PM
        self.campaign_service.activate_campaigns(daytime)
        
        # Verify some are active
        self.assertTrue(self.campaign1.is_active)
        self.assertTrue(self.campaign3.is_active)
        
        # Deactivate all
        self.campaign_service.deactivate_campaigns()
        
        # Verify all are inactive
        self.assertFalse(self.campaign1.is_active)
        self.assertFalse(self.campaign2.is_active)
        self.assertFalse(self.campaign3.is_active)
    
    def test_budget_reset_and_reactivation(self):
        # Exceed budget
        self.brand.current_daily_spend = 150
        
        # Campaigns should be inactive due to budget
        daytime = datetime(2023, 1, 1, 12, 0)
        self.campaign_service.activate_campaigns(daytime)
        self.assertFalse(self.campaign1.is_active)
        
        # Reset budget
        self.brand.reset_daily_budget()
        
        # Check activation again
        self.campaign_service.activate_campaigns(daytime)
        self.assertTrue(self.campaign1.is_active)  # Should be active now

if __name__ == "__main__":
    unittest.main()