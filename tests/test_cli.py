import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCLI(unittest.TestCase):
    @patch('src.cli.initialize_brand')
    def test_init_brand_command(self, mock_initialize_brand):
        # Set up mock for delay
        mock_initialize_brand.delay = MagicMock(return_value=None)
        
        # Import after patching
        from src.cli import main
        
        # Set up command line arguments
        testargs = ['cli.py', 'init-brand', 'Test Brand', '3000', '100', 
                   '--campaign', 'Campaign 1', '9', '17']
        with patch('sys.argv', testargs):
            main()
        
        # Verify initialize_brand.delay was called with correct arguments
        mock_initialize_brand.delay.assert_called_once_with(
            'Test Brand', 
            3000.0, 
            100.0, 
            {'Campaign 1': (9, 17)}
        )
    
    @patch('src.cli.update_brand_spend')
    def test_update_spend_command(self, mock_update_brand_spend):
        # Set up mock for delay
        mock_update_brand_spend.delay = MagicMock(return_value=None)
        
        # Import after patching
        from src.cli import main
        
        # Set up command line arguments
        testargs = ['cli.py', 'update-spend', 'Test Brand', '50']
        with patch('sys.argv', testargs):
            main()
        
        # Verify update_brand_spend.delay was called with correct arguments
        mock_update_brand_spend.delay.assert_called_once_with('Test Brand', 50.0)
    
    @patch('src.cli.reset_daily_budgets')
    def test_reset_daily_command(self, mock_reset_daily_budgets):
        # Set up mock for delay
        mock_reset_daily_budgets.delay = MagicMock(return_value=None)
        
        # Import after patching
        from src.cli import main
        
        # Set up command line arguments
        testargs = ['cli.py', 'reset-daily']
        with patch('sys.argv', testargs):
            main()
        
        # Verify reset_daily_budgets.delay was called
        mock_reset_daily_budgets.delay.assert_called_once()
    
    @patch('src.cli.reset_monthly_budgets')
    def test_reset_monthly_command(self, mock_reset_monthly_budgets):
        # Set up mock for delay
        mock_reset_monthly_budgets.delay = MagicMock(return_value=None)
        
        # Import after patching
        from src.cli import main
        
        # Set up command line arguments
        testargs = ['cli.py', 'reset-monthly']
        with patch('sys.argv', testargs):
            main()
        
        # Verify reset_monthly_budgets.delay was called
        mock_reset_monthly_budgets.delay.assert_called_once()
    
    @patch('src.cli.check_campaign_status')
    def test_check_status_command(self, mock_check_campaign_status):
        # Set up mock for delay
        mock_check_campaign_status.delay = MagicMock(return_value=None)
        
        # Import after patching
        from src.cli import main
        
        # Set up command line arguments
        testargs = ['cli.py', 'check-status']
        with patch('sys.argv', testargs):
            main()
        
        # Verify check_campaign_status.delay was called
        mock_check_campaign_status.delay.assert_called_once()
    
    @patch('argparse.ArgumentParser.print_help')
    def test_no_command(self, mock_print_help):
        # Import the module
        from src.cli import main
        
        # Set up command line arguments with no command
        testargs = ['cli.py']
        with patch('sys.argv', testargs):
            main()
        
        # Verify print_help was called
        mock_print_help.assert_called_once()

if __name__ == "__main__":
    unittest.main()
