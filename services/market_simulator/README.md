# Market Simulator Service

Real-time market data simulation service supporting multiple asset classes.

## Features

- Multi-asset class support:
  - Equities with dividend processing
  - Bonds with yield curve analysis
  - Futures with funding rates
- Real-time price simulation using stochastic models
- Corporate actions simulation
- WebSocket streaming
- Redis pub/sub integration

## Price Models

### Equity Simulation
- CAPM-based price movements
- Beta-adjusted market correlation
- Dividend payment processing
- Volume simulation based on market cap

### Bond Simulation
- Yield curve based pricing
- Credit rating impact
- Coupon payment processing
- Duration and convexity effects

### Futures Simulation
- Funding rate calculations
- Mark price computation
- Open interest simulation
- Volume profile generation

## Configuration

Environment variables:
- `REDIS_URL`: Redis connection URL
- `SIMULATION_INTERVAL`: Update interval in seconds
- `MARKET_VOLATILITY`: Base market volatility
- `LOG_LEVEL`: Logging level

## Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run simulator
python -m market_simulator.market_simulator
```

### Testing
```bash
# Run tests
pytest tests/

# Run specific test file
pytest tests/test_price_models.py
```

## Architecture

### Components

1. **Price Generator**
   - Implements stochastic price models
   - Handles corporate actions
   - Manages market correlations

2. **Market State Manager**
   - Tracks instrument states
   - Manages trading sessions
   - Handles market events

3. **Data Publisher**
   - WebSocket streaming
   - Redis pub/sub
   - Event broadcasting

## Dependencies

- NumPy: Mathematical computations
- Pandas: Data manipulation
- Redis: Message broker
- WebSockets: Real-time streaming
