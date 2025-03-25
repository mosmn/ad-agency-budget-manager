from celery import Celery
from datetime import datetime
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.models.brand import Brand
from src.models.campaign import Campaign
from src.services.budget_service import BudgetService
from src.services.campaign_service import CampaignService
import logging
import coloredlogs

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

# Initialize Celery app
app = Celery('ad_agency_tasks')
app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Store brands (in a real app this would be in a database)
brands = {}


@app.task
def initialize_brand(name, monthly_budget, daily_budget, campaign_data):
    """Initialize a brand with its campaigns."""
    brand = Brand(name, monthly_budget, daily_budget)
    
    for campaign_name, dayparting_hours in campaign_data.items():
        campaign = Campaign(campaign_name, dayparting_hours)
        brand.add_campaign(campaign)
    
    brands[name] = brand
    logger.info(f"✨ Initialized brand: {name} with {len(campaign_data)} campaigns")
    logger.info(f"📊 Budget limits - Daily: ${daily_budget}, Monthly: ${monthly_budget}")
    
    # Log campaign details
    for campaign_name, hours in campaign_data.items():
        logger.info(f"  - Campaign: {campaign_name}, Dayparting: {hours[0]}:00-{hours[1]}:00")
    
    return name


@app.task
def update_brand_spend(brand_name, amount):
    """Update a brand's daily and monthly spend."""
    if brand_name not in brands:
        logger.error(f"❌ Brand '{brand_name}' not found")
        return False
    
    brand = brands[brand_name]
    budget_service = BudgetService(brand)
    
    logger.info(f"💰 Updating spend for {brand_name} by ${amount}")
    logger.info(f"  Before update - Daily: ${brand.current_daily_spend}/{brand.daily_budget}, " +
                f"Monthly: ${brand.current_monthly_spend}/{brand.monthly_budget}")
    
    budget_service.update_daily_spend(amount)
    budget_service.update_monthly_spend(amount)
    
    logger.info(f"  After update - Daily: ${brand.current_daily_spend}/{brand.daily_budget}, " +
                f"Monthly: ${brand.current_monthly_spend}/{brand.monthly_budget}")
    
    # Check if any budgets were exceeded
    if brand.check_daily_budget():
        logger.warning(f"⚠️ Daily budget exceeded for {brand_name}")
    if brand.check_monthly_budget():
        logger.warning(f"⚠️ Monthly budget exceeded for {brand_name}")
    
    return True


@app.task
def reset_daily_budgets():
    """Reset daily budgets for all brands at the start of a new day."""
    logger.info(f"🔄 Resetting daily budgets for all brands")
    
    for brand_name, brand in brands.items():
        logger.info(f"  - {brand_name}: ${brand.current_daily_spend} → $0")
        brand.reset_daily_budget()
    
    logger.info(f"✅ Daily budget reset completed for {len(brands)} brands")
    return True


@app.task
def reset_monthly_budgets():
    """Reset monthly budgets for all brands at the start of a new month."""
    logger.info(f"🔄 Resetting monthly budgets for all brands")
    
    for brand_name, brand in brands.items():
        logger.info(f"  - {brand_name}: ${brand.current_monthly_spend} → $0")
        brand.reset_monthly_budget()
    
    logger.info(f"✅ Monthly budget reset completed for {len(brands)} brands")
    return True


@app.task
def check_campaign_status():
    """Check and update the status of all campaigns based on current time and budgets."""
    current_time = datetime.now()
    logger.info(f"🔍 Checking campaign status at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not brands:
        logger.info("  No brands configured yet")
        return True
    
    for brand_name, brand in brands.items():
        logger.info(f"  Brand: {brand_name}")
        logger.info(f"  Budget status - Daily: ${brand.current_daily_spend}/{brand.daily_budget}, " +
                    f"Monthly: ${brand.current_monthly_spend}/{brand.monthly_budget}")
        
        campaign_service = CampaignService(brand)
        
        # Save previous status to report changes
        previous_statuses = {c.name: c.is_active for c in brand.campaigns}
        
        campaign_service.activate_campaigns(current_time)
        
        # Log campaign statuses with reasons for being inactive
        for campaign in brand.campaigns:
            previous_status = previous_statuses[campaign.name]
            current_status = campaign.is_active
            
            status_change = ""
            if previous_status != current_status:
                if current_status:
                    status_change = " (ACTIVATED)"
                else:
                    status_change = " (DEACTIVATED)"
            
            status_emoji = '✅ ACTIVE' if current_status else '❌ INACTIVE'
            
            reason = ""
            if not current_status:
                if not campaign.is_within_dayparting(current_time):
                    reason = f" (outside dayparting hours {campaign.dayparting_hours[0]}:00-{campaign.dayparting_hours[1]}:00)"
                elif brand.check_daily_budget():
                    reason = " (daily budget exceeded)"
                elif brand.check_monthly_budget():
                    reason = " (monthly budget exceeded)"
            
            logger.info(f"    - {campaign.name}: {status_emoji}{status_change}{reason}")
    
    return True
