# Windsurf Trading Dashboard

The Trading Dashboard is a real-time interface for executing trades, managing orders, and monitoring market data across multiple asset classes.

## Features

- **Order Management**
  - Create market, limit, and stop orders
  - View and cancel active orders
  - Track order history and execution details

- **Market Data**
  - Real-time price updates
  - Historical price charts
  - Order book visualization

- **Portfolio Overview**
  - Current positions and exposure
  - P&L tracking
  - Risk metrics

- **Multi-Asset Support**
  - Equities
  - Bonds
  - Futures contracts

## Prerequisites

- Node.js 20+
- npm 9+

## Setup

1. **Install dependencies**
   ```bash
   cd ui/packages/trading
   npm install
   ```

2. **Setup environment variables**
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your settings
   ```

## Development

### Running the application

```bash
# Development mode
npm run dev

# Production build
npm run build
npm run start
```

The application will be available at http://localhost:3005.

## Testing

The Trading Dashboard includes comprehensive test coverage using Jest and React Testing Library.

```bash
# Run tests
npm run test

# Run tests with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

### Test Structure

Tests are organized in the `__tests__` directory, mirroring the structure of the source code:

```
__tests__/
├── components/     # Component tests
├── hooks/          # Hook tests
├── pages/          # Page tests
└── utils/          # Utility function tests
```

## API Integration

The Trading Dashboard communicates with backend services through the following endpoints:

- `/api/trading/contracts` - Get available contracts
- `/api/trading/orders` - Manage orders (GET, POST)
- `/api/trading/orders/{orderId}/cancel` - Cancel an order
- `/api/trading/market-data` - Get real-time market data

## Project Structure

```
├── __tests__/          # Test files
├── components/         # React components
│   ├── Layout.tsx      # Main layout component
│   └── NavBar.tsx      # Navigation bar
├── hooks/              # Custom React hooks
├── pages/              # Next.js pages
│   ├── _app.tsx        # App wrapper
│   ├── index.tsx       # Trading dashboard
│   ├── simple.tsx      # Simplified view
│   ├── minimal.js      # Minimal interface
│   └── standalone.js   # Standalone mode
├── public/             # Static assets
├── styles/             # CSS styles
├── utils/              # Utility functions
├── jest.config.js      # Jest configuration
├── jest.setup.js       # Jest setup
└── next.config.js      # Next.js configuration
```

## Troubleshooting

### Common Issues

1. **Invalid Hook Call Error**
   - Ensure React version is consistent across all dependencies
   - Verify hooks are only called at the top level of functional components
   - Check for multiple instances of React in the dependency tree

2. **API Connection Issues**
   - Verify the backend services are running
   - Check the API proxy configuration in `next.config.js`
   - Ensure environment variables are set correctly
