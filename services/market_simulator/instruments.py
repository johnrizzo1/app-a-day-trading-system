"""Market instruments for simulation."""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import numpy as np

class Instrument:
    def __init__(self, symbol: str, name: str, initial_price: float):
        self.symbol = symbol
        self.name = name
        self.price = initial_price
        self.last_update = datetime.now()
        
    def update_price(self, dt: float) -> float:
        """Base price update method."""
        raise NotImplementedError
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'timestamp': datetime.now().isoformat()
        }

class Equity(Instrument):
    def __init__(self, symbol: str, name: str, initial_price: float,
                 sector: str, market_cap: float, beta: float = 1.0):
        super().__init__(symbol, name, initial_price)
        self.sector = sector
        self.market_cap = market_cap
        self.beta = beta
        self.dividend_yield = 0.02  # 2% annual dividend yield
        self.next_dividend_date = datetime.now() + timedelta(days=90)
        
    def update_price(self, dt: float, market_return: float = 0.0) -> float:
        # CAPM-inspired price movement
        mu = 0.0001 + self.beta * market_return  # drift affected by market
        sigma = 0.001 * (1 + abs(self.beta))  # volatility scaled by beta
        
        dW = np.random.normal(0, np.sqrt(dt))
        price_change = self.price * (mu * dt + sigma * dW)
        self.price += price_change
        
        # Check for dividend payment
        if datetime.now() >= self.next_dividend_date:
            dividend = self.price * (self.dividend_yield / 4)  # Quarterly dividend
            self.price -= dividend
            self.next_dividend_date += timedelta(days=90)
        
        return self.price
        
    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            'type': 'equity',
            'sector': self.sector,
            'market_cap': self.market_cap,
            'beta': self.beta,
            'dividend_yield': self.dividend_yield,
            'next_dividend_date': self.next_dividend_date.isoformat()
        })
        return base_dict

class Bond(Instrument):
    def __init__(self, symbol: str, name: str, face_value: float,
                 coupon_rate: float, maturity_date: datetime,
                 credit_rating: str, yield_curve: Dict[str, float]):
        super().__init__(symbol, name, face_value)
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.maturity_date = maturity_date
        self.credit_rating = credit_rating
        self.yield_curve = yield_curve
        self.payment_frequency = 2  # Semi-annual payments
        self.next_coupon_date = datetime.now() + timedelta(days=180)
        
    def calculate_ytm(self) -> float:
        """Calculate Yield to Maturity."""
        time_to_maturity = (self.maturity_date - datetime.now()).days / 365
        if time_to_maturity <= 0:
            return 0
        
        # Interpolate from yield curve
        years = list(self.yield_curve.keys())
        rates = list(self.yield_curve.values())
        return np.interp(time_to_maturity, years, rates)
        
    def update_price(self, dt: float) -> float:
        ytm = self.calculate_ytm()
        time_to_maturity = (self.maturity_date - datetime.now()).days / 365
        
        if time_to_maturity <= 0:
            self.price = self.face_value
            return self.price
            
        # Calculate bond price using present value of cash flows
        price = 0
        coupon_payment = self.face_value * self.coupon_rate / self.payment_frequency
        
        for t in range(1, int(time_to_maturity * self.payment_frequency) + 1):
            t_years = t / self.payment_frequency
            discount_factor = 1 / (1 + ytm/self.payment_frequency) ** t
            price += coupon_payment * discount_factor
            
        # Add present value of principal
        price += self.face_value * (1 / (1 + ytm) ** time_to_maturity)
        
        # Add some noise to the price
        noise = np.random.normal(0, 0.0001 * price)
        self.price = price + noise
        
        # Process coupon payments
        if datetime.now() >= self.next_coupon_date:
            self.price -= coupon_payment
            self.next_coupon_date += timedelta(days=180)
        
        return self.price
        
    def to_dict(self) -> Dict[str, Any]:
        base_dict = super().to_dict()
        base_dict.update({
            'type': 'bond',
            'face_value': self.face_value,
            'coupon_rate': self.coupon_rate,
            'maturity_date': self.maturity_date.isoformat(),
            'credit_rating': self.credit_rating,
            'ytm': self.calculate_ytm(),
            'next_coupon_date': self.next_coupon_date.isoformat()
        })
        return base_dict
