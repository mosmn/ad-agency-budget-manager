import unittest
from datetime import datetime
from src.models.campaign import Campaign

class TestCampaign(unittest.TestCase):
    def setUp(self):
        self.campaign = Campaign(name="Test Campaign", dayparting_hours=(9, 17))
    
    def test_campaign_initialization(self):
        self.assertEqual(self.campaign.name, "Test Campaign")
        self.assertEqual(self.campaign.dayparting_hours, (9, 17))
        self.assertFalse(self.campaign.is_active)
    
    def test_activate(self):
        self.assertFalse(self.campaign.is_active)
        self.campaign.activate()
        self.assertTrue(self.campaign.is_active)
    
    def test_deactivate(self):
        self.campaign.activate()
        self.assertTrue(self.campaign.is_active)
        self.campaign.deactivate()
        self.assertFalse(self.campaign.is_active)
    
    def test_is_within_dayparting(self):
        # Time within dayparting hours (10 AM)
        time_within = datetime(2023, 1, 1, 10, 0)
        self.assertTrue(self.campaign.is_within_dayparting(time_within))
        
        # Time at start of dayparting hours (9 AM)
        time_at_start = datetime(2023, 1, 1, 9, 0)
        self.assertTrue(self.campaign.is_within_dayparting(time_at_start))
        
        # Time at end of dayparting hours (5 PM)
        time_at_end = datetime(2023, 1, 1, 17, 0)
        self.assertFalse(self.campaign.is_within_dayparting(time_at_end))
        
        # Time before dayparting hours (8 AM)
        time_before = datetime(2023, 1, 1, 8, 0)
        self.assertFalse(self.campaign.is_within_dayparting(time_before))
        
        # Time after dayparting hours (6 PM)
        time_after = datetime(2023, 1, 1, 18, 0)
        self.assertFalse(self.campaign.is_within_dayparting(time_after))
        
        # 24-hour campaign check
        all_day_campaign = Campaign(name="All Day", dayparting_hours=(0, 24))
        midnight = datetime(2023, 1, 1, 0, 0)
        noon = datetime(2023, 1, 1, 12, 0)
        eleven_pm = datetime(2023, 1, 1, 23, 0)
        
        self.assertTrue(all_day_campaign.is_within_dayparting(midnight))
        self.assertTrue(all_day_campaign.is_within_dayparting(noon))
        self.assertTrue(all_day_campaign.is_within_dayparting(eleven_pm))

if __name__ == "__main__":
    unittest.main()
