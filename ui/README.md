# Windsurf Trading Platform UI

This directory contains the frontend applications for the Windsurf Trading Platform, organized as a monorepo with multiple packages.

## Packages

- **Trading** (`packages/trading`): Trading dashboard for executing and managing orders
- **Backtesting** (`packages/backtesting`): Tools for testing trading strategies against historical data
- **Model Development** (`packages/model-development`): Environment for creating and testing trading models
- **Portfolio Monitor** (`packages/portfolio-monitor`): Dashboard for monitoring portfolio performance
- **Strategy Development** (`packages/strategy-development`): Tools for developing trading strategies

## Prerequisites

- Node.js 20+
- npm 9+

## Setup

1. **Install dependencies**
   ```bash
   cd ui
   npm install
   ```

2. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Development

### Running individual packages

Each package can be run independently:

```bash
# Trading dashboard
cd packages/trading
npm run dev

# Backtesting
cd packages/backtesting
npm run dev

# Model Development
cd packages/model-development
npm run dev

# Portfolio Monitor
cd packages/portfolio-monitor
npm run dev

# Strategy Development
cd packages/strategy-development
npm run dev
```

### Ports

- Trading: http://localhost:3005
- Backtesting: http://localhost:3001
- Model Development: http://localhost:3002
- Portfolio Monitor: http://localhost:3003
- Strategy Development: http://localhost:3004

## Testing

Each package has its own test suite:

```bash
# Run tests for a specific package
cd packages/trading
npm run test

# Run tests with coverage
npm run test:coverage
```

## Building for Production

```bash
# Build a specific package
cd packages/trading
npm run build

# Start production server
npm run start
```

## Project Structure

Each package follows a similar structure:

```
packages/[package-name]/
├── __tests__/          # Test files
├── components/         # React components
├── hooks/              # Custom React hooks
├── pages/              # Next.js pages
├── public/             # Static assets
├── styles/             # CSS styles
├── utils/              # Utility functions
├── .eslintrc.js        # ESLint configuration
├── jest.config.js      # Jest configuration
├── next.config.js      # Next.js configuration
├── package.json        # Package dependencies
└── tsconfig.json       # TypeScript configuration
```

## Shared Components

Common components are shared across packages to maintain UI consistency.

## API Integration

The UI communicates with backend services through RESTful APIs. Each package is configured to proxy API requests to the appropriate backend service.
