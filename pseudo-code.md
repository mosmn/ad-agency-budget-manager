# Ad Agency Budget Manager: Pseudo-code

This document provides a high-level, language-agnostic overview of the algorithms and data structures used in the Ad Agency Budget Manager system.

## Data Structures

### Brand

```
Class Brand
    Properties:
        name: String
        monthly_budget: Number
        daily_budget: Number
        current_monthly_spend: Number (initialized to 0)
        current_daily_spend: Number (initialized to 0)
        campaigns: List of Campaign objects
  
    Methods:
        add_campaign(campaign: Campaign): void
        check_monthly_budget(): Boolean
            return current_monthly_spend >= monthly_budget
        check_daily_budget(): Boolean
            return current_daily_spend >= daily_budget
        reset_daily_budget(): void
            set current_daily_spend to 0
        reset_monthly_budget(): void
            set current_monthly_spend to 0
```

### Campaign

```
Class Campaign
    Properties:
        name: String
        is_active: Boolean (initialized to false)
        dayparting_hours: Tuple of (start_hour: Integer, end_hour: Integer)
  
    Methods:
        activate(): void
            set is_active to true
        deactivate(): void
            set is_active to false
        is_within_dayparting(current_time: DateTime): Boolean
            start_hour, end_hour = dayparting_hours
            return start_hour <= current_time.hour < end_hour
```

## Services

### BudgetService

```
Class BudgetService
    Properties:
        brand: Brand
  
    Methods:
        update_daily_spend(amount: Number): void
            brand.current_daily_spend += amount
            if brand.check_daily_budget() then
                deactivate_campaigns()
            end if
      
        update_monthly_spend(amount: Number): void
            brand.current_monthly_spend += amount
            if brand.check_monthly_budget() then
                deactivate_campaigns()
            end if
      
        deactivate_campaigns(): void
            for each campaign in brand.campaigns do
                campaign.deactivate()
            end for
```

### CampaignService

```
Class CampaignService
    Properties:
        brand: Brand
  
    Methods:
        activate_campaigns(current_time: DateTime): void
            for each campaign in brand.campaigns do
                if campaign.is_within_dayparting(current_time) AND 
                   NOT brand.check_daily_budget() AND 
                   NOT brand.check_monthly_budget() then
                    campaign.activate()
                else
                    campaign.deactivate()
                end if
            end for
      
        deactivate_campaigns(): void
            for each campaign in brand.campaigns do
                campaign.deactivate()
            end for
```

## Core Processes

### Daily Budget Reset Process

```
Process reset_daily_budgets
    for each brand in all_brands do
        brand.reset_daily_budget()
        log "Reset daily budget for {brand.name}"
    end for
```

### Monthly Budget Reset Process

```
Process reset_monthly_budgets
    for each brand in all_brands do
        brand.reset_monthly_budget()
        log "Reset monthly budget for {brand.name}"
    end for
```

### Campaign Status Check Process

```
Process check_campaign_status
    current_time = get_current_time()
  
    for each brand in all_brands do
        campaign_service = create CampaignService with brand
      
        // Save previous status to report changes
        previous_statuses = Dictionary mapping campaign name to is_active status
      
        // Update campaign statuses
        campaign_service.activate_campaigns(current_time)
      
        // Log results
        for each campaign in brand.campaigns do
            previous_status = previous_statuses[campaign.name]
            current_status = campaign.is_active
          
            if previous_status != current_status then
                if current_status then
                    log "Campaign {campaign.name} ACTIVATED"
                else
                    log "Campaign {campaign.name} DEACTIVATED"
                end if
            end if
          
            if not current_status then
                if not campaign.is_within_dayparting(current_time) then
                    log "Campaign {campaign.name} inactive: outside dayparting hours"
                else if brand.check_daily_budget() then
                    log "Campaign {campaign.name} inactive: daily budget exceeded"
                else if brand.check_monthly_budget() then
                    log "Campaign {campaign.name} inactive: monthly budget exceeded"
                end if
            end if
        end for
    end for
```

### Spend Update Process

```
Process update_brand_spend(brand_name: String, amount: Number)
    brand = find brand by name
    if brand not found then
        log "Brand {brand_name} not found"
        return
    end if
  
    budget_service = create BudgetService with brand
  
    log "Updating spend for {brand_name} by {amount}"
  
    budget_service.update_daily_spend(amount)
    budget_service.update_monthly_spend(amount)
  
    log "Updated spend: daily={brand.current_daily_spend}, monthly={brand.current_monthly_spend}"
  
    if brand.check_daily_budget() then
        log "Daily budget exceeded for {brand_name}"
    end if
  
    if brand.check_monthly_budget() then
        log "Monthly budget exceeded for {brand_name}"
    end if
```

## Scheduled Tasks

```
Schedule:
    At midnight every day:
        Execute reset_daily_budgets process
  
    At midnight on the 1st of every month:
        Execute reset_monthly_budgets process
  
    Every hour:
        Execute check_campaign_status process
```
