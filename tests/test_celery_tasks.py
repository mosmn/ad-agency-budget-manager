import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.celery_tasks import (
    initialize_brand,
    update_brand_spend,
    reset_daily_budgets,
    reset_monthly_budgets,
    check_campaign_status,
    brands
)

class TestCeleryTasks(unittest.TestCase):
    def setUp(self):
        # Clear the brands dictionary before each test
        brands.clear()
    
    def test_initialize_brand(self):
        campaign_data = {
            "Campaign 1": (9, 17),
            "Campaign 2": (0, 24)
        }
        
        result = initialize_brand("Test Brand", 3000, 100, campaign_data)
        
        self.assertEqual(result, "Test Brand")
        self.assertIn("Test Brand", brands)
        self.assertEqual(len(brands["Test Brand"].campaigns), 2)
        self.assertEqual(brands["Test Brand"].monthly_budget, 3000)
        self.assertEqual(brands["Test Brand"].daily_budget, 100)
    
    def test_update_brand_spend_brand_exists(self):
        # First initialize a brand
        initialize_brand("Test Brand", 3000, 100, {"Campaign 1": (9, 17)})
        
        # Update spend
        result = update_brand_spend("Test Brand", 50)
        
        self.assertTrue(result)
        self.assertEqual(brands["Test Brand"].current_daily_spend, 50)
        self.assertEqual(brands["Test Brand"].current_monthly_spend, 50)
    
    def test_update_brand_spend_brand_not_found(self):
        # Try to update non-existent brand
        result = update_brand_spend("Nonexistent Brand", 50)
        
        self.assertFalse(result)
    
    def test_update_brand_spend_exceed_budget(self):
        # Initialize brand
        initialize_brand("Test Brand", 3000, 100, {"Campaign 1": (9, 17)})
        
        # Activate campaigns
        for campaign in brands["Test Brand"].campaigns:
            campaign.activate()
        
        # Update spend to exceed daily budget
        update_brand_spend("Test Brand", 120)
        
        # Check that campaigns are deactivated
        for campaign in brands["Test Brand"].campaigns:
            self.assertFalse(campaign.is_active)
    
    def test_reset_daily_budgets(self):
        # Initialize brand and add some spend
        initialize_brand("Brand1", 3000, 100, {"Campaign 1": (9, 17)})
        initialize_brand("Brand2", 2000, 200, {"Campaign 2": (0, 24)})
        
        update_brand_spend("Brand1", 50)
        update_brand_spend("Brand2", 100)
        
        # Reset daily budgets
        result = reset_daily_budgets()
        
        self.assertTrue(result)
        self.assertEqual(brands["Brand1"].current_daily_spend, 0)
        self.assertEqual(brands["Brand2"].current_daily_spend, 0)
        # Monthly spend should remain
        self.assertEqual(brands["Brand1"].current_monthly_spend, 50)
        self.assertEqual(brands["Brand2"].current_monthly_spend, 100)
    
    def test_reset_monthly_budgets(self):
        # Initialize brand and add some spend
        initialize_brand("Brand1", 3000, 100, {"Campaign 1": (9, 17)})
        initialize_brand("Brand2", 2000, 200, {"Campaign 2": (0, 24)})
        
        update_brand_spend("Brand1", 50)
        update_brand_spend("Brand2", 100)
        
        # Reset monthly budgets
        result = reset_monthly_budgets()
        
        self.assertTrue(result)
        # Daily spend should remain
        self.assertEqual(brands["Brand1"].current_daily_spend, 50)
        self.assertEqual(brands["Brand2"].current_daily_spend, 100)
        # Monthly spend should be reset
        self.assertEqual(brands["Brand1"].current_monthly_spend, 0)
        self.assertEqual(brands["Brand2"].current_monthly_spend, 0)
    
    @patch('src.celery_tasks.datetime')
    def test_check_campaign_status(self, mock_datetime):
        # Set a fixed time for testing
        mock_datetime.now.return_value = datetime(2023, 1, 1, 10, 0)  # 10 AM
        
        # Initialize a brand with day and night campaigns
        initialize_brand("Test Brand", 3000, 100, {
            "Day Campaign": (9, 17),   # 9 AM to 5 PM
            "Night Campaign": (18, 23) # 6 PM to 11 PM
        })
        
        # Check status
        result = check_campaign_status()
        
        self.assertTrue(result)
        
        # At 10 AM, day campaign should be active and night campaign inactive
        campaigns = brands["Test Brand"].campaigns
        day_campaign = next(c for c in campaigns if c.name == "Day Campaign")
        night_campaign = next(c for c in campaigns if c.name == "Night Campaign")
        
        self.assertTrue(day_campaign.is_active)
        self.assertFalse(night_campaign.is_active)
    
    def test_check_campaign_status_no_brands(self):
        # Make sure no brands are initialized
        brands.clear()
        
        # Should return True and not raise any exceptions
        result = check_campaign_status()
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
