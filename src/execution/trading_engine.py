"""Trading execution engine."""
from typing import Dict, Any, Optional
import ccxt
from datetime import datetime

class TradingEngine:
    def __init__(self, exchange_id: str, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.exchange = getattr(ccxt, exchange_id)({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True
        })
        
    async def place_order(self, symbol: str, order_type: str, side: str, 
                         amount: float, price: Optional[float] = None) -> Dict[str, Any]:
        """Place an order on the exchange."""
        try:
            params = {}
            if price:
                return await self.exchange.create_order(symbol, order_type, side, amount, price, params)
            else:
                return await self.exchange.create_order(symbol, order_type, side, amount, params)
        except Exception as e:
            raise Exception(f"Error placing order: {str(e)}")
    
    async def cancel_order(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """Cancel an existing order."""
        try:
            return await self.exchange.cancel_order(order_id, symbol)
        except Exception as e:
            raise Exception(f"Error canceling order: {str(e)}")
    
    async def get_position(self, symbol: str) -> Dict[str, Any]:
        """Get current position for a symbol."""
        try:
            return await self.exchange.fetch_position(symbol)
        except Exception as e:
            raise Exception(f"Error fetching position: {str(e)}")
    
    def update_order_status(self, order_id: str) -> Dict[str, Any]:
        """Update the status of an existing order."""
        try:
            return self.exchange.fetch_order(order_id)
        except Exception as e:
            raise Exception(f"Error updating order status: {str(e)}")
