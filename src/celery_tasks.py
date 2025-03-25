from celery import Celery
from datetime import datetime
from src.main import Brand, Campaign, BudgetService, CampaignService
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
    logger.info(f"Initialized brand: {name} with {len(campaign_data)} campaigns")
    return name


@app.task
def update_brand_spend(brand_name, amount):
    """Update a brand's daily and monthly spend."""
    if brand_name not in brands:
        logger.error(f"Brand {brand_name} not found")
        return False
    
    brand = brands[brand_name]
    budget_service = BudgetService(brand)
    
    budget_service.update_daily_spend(amount)
    budget_service.update_monthly_spend(amount)
    
    logger.info(f"Updated {brand_name} spend by {amount}. Daily: {brand.current_daily_spend}, Monthly: {brand.current_monthly_spend}")
    return True


@app.task
def reset_daily_budgets():
    """Reset daily budgets for all brands at the start of a new day."""
    for brand_name, brand in brands.items():
        brand.reset_daily_budget()
        logger.info(f"Reset daily budget for {brand_name}")
    return True


@app.task
def reset_monthly_budgets():
    """Reset monthly budgets for all brands at the start of a new month."""
    for brand_name, brand in brands.items():
        brand.reset_monthly_budget()
        logger.info(f"Reset monthly budget for {brand_name}")
    return True


@app.task
def check_campaign_status():
    """Check and update the status of all campaigns based on current time and budgets."""
    current_time = datetime.now()
    logger.info(f"Checking campaign status at {current_time}")
    
    for brand_name, brand in brands.items():
        campaign_service = CampaignService(brand)
        campaign_service.activate_campaigns(current_time)
        
        # Log campaign statuses
        campaign_statuses = [f"{c.name}: {'active' if c.is_active else 'inactive'}" for c in brand.campaigns]
        logger.info(f"Brand {brand_name} campaigns: {', '.join(campaign_statuses)}")
    
    return True
