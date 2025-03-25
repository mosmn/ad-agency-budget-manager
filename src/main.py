import logging
import argparse
from datetime import datetime, time
import coloredlogs
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.brand import Brand
from src.models.campaign import Campaign
from src.services.budget_service import BudgetService
from src.services.campaign_service import CampaignService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configure colored logs for better readability
coloredlogs.install(
    level='INFO',
    logger=logger,
    fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def simulate_day(brand, budget_service, campaign_service, spend_amount):
    """Simulate a day's activities for a brand."""
    logger.info(f"🚀 Starting simulation for brand: {brand.name}")
    logger.info(f"📊 Initial budget status - Daily limit: ${brand.daily_budget}, Monthly limit: ${brand.monthly_budget}")
    
    # Morning check (9 AM)
    morning = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    logger.info(f"☀️ Morning check ({morning.strftime('%H:%M')})")
    campaign_service.activate_campaigns(morning)
    
    campaign_statuses = []
    for c in brand.campaigns:
        status = '✅ ACTIVE' if c.is_active else '❌ INACTIVE'
        daypart = f"{c.dayparting_hours[0]}:00-{c.dayparting_hours[1]}:00"
        campaign_statuses.append(f"{c.name} ({daypart}): {status}")
    
    logger.info("Campaign status:")
    for status in campaign_statuses:
        logger.info(f"  - {status}")
    
    # Simulating spend
    logger.info(f"💰 Adding spend: ${spend_amount}")
    budget_service.update_daily_spend(spend_amount)
    budget_service.update_monthly_spend(spend_amount)
    logger.info(f"Updated budget status - Daily: ${brand.current_daily_spend}/{brand.daily_budget}, " +
                f"Monthly: ${brand.current_monthly_spend}/{brand.monthly_budget}")
    
    # Check if budgets are exceeded
    if brand.check_daily_budget():
        logger.warning(f"⚠️ Daily budget exceeded for {brand.name}")
    if brand.check_monthly_budget():
        logger.warning(f"⚠️ Monthly budget exceeded for {brand.name}")
    
    # Evening check (6 PM)
    evening = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    logger.info(f"🌙 Evening check ({evening.strftime('%H:%M')})")
    campaign_service.activate_campaigns(evening)
    
    campaign_statuses = []
    for c in brand.campaigns:
        status = '✅ ACTIVE' if c.is_active else '❌ INACTIVE'
        reason = ""
        if not c.is_active:
            if not c.is_within_dayparting(evening):
                reason = " (outside dayparting hours)"
            elif brand.check_daily_budget():
                reason = " (daily budget exceeded)"
            elif brand.check_monthly_budget():
                reason = " (monthly budget exceeded)"
        campaign_statuses.append(f"{c.name}: {status}{reason}")
    
    logger.info("Campaign status:")
    for status in campaign_statuses:
        logger.info(f"  - {status}")
    
    logger.info(f"🏁 Simulation completed for {brand.name}")


def main():
    parser = argparse.ArgumentParser(description='Ad Agency Budget Manager')
    parser.add_argument('--simulate', action='store_true', help='Run a simulation')
    parser.add_argument('--spend', type=float, default=50.0, help='Simulated spend amount')
    args = parser.parse_args()
    
    # Example usage
    brand = Brand("Brand A", 1000, 100)
    campaign1 = Campaign("Campaign 1", (9, 17))  # Active from 9 AM to 5 PM
    campaign2 = Campaign("Campaign 2", (0, 24))  # Active all day
    brand.add_campaign(campaign1)
    brand.add_campaign(campaign2)

    budget_service = BudgetService(brand)
    campaign_service = CampaignService(brand)

    if args.simulate:
        simulate_day(brand, budget_service, campaign_service, args.spend)
    else:
        logger.info("No action specified. Use --simulate to run a simulation.")


if __name__ == "__main__":
    main()