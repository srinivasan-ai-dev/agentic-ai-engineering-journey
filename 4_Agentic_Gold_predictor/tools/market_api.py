import yfinance as yf
def fetch_live_metrics () -> dict:
    
    """
    Fetches the latest closing prices and calculates daily percentage changes.
    """

    # Initialize variables
    tickers = {"gold": "GC=F", "dxy": "DX-Y.NYB", "oil": "CL=F", "yield": "^TNX"} 
    metrics = {} 


    for name, ticker in tickers.items():
        try:
            history = yf.Ticker(ticker).history(period="5d") 
            # Fetch the last 5 days of historical data for the ticker. 
            # it returns a DataFrame with columns like 'Open', 'High', 'Low', 'Close', 'Volume', etc. 
            # We are interested in the 'Close' column for our calculations.

            current_price = history['Close'].iloc[-1] # Get the most recent closing price, which is the last entry in the 'Close' column of the DataFrame.
            previous_price = history['Close'].iloc[-2] # Get the previous closing price, which is the second-to-last entry in the 'Close' column of the DataFrame.
            percentage_change = ((current_price - previous_price) / previous_price) * 100

            metrics[f"{name}_price"] = round(current_price, 2) 
            # Store the current price in the metrics dictionary, rounding it to 2 decimal places for readability. The key is formatted as "{name}_price", where {name} is the name of the asset (e.g., "gold_price").
            metrics[f"{name}_change"] = round(percentage_change, 3)
            # Store the percentage change in the metrics dictionary, rounding it to 3 decimal places for precision. The key is formatted as "{name}_change", where {name} is the name of the asset (e.g., "gold_change").

        except Exception as e:
            metrics[f"{name}_error"] = str(e)
            # If there is an error fetching the data for a particular ticker (e.g., network issues, invalid ticker, etc.), we catch the exception and store the error message in the metrics dictionary with a key formatted as "{name}_error". This way, we can keep track of any issues that arise during the data fetching process without crashing the entire function.

    return metrics



 
