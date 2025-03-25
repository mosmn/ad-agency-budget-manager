import argparse
import logging
from datetime import datetime
from celery_tasks import (
    initialize_brand, 
    update_brand_spend, 
    reset_daily_budgets,
    reset_monthly_budgets,
    check_campaign_status
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Ad Agency Budget Manager CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Initialize brand command
    init_parser = subparsers.add_parser('init-brand', help='Initialize a new brand')
    init_parser.add_argument('name', type=str, help='Brand name')
    init_parser.add_argument('monthly_budget', type=float, help='Monthly budget')
    init_parser.add_argument('daily_budget', type=float, help='Daily budget')
    init_parser.add_argument('--campaign', action='append', nargs=3, 
                            metavar=('name', 'start_hour', 'end_hour'),
                            help='Add a campaign with name and dayparting hours')
    
    # Update spend command
    spend_parser = subparsers.add_parser('update-spend', help='Update brand spend')
    spend_parser.add_argument('brand_name', type=str, help='Brand name')
    spend_parser.add_argument('amount', type=float, help='Amount to add to spending')
    
    # Reset budgets commands
    subparsers.add_parser('reset-daily', help='Reset daily budgets for all brands')
    subparsers.add_parser('reset-monthly', help='Reset monthly budgets for all brands')
    
    # Check status command
    subparsers.add_parser('check-status', help='Check campaign status based on current time and budgets')
    
    args = parser.parse_args()
    
    if args.command == 'init-brand':
        campaign_data = {}
        if args.campaign:
            for campaign_args in args.campaign:
                name, start_hour, end_hour = campaign_args
                campaign_data[name] = (int(start_hour), int(end_hour))
        
        initialize_brand.delay(args.name, args.monthly_budget, args.daily_budget, campaign_data)
        logger.info(f"Brand initialization task sent: {args.name}")
    
    elif args.command == 'update-spend':
        update_brand_spend.delay(args.brand_name, args.amount)
        logger.info(f"Update spend task sent for {args.brand_name}: ${args.amount}")
    
    elif args.command == 'reset-daily':
        reset_daily_budgets.delay()
        logger.info("Reset daily budgets task sent")
    
    elif args.command == 'reset-monthly':
        reset_monthly_budgets.delay()
        logger.info("Reset monthly budgets task sent")
    
    elif args.command == 'check-status':
        check_campaign_status.delay()
        logger.info("Check campaign status task sent")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
