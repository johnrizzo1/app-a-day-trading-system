"""Market data acquisition and processing module."""
from typing import Dict, List, Optional
import ccxt
import pandas as pd
from datetime import datetime

class MarketDataService:
    def __init__(self, exchange_id: str = 'binance'):
        self.exchange = getattr(ccxt, exchange_id)()
        
    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1m', limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV (Open, High, Low, Close, Volume) data."""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            raise Exception(f"Error fetching market data: {str(e)}")

    async def fetch_orderbook(self, symbol: str, limit: int = 20) -> Dict:
        """Fetch current orderbook."""
        try:
            return self.exchange.fetch_order_book(symbol, limit=limit)
        except Exception as e:
            raise Exception(f"Error fetching orderbook: {str(e)}")

    def process_raw_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process raw market data."""
        # Add basic technical indicators
        df['sma_20'] = df['close'].rolling(window=20).mean()
        df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['volume_ma'] = df['volume'].rolling(window=20).mean()
        return df
