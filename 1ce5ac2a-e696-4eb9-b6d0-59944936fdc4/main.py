from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, OBV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the stock ticker here
        self.ticker = "MNGO"  # Assuming 'MNGO' as the ticker for the Mango stock
        self.rsi_length = 14  # Typical period for RSI calculation
        self.obv_length = 0  # Length is set to 0 since OBV doesn't require a length; removing ambiguity

    @property
    def assets(self):
        # Return a list of assets the strategy is interested in
        return [self.ticker]

    @property
    def interval(self):
        # Define the data interval (daily, hourly, etc.)
        return "1day"

    def run(self, data):
        # Main logic of the strategy
        allocation = {self.ticker: 0}  # Default to 0 allocation

        # Ensure there's enough data for analysis
        if len(data["ohlcv"]) > self.rsi_length:
            # Calculate RSI
            rsi_values = RSI(self.ticker, data["ohlcv"], self.rsi_length)
            # Calculate OBV; since we are not passing length, it computes OBV over all available data
            obv_values = OBV(self.ticker, data["ohlcv"], self.obv_length)
            
            # Check if both conditions for a bullish outlook are met:
            # 1. RSI is less than 70, indicating the stock is not overbought.
            # 2. OBV is increasing, indicating buying pressure.
            if rsi_values[-1] < 70 and obv_values[-1] > obv_values[-2]:
                log(f"Bullish outlook on {self.ticker}: RSI and OBV conditions met.")
                allocation[self.ticker] = 0.1  # Allocate 10% as an example
            
            # Logging for analysis
            log(f"RSI: {rsi_values[-1]}, OBV change: {obv_values[-1] - obv_values[-2]}")
        
        return TargetAllocation(allocation)