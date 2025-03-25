import unittest
from src.main import Brand, Campaign, BudgetService

class TestBudgetService(unittest.TestCase):
    def setUp(self):
        self.brand = Brand(name="Test Brand", monthly_budget=3000, daily_budget=100)
        self.campaign1 = Campaign(name="Campaign 1", dayparting_hours=(9, 17))
        self.campaign2 = Campaign(name="Campaign 2", dayparting_hours=(0, 24))
        self.brand.add_campaign(self.campaign1)
        self.brand.add_campaign(self.campaign2)
        
        # Activate campaigns
        self.campaign1.activate()
        self.campaign2.activate()
        
        self.budget_service = BudgetService(self.brand)

    def test_initial_state(self):
        self.assertEqual(self.brand.current_daily_spend, 0)
        self.assertEqual(self.brand.current_monthly_spend, 0)
        self.assertTrue(self.campaign1.is_active)
        self.assertTrue(self.campaign2.is_active)
    
    def test_update_daily_spend_under_budget(self):
        self.budget_service.update_daily_spend(50)
        self.assertEqual(self.brand.current_daily_spend, 50)
        self.assertTrue(self.campaign1.is_active)
        self.assertTrue(self.campaign2.is_active)
    
    def test_update_daily_spend_exact_budget(self):
        self.budget_service.update_daily_spend(100)
        self.assertEqual(self.brand.current_daily_spend, 100)
        self.assertFalse(self.campaign1.is_active)
        self.assertFalse(self.campaign2.is_active)
    
    def test_update_daily_spend_exceed_budget(self):
        self.budget_service.update_daily_spend(150)
        self.assertEqual(self.brand.current_daily_spend, 150)
        self.assertFalse(self.campaign1.is_active)
        self.assertFalse(self.campaign2.is_active)
    
    def test_update_monthly_spend_under_budget(self):
        self.budget_service.update_monthly_spend(1500)
        self.assertEqual(self.brand.current_monthly_spend, 1500)
        self.assertTrue(self.campaign1.is_active)
        self.assertTrue(self.campaign2.is_active)
    
    def test_update_monthly_spend_exact_budget(self):
        self.budget_service.update_monthly_spend(3000)
        self.assertEqual(self.brand.current_monthly_spend, 3000)
        self.assertFalse(self.campaign1.is_active)
        self.assertFalse(self.campaign2.is_active)
    
    def test_update_monthly_spend_exceed_budget(self):
        self.budget_service.update_monthly_spend(3500)
        self.assertEqual(self.brand.current_monthly_spend, 3500)
        self.assertFalse(self.campaign1.is_active)
        self.assertFalse(self.campaign2.is_active)
    
    def test_deactivate_campaigns(self):
        # Ensure campaigns are active
        self.campaign1.activate()
        self.campaign2.activate()
        self.assertTrue(self.campaign1.is_active)
        self.assertTrue(self.campaign2.is_active)
        
        # Deactivate campaigns
        self.budget_service.deactivate_campaigns()
        self.assertFalse(self.campaign1.is_active)
        self.assertFalse(self.campaign2.is_active)
    
    def test_multiple_spend_updates(self):
        # Multiple updates to daily spend
        self.budget_service.update_daily_spend(30)
        self.assertEqual(self.brand.current_daily_spend, 30)
        self.assertTrue(self.campaign1.is_active)
        
        self.budget_service.update_daily_spend(40)
        self.assertEqual(self.brand.current_daily_spend, 70)
        self.assertTrue(self.campaign1.is_active)
        
        self.budget_service.update_daily_spend(40)
        self.assertEqual(self.brand.current_daily_spend, 110)
        self.assertFalse(self.campaign1.is_active)
    
    def test_budget_reset_and_reactivation(self):
        # Exceed budget and deactivate campaigns
        self.budget_service.update_daily_spend(150)
        self.assertFalse(self.campaign1.is_active)
        
        # Reset budget
        self.brand.reset_daily_budget()
        self.assertEqual(self.brand.current_daily_spend, 0)
        
        # Campaigns should still be deactivated until checked again
        self.assertFalse(self.campaign1.is_active)

if __name__ == "__main__":
    unittest.main()