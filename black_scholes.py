import numpy as np
from scipy.stats import norm

class BlackScholes:
    def __init__(self, current_price: float, strike: float, time_to_maturity: float, volatility: float, interest_rate: float):
        self.current_price = current_price          # Current price of the underlying asset
        self.strike = strike                        # Strike price of the option
        self.time_to_maturity = time_to_maturity    # Time to maturity (in years)
        self.volatility = volatility                # Volatility of the underlying asset
        self.interest_rate = interest_rate          # Risk-free interest rate

    def _d1(self):
        # Calculate d1 for Black-Scholes formula
        return (np.log(self.current_price / self.strike) + 
                (self.interest_rate + 0.5 * self.volatility**2) * self.time_to_maturity) / \
               (self.volatility * np.sqrt(self.time_to_maturity))

    def _d2(self):
        # Calculate d2 for Black-Scholes formula
        return self._d1() - self.volatility * np.sqrt(self.time_to_maturity)

    def calculate_option_prices(self):
        d1 = self._d1()
        d2 = self._d2()

        # Calculate Call and Put option prices
        call_price = (self.current_price * norm.cdf(d1) - 
                      self.strike * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2))
        put_price = (self.strike * np.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2) - 
                     self.current_price * norm.cdf(-d1))

        return call_price, put_price

    def calculate_greeks(self):
        d1 = self._d1()

        # Calculate Delta for Call and Put options
        call_delta = norm.cdf(d1)
        put_delta = call_delta - 1

        # Calculate Gamma (same for Call and Put)
        gamma = norm.pdf(d1) / (self.current_price * self.volatility * np.sqrt(self.time_to_maturity))

        return {
            "call_delta": call_delta,
            "put_delta": put_delta,
            "gamma": gamma
        }
