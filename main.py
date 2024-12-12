#main for project
import pandas as pd
import sys
import os
import random
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries

# Load the API key from the .env file and set variables
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# Create a time series object with the API key and set the output format to pandas
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Get the data for the stock of your choice
stock_ticker = 'NVDA' # Change this to the stock ticker of your choice to pull data for that stock
data_option = 'full'    # Change this to 'full' for entire historical dataset keep 'compact' for the latest 100 data points
data, meta_data = ts.get_daily(symbol= stock_ticker, outputsize= data_option)

# Limit the data to the first 1,000 rows
data = data.head(1000)  # Take the first 1000 data points only

# Print the data
print(f"Data for {stock_ticker} :") 
print(data.head())

# Save to CSV file for further analysis into the CSV_data_copies folder
data.to_csv(f"CSV_data_copies/{stock_ticker}_data.csv", index=True)
print(f"Data saved to {stock_ticker}_data.csv.")

# Calculate Moving Averages and RSI
data['50_MA'] = data['4. close'].rolling(window=50).mean()
data['200_MA'] = data['4. close'].rolling(window=200).mean()

# RSI Calculation
window_length = 14
delta = data['4. close'].diff(1)
gain = (delta.where(delta > 0, 0)).rolling(window=window_length).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=window_length).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# Function to check conditions and notify
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
