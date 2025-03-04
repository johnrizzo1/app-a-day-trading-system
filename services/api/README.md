# API Service

FastAPI-based REST API service for the trading system.

## Features

- RESTful endpoints for all trading operations
- WebSocket support for real-time market data
- JWT authentication and authorization
- OpenAPI documentation
- Rate limiting and request validation
- Database integration with SQLAlchemy

## API Endpoints

### Authentication
- `POST /api/auth/login`: User login
- `POST /api/auth/refresh`: Refresh access token

### Instruments
- `GET /api/instruments/equities`: List available equities
- `GET /api/instruments/bonds`: List available bonds
- `GET /api/instruments/{id}/quote`: Get current quote
- `WS /api/instruments/market-data`: Real-time market data

### Trading
- `POST /api/orders`: Place new order
- `GET /api/orders`: List orders
- `GET /api/positions`: List positions
- `GET /api/portfolio/metrics`: Get portfolio metrics

## Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn src.api.main:app --reload
```

### Testing
```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Configuration

Environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection URL
- `JWT_SECRET`: Secret key for JWT tokens
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

## Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Dependencies

- FastAPI: Web framework
- SQLAlchemy: ORM
- Pydantic: Data validation
- Python-JWT: Authentication
- Redis: Caching and pub/sub
- Uvicorn: ASGI server
