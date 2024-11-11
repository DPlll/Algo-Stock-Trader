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
stock_ticker = 'AAPL' # Change this to the stock ticker of your choice to pull data for that stock
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

