# Ad Agency Budget Manager

A system to manage advertising budgets, campaigns, and dayparting for multiple brands.

## Overview

This application helps ad agencies manage their clients' ad campaigns by:
- Tracking daily and monthly budgets for each brand
- Automatically turning off campaigns when budgets are exceeded
- Respecting dayparting schedules (campaigns that should only run during specific hours)
- Automatically resetting budgets at the start of each new day/month

## Data Structures

- **Brand**: Contains brand information, budget limits, current spend, and associated campaigns
- **Campaign**: Contains campaign information, active status, and dayparting hours
- **BudgetService**: Manages budget updates and campaign deactivation
- **CampaignService**: Manages campaign activation based on dayparting and budget availability

## Program Flow

1. Brands are initialized with their budget limits and campaigns
2. Throughout the day, spending is recorded against daily and monthly budgets
3. When spending exceeds the daily or monthly budget, associated campaigns are turned off
4. At the start of each new day, daily budgets are reset
5. At the start of each new month, monthly budgets are reset
6. Campaigns are activated or deactivated based on current time and dayparting rules

## Setup and Installation

### Prerequisites

- Python 3.8+
- Redis (for Celery task queue)

#### Installing and Managing Redis

##### macOS
Install Redis using Homebrew:
```bash
brew install redis
```

Start Redis server:
```bash
brew services start redis
```

Stop Redis server:
```bash
brew services stop redis
```

Check Redis status:
```bash
brew services list | grep redis
```

##### Windows
1. Download the Redis Windows installer from [Redis Downloads](https://github.com/microsoftarchive/redis/releases)
2. Run the installer (Redis-x64-xxx.msi)
3. The installer will add Redis to Windows Services

Manage Redis service using PowerShell:
```powershell
# Start Redis
Start-Service Redis

# Stop Redis
Stop-Service Redis

# Check Redis status
Get-Service Redis
```

Alternative: Using command prompt:
```cmd
# Start Redis
net start Redis

# Stop Redis
net stop Redis
```

Test Redis connection (both OS):
```bash
redis-cli ping
# Should return PONG
```

### Installation

1. Clone the repository
2. Install dependencies:
```
pip install -r requirements.txt
```

## Running the Application

### Using Honcho (Recommended)

Start all services with a single command:

```bash
cd ad-agency-budget-manager
honcho start
```

To start specific services only:

```bash
# Start worker and scheduler only
honcho start worker scheduler

# Start just the simulation
honcho start sim
```

### Starting Services Individually

#### Starting the Celery Workers

```bash
cd ad-agency-budget-manager
celery -A src.celery_tasks worker --loglevel=info
```

#### Starting the Celery Beat Scheduler

```bash
cd ad-agency-budget-manager
celery -A celerybeat-schedule beat --loglevel=info
```

### Using the CLI

Initialize a brand with campaigns:

```bash
python src/cli.py init-brand "Brand A" 1000 100 --campaign "Campaign 1" 9 17 --campaign "Campaign 2" 0 24
```

Update brand spending:

```bash
python src/cli.py update-spend "Brand A" 50
```

Reset daily budgets:

```bash
python src/cli.py reset-daily
```

Reset monthly budgets:

```bash
python src/cli.py reset-monthly
```

Check campaign status:

```bash
python src/cli.py check-status
```

## Running a Simulation

To run a simple simulation:

```bash
python src/main.py --simulate --spend 75
```

## Running Tests

To run the unit tests and ensure everything is working as expected:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=src tests/

# Run a specific test file
pytest tests/test_brand.py
```

The test suite has been designed to cover all key functionality including:
- Brand and Campaign model behavior
- Budget management
- Campaign activation and deactivation based on time and budget constraints
- Celery task functionality
- CLI command processing

## Assumptions and Simplifications

- In-memory storage is used for brands and campaigns (a real system would use a database)
- All times are in the local timezone
- Budget periods are based on calendar days and months
- Campaign dayparting hours are specified as integers (0-23)
- No authentication or user management is implemented