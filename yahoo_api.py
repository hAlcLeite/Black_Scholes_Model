import yfinance as yf

def get_stock_price(ticker: str):
    """
    Fetches the current stock price for a given ticker symbol.
    
    Args:
        ticker (str): The stock ticker symbol (e.g., 'AAPL' for Apple Inc.)
    
    Returns:
        float: The current stock price if the ticker is valid.
        None: If the ticker is invalid or data cannot be fetched.
    """
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.history(period="1d")
        
        if not stock_info.empty:
            return stock_info['Close'].iloc[-1]  # Get the closing price
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None
