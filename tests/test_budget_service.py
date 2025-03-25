from src.services.budget_service import BudgetService
from src.models.brand import Brand

def test_budget_service():
    # Create a brand with specific budgets
    brand = Brand(name="Test Brand", daily_budget=100, monthly_budget=3000)
    budget_service = BudgetService(brand)

    # Test initial state
    assert brand.current_daily_spend == 0
    assert brand.current_monthly_spend == 0

    # Test daily budget update
    budget_service.update_daily_spend(50)
    assert brand.current_daily_spend == 50
    assert not budget_service.is_daily_budget_exceeded()

    budget_service.update_daily_spend(60)  # This should exceed the daily budget
    assert brand.current_daily_spend == 110
    assert budget_service.is_daily_budget_exceeded()

    # Reset daily spend and check
    budget_service.reset_daily_spend()
    assert brand.current_daily_spend == 0

    # Test monthly budget update
    budget_service.update_monthly_spend(2000)
    assert brand.current_monthly_spend == 2000
    assert not budget_service.is_monthly_budget_exceeded()

    budget_service.update_monthly_spend(1500)  # This should exceed the monthly budget
    assert brand.current_monthly_spend == 3500
    assert budget_service.is_monthly_budget_exceeded()

    # Reset monthly spend and check
    budget_service.reset_monthly_spend()
    assert brand.current_monthly_spend == 0

    # Test turning off campaigns
    budget_service.update_daily_spend(100)  # Set to daily budget
    assert budget_service.turn_off_campaigns_if_budget_exceeded() == True

    budget_service.reset_daily_spend()
    budget_service.update_monthly_spend(3000)  # Set to monthly budget
    assert budget_service.turn_off_campaigns_if_budget_exceeded() == True

    # Final assertions
    assert brand.current_daily_spend == 0
    assert brand.current_monthly_spend == 0
    assert not budget_service.is_daily_budget_exceeded()
    assert not budget_service.is_monthly_budget_exceeded()