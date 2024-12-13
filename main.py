# Dean Pevey III
# Advanced Software for Economics
# Honors Trading Algorithm Term Project
# main file for project
import pandas as pd
import sys
import os
import random
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries

# Load the API key from the .env file and set variables (you have to obtain your own API key from AlphaVantage & create new .env file to wokr this program)
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# Create a time series object with the API key and set the output format to pandas
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Get the data for the stock of your choice
stock_ticker = 'NVDA' # Change this to the stock ticker of your choice to pull data for that stock
data_option = 'full' # Change this to 'full' for entire historical dataset keep 'compact' for the latest 100 data points
data, meta_data = ts.get_daily(symbol= stock_ticker, outputsize= data_option)

# Limit the data to the first 1,000 rows
data = data.head(1000)  # Take the first 1000 data points only

# Print the Abstracted data view collected from AlphaAdvantage API
print("\nConnection to AlphaAdvantage API successful")
print(f"\nBasic Abstracted Data for {stock_ticker} :") 
print(data.head())

# Save to CSV file for further analysis into the CSV_data_copies folder
data.to_csv(f"CSV_data_copies/{stock_ticker}_data.csv", index=True)
print(f"Data saved to {stock_ticker}_data.csv.")

## ----- Abstarcted data setup ----- ##
# Calculate Moving Averages 
data['50_MA'] = data['4. close'].rolling(window=50).mean()
data['200_MA'] = data['4. close'].rolling(window=200).mean()
# RSI Calculation (also used in the trading signals function)
def calculate_rsi(data, window_length=14):
    delta = data['4. close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window_length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window_length).mean()
    rs = gain / loss.replace(0, float('inf'))  # Prevent division by zero
    return 100 - (100 / (1 + rs))
data['RSI'] = calculate_rsi(data)  # Calculate RSI
# ----- Function to check conditions and notify buy/sell signals ----- #
def check_trading_signals(data):
    last_row = data.iloc[-1]
    prev_row = data.iloc[-2]
    # Print the values to troubleshoot
    print("Last Row 50_MA:", last_row['50_MA'])
    print("Last Row 200_MA:", last_row['200_MA'])
    print("Last Row RSI:", last_row['RSI'])
    # Moving Average Crossover Buy/Sell Signal
    if prev_row['50_MA'] < prev_row['200_MA'] and last_row['50_MA'] > last_row['200_MA']:
        print(f"Buy signal for {stock_ticker} - 50-day MA crossed above 200-day MA.")
    elif prev_row['50_MA'] > prev_row['200_MA'] and last_row['50_MA'] < last_row['200_MA']:
        print(f"Sell signal for {stock_ticker} - 50-day MA crossed below 200-day MA.")
    # RSI Buy/Sell Signal
    if last_row['RSI'] < 30:
        print(f"Buy signal for {stock_ticker} - RSI below 30 (oversold).")
    elif last_row['RSI'] > 70:
        print(f"Sell signal for {stock_ticker} - RSI above 70 (overbought).")

# Run the function to check for signals
check_trading_signals(data)

## ----- Give by and sell signals for RSI based on Historical data ----- ##
# Function to check RSI-based buy/sell signals across all rows, avoiding duplicates and neutralizing signals. Parameters: 
# data (pd.DataFrame): DataFrame with stock prices and RSI values/// stock_ticker (str): Stock ticker symbol for reference in output/// 
# rsi_low (int): Lower RSI threshold for buy signals/// rsi_high (int): Upper RSI threshold for sell signals.
# Returns: list: A list of tuples containing the signal type, date, and details.
def scan_rsi_signals(data, stock_ticker, rsi_low=30, rsi_high=70):
    # Initialize lists for buy and sell signals
    signals = []
    previous_signal = None  # Track the last signal type (Buy/Sell/Neutral)
    # Iterate through the dataset row by row
    for i in range(len(data)):
        rsi = data.iloc[i]['RSI']
        date = data.index[i]
        # Generate Buy Signal
        if rsi < rsi_low and previous_signal != 'Buy':
            signals.append(("Buy", date, f"RSI < {rsi_low}"))
            previous_signal = 'Buy'
        # Generate Sell Signal
        elif rsi > rsi_high and previous_signal != 'Sell':
            signals.append(("Sell", date, f"RSI > {rsi_high}"))
            previous_signal = 'Sell'
        # Reset signal if RSI returns to neutral
        elif rsi_low <= rsi <= rsi_high:
            previous_signal = None
    # Sort signals by date
    signals = sorted(signals, key=lambda x: x[1])
    # Print results
    print("\n" + "=" * 50)
    print(f"Historical RSI Signals for {stock_ticker}".center(50))
    print("=" * 50)
    print(f"{'Signal':<10}{'Date':<30}{'Details':<10}")
    print("-" * 50)
    for signal, date, details in signals:
        print(f"{signal:<10}{str(date):<30}{details}")
    print("=" * 50)

    return signals

print(f"\nScanning historical data collected on {stock_ticker} for RSI signals...\n")
signals = scan_rsi_signals(data, stock_ticker)


## ------ Calculate and graph the strategy returns ------- ##
# Function to calculate and graph returns -> Simulates the returns generated by the buy/sell strategy and graphs the cumulative returns. Parameters:
# data (pd.DataFrame): DataFrame with stock prices and RSI signals/// signals (list): List of tuples containing ('Signal', date, details)/// 
# stock_ticker (str): Stock ticker symbol for reference in the graph.///signals (list): List of tuples containing ('Signal', date, details).
def calculate_and_graph_strategy_returns(data, signals, stock_ticker):
    # Extract closing prices
    closing_prices = data['4. close']
    
    # Initialize variables for tracking
    cumulative_returns = []
    cash = 1  # Start with $1 initial investment
    investment_price = None  # Price at which the last investment was made
    cumulative_value = 1  # Start with $1
    dates = []  # Dates for plotting

    # Process each signal
    for signal, date, details in signals:
        price = closing_prices.loc[date]
        dates.append(date)
        
        if signal == "Buy":
            if investment_price is None:  # Avoid double buying
                investment_price = price  # Invest at the current price
        elif signal == "Sell" and investment_price is not None:
            # Calculate the return from the investment
            profit = (price - investment_price) / investment_price
            cash += cumulative_value * profit
            investment_price = None  # Reset the investment price
            
        # Update cumulative value based on cash and any ongoing investment
        if investment_price is not None:
            # Unrealized value of the current investment
            unrealized_value = cumulative_value * (price / investment_price)
        else:
            # No ongoing investment
            unrealized_value = 0

        cumulative_value = cash + unrealized_value
        cumulative_returns.append(cumulative_value)
        
    # Plot the cumulative returns
    plt.figure(figsize=(10, 6))
    plt.plot(dates, cumulative_returns, label=f"Strategy Returns for {stock_ticker}")
    plt.axhline(y=1, color='gray', linestyle='--', label="Initial Investment")
    plt.title(f"Strategy Cumulative Returns for {stock_ticker}")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Returns ($)")
    plt.legend()
    plt.grid()
    plt.show()
    
    print(f"\nTotal Returns for {stock_ticker}: ${cumulative_value:.2f} (Starting from $1)")

    
# Add to the end of the existing script
print(f"\nScanning historical data collected on {stock_ticker} for RSI signals...\n")
signals = scan_rsi_signals(data, stock_ticker)

# Run the returns calculation and graphing function
calculate_and_graph_strategy_returns(data, signals, stock_ticker)

