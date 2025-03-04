"""Risk management system."""
from typing import Dict, Any, List
import pandas as pd
from datetime import datetime

class RiskManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.position_limits = config.get('position_limits', {})
        self.risk_limits = config.get('risk_limits', {})
        self.positions = {}
        
    def check_order(self, order: Dict[str, Any]) -> bool:
        """Validate if an order meets risk parameters."""
        symbol = order['symbol']
        amount = order['amount']
        
        # Check position limits
        if symbol in self.positions:
            new_position = self.positions[symbol] + amount
            if abs(new_position) > self.position_limits.get(symbol, float('inf')):
                return False
                
        # Check order size
        if amount > self.risk_limits.get('max_order_size', float('inf')):
            return False
            
        return True
        
    def calculate_var(self, positions: Dict[str, float], 
                     price_history: pd.DataFrame, 
                     confidence_level: float = 0.95) -> float:
        """Calculate Value at Risk for current positions."""
        returns = price_history.pct_change().dropna()
        var = returns.quantile(1 - confidence_level)
        position_value = sum(pos * price_history[sym].iloc[-1] 
                           for sym, pos in positions.items())
        return abs(var * position_value)
        
    def update_positions(self, positions: Dict[str, float]):
        """Update current positions."""
        self.positions = positions
        
    def get_risk_metrics(self) -> Dict[str, Any]:
        """Calculate current risk metrics."""
        return {
            'total_exposure': sum(abs(pos) for pos in self.positions.values()),
            'position_count': len(self.positions),
            'timestamp': datetime.now()
        }
