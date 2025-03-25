
1. First, make sure you have Redis installed and running. On Mac you can do:

```bash
brew install redis
brew services start redis
```

2. Set up your Python environment (if not already done):

```bash
python -m venv venv
source venv/bin/activate
pip install celery redis coloredlogs
```

3. Start multiple terminal windows/tabs. You'll need three:

### Terminal 1: Start Celery Worker

```bash
cd /Users/mohaosman/project/remoterep_code_challenge/ad-agency-budget-manager
celery -A src.celery_tasks worker --loglevel=info
```

### Terminal 2: Start Celery Beat

```bash
cd /Users/mohaosman/project/remoterep_code_challenge/ad-agency-budget-manager
celery -A celerybeat-schedule beat --loglevel=info
```

### Terminal 3: Use the CLI to interact with the system

```bash
cd /Users/mohaosman/project/remoterep_code_challenge/ad-agency-budget-manager
```

Now you can try these commands:

1. Initialize a brand with campaigns:

```bash
python src/cli.py init-brand "Nike" 1000 100 --campaign "Morning" 9 17 --campaign "Evening" 18 23 --campaign "AllDay" 0 24
```

2. Update spending:

```bash
python src/cli.py update-spend "Nike" 50
```

3. Check campaign status:

```bash
python src/cli.py check-status
```

4. Reset budgets manually:

```bash
python src/cli.py reset-daily
python src/cli.py reset-monthly
```

5. Run the simulation:

```bash
python src/main.py --simulate --spend 75
```

Test scenarios you might want to try:

1. Exceed daily budget:

```bash
python src/cli.py update-spend "Nike" 101
python src/cli.py check-status
```

2. Exceed monthly budget:

```bash
python src/cli.py update-spend "Nike" 1001
python src/cli.py check-status
```

3. Check dayparting by running status checks at different times of day:

```bash
python src/cli.py check-status
```

The Celery beat scheduler will automatically run tasks to:

- Reset daily budgets at midnight
- Reset monthly budgets on the 1st of each month
- Check campaign status every hour
