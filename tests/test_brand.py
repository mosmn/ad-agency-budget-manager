import unittest
from src.main import Brand, Campaign

class TestBrand(unittest.TestCase):
    def setUp(self):
        self.brand = Brand(name="Test Brand", monthly_budget=3000, daily_budget=100)
        self.campaign1 = Campaign(name="Campaign 1", dayparting_hours=(9, 17))
        self.campaign2 = Campaign(name="Campaign 2", dayparting_hours=(0, 24))
    
    def test_brand_initialization(self):
        self.assertEqual(self.brand.name, "Test Brand")
        self.assertEqual(self.brand.monthly_budget, 3000)
        self.assertEqual(self.brand.daily_budget, 100)
        self.assertEqual(self.brand.current_monthly_spend, 0)
        self.assertEqual(self.brand.current_daily_spend, 0)
        self.assertEqual(len(self.brand.campaigns), 0)
    
    def test_add_campaign(self):
        self.brand.add_campaign(self.campaign1)
        self.assertEqual(len(self.brand.campaigns), 1)
        self.assertEqual(self.brand.campaigns[0].name, "Campaign 1")
        
        self.brand.add_campaign(self.campaign2)
        self.assertEqual(len(self.brand.campaigns), 2)
        self.assertEqual(self.brand.campaigns[1].name, "Campaign 2")
    
    def test_check_monthly_budget(self):
        # Initially, the budget is not exceeded
        self.assertFalse(self.brand.check_monthly_budget())
        
        # Set the spend equal to budget
        self.brand.current_monthly_spend = 3000
        self.assertTrue(self.brand.check_monthly_budget())
        
        # Set the spend above budget
        self.brand.current_monthly_spend = 3001
        self.assertTrue(self.brand.check_monthly_budget())
    
    def test_check_daily_budget(self):
        # Initially, the budget is not exceeded
        self.assertFalse(self.brand.check_daily_budget())
        
        # Set the spend equal to budget
        self.brand.current_daily_spend = 100
        self.assertTrue(self.brand.check_daily_budget())
        
        # Set the spend above budget
        self.brand.current_daily_spend = 101
        self.assertTrue(self.brand.check_daily_budget())
    
    def test_reset_daily_budget(self):
        self.brand.current_daily_spend = 50
        self.brand.reset_daily_budget()
        self.assertEqual(self.brand.current_daily_spend, 0)
    
    def test_reset_monthly_budget(self):
        self.brand.current_monthly_spend = 1500
        self.brand.reset_monthly_budget()
        self.assertEqual(self.brand.current_monthly_spend, 0)

if __name__ == "__main__":
    unittest.main()
