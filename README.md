# Multi-Asset Trading System

A comprehensive trading system supporting multiple asset classes including Equities, Bonds, and Futures, with real-time market data simulation and automated trading capabilities.

## Features

- **Multi-Asset Support**
  - Equities trading with dividend processing
  - Bond trading with yield curve analysis
  - Futures trading with funding rate calculations

- **Market Operations**
  - Real-time market data simulation
  - Order execution and management
  - Portfolio tracking and analytics
  - Corporate actions processing

- **Technical Infrastructure**
  - RESTful API with WebSocket support
  - Automated task scheduling
  - Database migrations and versioning
  - Containerized microservices

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 20+
- direnv (for environment management)

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd windsurf-project
   direnv allow
   ./scripts/setup.sh
   ```

2. **Start Services**
   ```bash
   docker-compose up -d
   ```

3. **Run Initial Migration**
   ```bash
   docker-compose run --rm migrate alembic upgrade head
   ```

4. **Verify Services**
   ```bash
   docker-compose ps
   ```

## Development Guide

### Environment Configuration

1. **Initialize Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Environment Variables**
   - `DATABASE_URL`: PostgreSQL connection string
   - `REDIS_URL`: Redis connection URL
   - `JWT_SECRET`: API security key
   - `ENVIRONMENT`: development/production

### Database Management

1. **Create Migration**
   ```bash
   docker-compose run --rm migrate alembic revision \
     --autogenerate -m "description"
   ```

2. **Apply Migration**
   ```bash
   docker-compose run --rm migrate alembic upgrade head
   ```

3. **Rollback Migration**
   ```bash
   docker-compose run --rm migrate alembic downgrade -1
   ```

### Testing

1. **Unit Tests**
   ```bash
   docker-compose run --rm api pytest tests/unit
   ```

2. **Integration Tests**
   ```bash
   docker-compose run --rm api pytest tests/integration
   ```

3. **Coverage Report**
   ```bash
   docker-compose run --rm api pytest --cov=src tests/
   ```

### Service Management

1. **View Logs**
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f api
   ```

2. **Restart Services**
   ```bash
   docker-compose restart [service_name]
   ```

3. **Rebuild Services**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

## Project Structure

```
├── migrations/          # Database migrations
├── scripts/            # Utility scripts
├── services/           # Microservices
│   ├── api/           # REST API service
│   ├── market_simulator/# Market data simulation
│   └── worker/        # Background tasks
├── src/               # Core application code
│   ├── api/          # API endpoints
│   ├── database/     # Database models
│   └── utils/        # Shared utilities
├── tests/             # Test suite
└── ui/                # Frontend application
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Architecture

### Microservices

1. **API Service**
   - FastAPI-based REST API
   - JWT authentication
   - WebSocket support

2. **Market Simulator**
   - Real-time price simulation
   - Multiple asset class support
   - Corporate actions simulation

3. **Worker Service**
   - Order execution
   - Portfolio calculations
   - Scheduled tasks

### Infrastructure

- **PostgreSQL**: Primary database
- **Redis**: Caching and message broker
- **Celery**: Task queue and scheduling
- **Alembic**: Database migrations

## Monitoring

1. **Service Health**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Metrics Dashboard**
   ```bash
   docker-compose up -d grafana
   # Visit http://localhost:3000
   ```

## Troubleshooting

1. **Database Issues**
   ```bash
   # Reset database
   docker-compose down -v
   docker-compose up -d postgres
   docker-compose run --rm migrate alembic upgrade head
   ```

2. **Service Errors**
   ```bash
   # Check logs
   docker-compose logs -f --tail=100 [service_name]
   
   # Restart service
   docker-compose restart [service_name]
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Run tests
5. Submit pull request

## License

MIT License - see LICENSE file for details
