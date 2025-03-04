"""Comprehensive market data simulation service for multiple asset classes."""
import asyncio
import json
import random
from datetime import datetime, timedelta
import redis
import numpy as np
from typing import Dict, Any, List
from services.market_simulator.instruments import Equity, Bond, Instrument

class MarketSimulator:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.instruments: Dict[str, Instrument] = {}
        self.prices: Dict[str, float] = {}
        self.market_return = 0.0  # Overall market return for CAPM
        self._initialize_instruments()
        
    def _initialize_instruments(self):
        """Initialize various trading instruments."""
        # Initialize Equities
        equities = [
            ('AAPL', 'Apple Inc.', 180.0, 'Technology', 3e12, 1.2),
            ('MSFT', 'Microsoft Corp.', 350.0, 'Technology', 2.8e12, 1.1),
            ('JPM', 'JPMorgan Chase', 140.0, 'Finance', 400e9, 1.4),
            ('XOM', 'Exxon Mobil', 100.0, 'Energy', 450e9, 0.8)
        ]
        
        for symbol, name, price, sector, mcap, beta in equities:
            self.instruments[symbol] = Equity(symbol, name, price, sector, mcap, beta)
        
        # Initialize Bonds with a sample yield curve
        yield_curve = {1: 0.04, 2: 0.042, 5: 0.045, 10: 0.048, 30: 0.05}
        bonds = [
            ('T-2Y', '2-Year Treasury', 1000.0, 0.042, datetime.now() + timedelta(days=730), 'AAA'),
            ('T-5Y', '5-Year Treasury', 1000.0, 0.045, datetime.now() + timedelta(days=1825), 'AAA'),
            ('T-10Y', '10-Year Treasury', 1000.0, 0.048, datetime.now() + timedelta(days=3650), 'AAA'),
            ('CORP-A', 'Corporate Bond A', 1000.0, 0.06, datetime.now() + timedelta(days=1825), 'A')
        ]
        
        for symbol, name, face_value, coupon, maturity, rating in bonds:
            self.instruments[symbol] = Bond(symbol, name, face_value, coupon, maturity, rating, yield_curve)
        
        # Initialize prices dictionary
        for symbol, instrument in self.instruments.items():
            self.prices[symbol] = instrument.price
    
    @property
    def symbols(self) -> List[str]:
        """Get list of all instrument symbols."""
        return list(self.instruments.keys())
    
    def generate_price_update(self, symbol: str) -> Dict[str, Any]:
        """Generate a simulated price update using GBM."""
        current_price = self.prices[symbol]
        # Geometric Brownian Motion parameters
        mu = 0.0001  # drift
        sigma = 0.001  # volatility
        dt = 1  # time step (1 second)
        
        # Calculate new price
        dW = np.random.normal(0, np.sqrt(dt))
        price_change = current_price * (mu * dt + sigma * dW)
        new_price = current_price + price_change
        
        self.prices[symbol] = new_price
        
        return {
            'symbol': symbol,
            'price': new_price,
            'timestamp': datetime.now().isoformat(),
            'volume': random.uniform(0.1, 10.0)
        }
        
    async def run(self):
        """Run the market simulator."""
        while True:
            for symbol in self.symbols:
                update = self.generate_price_update(symbol)
                self.redis.publish('market_data', json.dumps(update))
            await asyncio.sleep(1)  # Update every second

def main():
    """Run the market simulator."""
    simulator = MarketSimulator('redis://redis:6379')
    asyncio.run(simulator.run())

if __name__ == "__main__":
    main()
