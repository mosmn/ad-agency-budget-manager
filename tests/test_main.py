import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime
import io

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestMain(unittest.TestCase):
    @patch('src.main.simulate_day')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_simulate(self, mock_parse_args, mock_simulate_day):
        # Configure the mock for parse_args
        args = MagicMock()
        args.simulate = True
        args.spend = 75.0
        mock_parse_args.return_value = args
        
        # Import the module after patching
        from src.main import main
        
        # Call the main function
        main()
        
        # Verify simulate_day was called
        mock_simulate_day.assert_called_once()
    
    @patch('argparse.ArgumentParser.parse_args')
    @patch('src.main.logger')
    def test_main_no_simulate(self, mock_logger, mock_parse_args):
        # Configure the mock for parse_args
        args = MagicMock()
        args.simulate = False
        mock_parse_args.return_value = args
        
        # Import the module after patching
        from src.main import main
        
        # Call the main function
        main()
        
        # Verify logger.info was called with the right message
        mock_logger.info.assert_any_call("No action specified. Use --simulate to run a simulation.")
    
    @patch('src.main.datetime')
    def test_simulate_day(self, mock_datetime):
        # Import the module after patching
        from src.main import Brand, Campaign, BudgetService, CampaignService, simulate_day
        
        # Fix the time for testing
        morning = datetime(2023, 1, 1, 9, 0)
        evening = datetime(2023, 1, 1, 18, 0)
        mock_datetime.now.side_effect = [morning, evening]
        
        # Create test objects
        brand = Brand("Test Brand", 1000, 100)
        campaign1 = Campaign("Day Campaign", (9, 17))
        campaign2 = Campaign("All Day", (0, 24))
        brand.add_campaign(campaign1)
        brand.add_campaign(campaign2)
        
        budget_service = BudgetService(brand)
        campaign_service = CampaignService(brand)
        
        # Capture stdout to verify log messages
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            simulate_day(brand, budget_service, campaign_service, 50.0)
            
            # Verify the spend was updated
            self.assertEqual(brand.current_daily_spend, 50.0)
            self.assertEqual(brand.current_monthly_spend, 50.0)
    
    def test_brand_check_budget(self):
        # Import the module
        from src.main import Brand
        
        # Create a brand
        brand = Brand("Test", 1000, 100)
        
        # Test daily budget check
        brand.current_daily_spend = 50
        self.assertFalse(brand.check_daily_budget())
        
        brand.current_daily_spend = 100
        self.assertTrue(brand.check_daily_budget())
        
        # Test monthly budget check
        brand.current_monthly_spend = 500
        self.assertFalse(brand.check_monthly_budget())
        
        brand.current_monthly_spend = 1000
        self.assertTrue(brand.check_monthly_budget())

if __name__ == "__main__":
    unittest.main()
