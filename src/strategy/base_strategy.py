"""Base strategy implementation."""
from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd
from datetime import datetime

class BaseStrategy(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.position = 0
        self.signals = []
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """Generate trading signals from market data."""
        pass
    
    def calculate_position_size(self, signal: float, price: float, balance: float) -> float:
        """Calculate position size based on signal strength and risk parameters."""
        max_position = balance * self.config.get('max_position_size', 0.1)
        return signal * max_position / price
    
    def update(self, market_data: pd.DataFrame) -> Dict[str, Any]:
        """Update strategy state with new market data."""
        signal = self.generate_signals(market_data)
        current_price = market_data['close'].iloc[-1]
        
        return {
            'signal': signal.iloc[-1] if isinstance(signal, pd.Series) else signal,
            'current_price': current_price,
            'timestamp': datetime.now(),
            'position': self.position
        }
