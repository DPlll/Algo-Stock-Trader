#main for project
import pandas as pd
import sys 
import os
import random
from dotenv import load_dotenv
from alpha_vantage import time_series

# Load the API key from the .env file and set variables
load_dotenv()
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

# Create a time series object
ts = time_series.TimeSeries(key=API_KEY, output_format='pandas')


