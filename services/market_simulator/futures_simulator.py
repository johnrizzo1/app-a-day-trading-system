"""Futures market simulator."""
import asyncio
import json
from datetime import datetime, timedelta
import redis
import numpy as np
from typing import Dict, Any, List

class FuturesContract:
    def __init__(self, symbol: str, expiry: datetime, initial_price: float,
                 tick_size: float, contract_size: float):
        self.symbol = symbol
        self.expiry = expiry
        self.price = initial_price
        self.tick_size = tick_size
        self.contract_size = contract_size
        self.funding_rate = 0.0001  # 0.01% funding rate
        self.last_funding = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'symbol': self.symbol,
            'expiry': self.expiry.isoformat(),
            'price': self.price,
            'tick_size': self.tick_size,
            'contract_size': self.contract_size,
            'funding_rate': self.funding_rate
        }

class FuturesSimulator:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.contracts: Dict[str, FuturesContract] = {}
        self._initialize_contracts()
        
    def _initialize_contracts(self):
        """Initialize futures contracts with different expiries."""
        base_assets = ['BTC', 'ETH', 'SOL']
        expiries = [
            datetime.now() + timedelta(days=30),  # Monthly
            datetime.now() + timedelta(days=90),  # Quarterly
            datetime.now() + timedelta(days=180)  # Bi-annual
        ]
        
        for asset in base_assets:
            for expiry in expiries:
                symbol = f"{asset}-PERP"  # Perpetual
                self.contracts[symbol] = FuturesContract(
                    symbol=symbol,
                    expiry=expiry,
                    initial_price=self._get_initial_price(asset),
                    tick_size=0.1,
                    contract_size=1.0
                )
                
    def _get_initial_price(self, asset: str) -> float:
        """Get initial price for an asset."""
        prices = {
            'BTC': 50000.0,
            'ETH': 3000.0,
            'SOL': 100.0
        }
        return prices.get(asset, 100.0)
        
    def _calculate_price_impact(self, base_price: float, volume: float) -> float:
        """Calculate price impact based on volume."""
        impact_factor = 0.0001  # 0.01% impact per unit of volume
        return base_price * (1 + impact_factor * volume)
        
    def _update_funding_rates(self):
        """Update funding rates for perpetual contracts."""
        current_time = datetime.now()
        for contract in self.contracts.values():
            if '-PERP' in contract.symbol:
                # Update funding rate every 8 hours
                if (current_time - contract.last_funding).total_seconds() >= 8 * 3600:
                    # Simulate funding rate based on price deviation from spot
                    contract.funding_rate = np.random.normal(0.0001, 0.0002)
                    contract.last_funding = current_time
        
    def generate_price_updates(self) -> List[Dict[str, Any]]:
        """Generate price updates for all contracts."""
        updates = []
        self._update_funding_rates()
        
        for contract in self.contracts.values():
            # Base price movement
            mu = 0.0001  # drift
            sigma = 0.001  # volatility
            dt = 1  # time step (1 second)
            
            # Add time decay for non-perpetual contracts
            if '-PERP' not in contract.symbol:
                time_to_expiry = (contract.expiry - datetime.now()).total_seconds()
                if time_to_expiry > 0:
                    theta = 0.0001  # time decay factor
                    mu -= theta
            
            # Calculate price movement
            dW = np.random.normal(0, np.sqrt(dt))
            price_change = contract.price * (mu * dt + sigma * dW)
            
            # Simulate random volume
            volume = np.random.exponential(10.0)
            
            # Apply price impact
            new_price = contract.price + price_change
            new_price = self._calculate_price_impact(new_price, volume)
            
            # Round to tick size
            new_price = round(new_price / contract.tick_size) * contract.tick_size
            
            contract.price = new_price
            
            updates.append({
                'contract': contract.to_dict(),
                'timestamp': datetime.now().isoformat(),
                'volume': volume,
                'open_interest': np.random.randint(1000, 10000)
            })
            
        return updates
        
    async def run(self):
        """Run the futures market simulator."""
        while True:
            updates = self.generate_price_updates()
            for update in updates:
                self.redis.publish('futures_market_data', json.dumps(update))
            await asyncio.sleep(1)  # Update every second

if __name__ == "__main__":
    simulator = FuturesSimulator('redis://redis:6379')
    asyncio.run(simulator.run())
