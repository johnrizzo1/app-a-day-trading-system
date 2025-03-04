# Worker Service

Celery-based worker service for handling background tasks and scheduled operations.

## Features

- Order execution and management
- Portfolio metrics calculation
- Corporate actions processing
- Scheduled task execution
- Event-driven processing

## Tasks

### Trading Operations
- Order execution
- Position updates
- Trade settlement
- Risk calculations

### Portfolio Management
- Portfolio valuation
- Performance metrics
- Asset allocation
- Risk analytics

### Corporate Actions
- Dividend processing
- Stock splits
- Bond coupon payments
- Rights issues

### Scheduled Tasks
- Daily portfolio valuation
- Market data aggregation
- Performance reporting
- Risk limit checks

## Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start Celery worker
celery -A worker.tasks worker --loglevel=info

# Start Celery beat (for scheduled tasks)
celery -A worker.tasks beat --loglevel=info
```

### Testing
```bash
# Run tests
pytest tests/

# Test specific task
pytest tests/test_order_execution.py
```

## Configuration

Environment variables:
- `REDIS_URL`: Redis broker URL
- `DATABASE_URL`: PostgreSQL connection string
- `CELERY_TASK_ALWAYS_EAGER`: Run tasks synchronously (testing)
- `C_FORCE_ROOT`: Allow running as root (containerized)

## Task Scheduling

Example schedule configuration:
```python
app.conf.beat_schedule = {
    'calculate-portfolio-metrics': {
        'task': 'worker.tasks.calculate_portfolio_metrics',
        'schedule': crontab(minute='*/15'),
    },
    'process-corporate-actions': {
        'task': 'worker.tasks.process_corporate_actions',
        'schedule': crontab(hour='0', minute='0'),
    },
}
```

## Dependencies

- Celery: Task queue
- Redis: Message broker
- SQLAlchemy: Database ORM
- NumPy: Numerical computations
- Pandas: Data analysis
