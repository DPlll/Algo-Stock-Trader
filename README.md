# <p align="center">Algorithmic Stock Trader</p>

---

![Logo](b1deb98a-13e6-4496-be39-0d01353a43f4.webp)

<p align="center"> Honors by Contract Term Project for Advance Software Applications for Economics. Use alpha advantage API to collect, organize, and analyze stock data with a basic trading stategy. Then see how your strategy performs with the data collected on desired stock. </p>

---

# Basic Trading Algorithm Project

## Steps to Use

1. **Install Requirements**  
   - Ensure you have Python 3.12.2 installed.  
   - Create and activate a virtual environment:  
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```
   - Install the required dependencies:  
     ```bash
     pip install -r requirements.txt
     ```

2. **Get an AlphaVantage API Key**  
   - Visit [AlphaVantage API Key Signup](https://www.alphavantage.co/support/#api-key) and sign up for a free API key.  

3. **Set Up the `.env` File**  
   - Create a file named `.env` in the project folder.  
   - Add your AlphaVantage API key in this format:  
     ```
     ALPHAVANTAGE_API_KEY=<YOUR_API_KEY>
     ```

4. **Run the Program**  
   - Open the `main.py` file to configure the following settings:  
     - **Stock Ticker:** Change the stock symbol (default is `AAPL`):  
       ```python
       stock_ticker = 'AAPL'
       ```
     - **Data Option:** Choose `full` for full historical data or `compact` for the last 100 data points:  
       ```python
       data_option = 'full'
       ```
     - **Limit Rows:** Adjust the number of rows to analyze (default is 1,000):  
       ```python
       data = data.head(1000)
       ```
   - Save your changes and run the program:  
     ```bash
     python main.py
     ```

5. **Analyze the Results**  
   - The program saves stock data to the `CSV_data_copies` folder.  
   - It also calculates signals (buy/sell) and displays a chart of strategy returns.  

---

### Troubleshooting

- **Missing `.env` File:**  
  If the `.env` file is missing, the program will show:  
  ```plaintext
  Error: .env file not found. Please create a .env file with your API key.


---

## Project Breakdown
The project is divided into three parts, each worth 10 points:

### Data Collection:

Gather data on a stock of your choice from the 'Alphavantage API'.
Collect at least 1,000 data points (daily or intraday) and save them in a 'CSV file' to upload.
### Data Analysis:

Develop a trading strategy using the collected data.
Write a short paper (1-3 pages) in LaTeX, describing:
The stock you selected.
When to buy and sell based on your strategy.
Results of backtesting your strategy (e.g., returns on a $1 investment).
A graph showing your strategy's return over time.
Submit as a PDF.
### Programming:

Provide the Python code used to perform the analysis in Part 2.
Ensure it matches your data and analysis findings, so others can reproduce your results.

---

# Roadmap

Week 1: Setup and Data Collection
Task: Set up Alphavantage API access and decide on a stock.
Milestone: Collect and save 1,000 data points in a CSV file.

Week 2-3: Strategy Development and Backtesting
Task: Design a trading strategy using your data.
Milestone: Complete initial analysis and determine buy/sell points based on patterns or indicators.

Week 4: Writing the Analysis Report
Task: Write a LaTeX document for your strategy analysis.
Milestone: Complete draft, including analysis description, backtesting results, and return graph.

Week 5: Coding and Finalization
Task: Code the strategy in Python based on your analysis.
Milestone: Verify code consistency with your data and backtesting report.

Week 6: Submission
Task: Submit the CSV, LaTeX paper (PDF), and Python code on Blackboard.

---

# Trading Strategies

## 1. Moving Average Crossover Strategy
- **How It Works**: This strategy uses two moving averages—a short-term and a long-term moving average. When the short-term moving average crosses **above** the long-term moving average, it's a **buy** signal. When it crosses **below**, it's a **sell** signal.
- **Implementation**: Calculate the short-term and long-term moving averages (e.g., 50-day and 200-day) and monitor crossovers.

## 2. Relative Strength Index (RSI) Strategy
- **How It Works**: RSI indicates overbought or oversold conditions in the market. RSI values above **70** suggest the stock might be overbought (potential **sell** signal), while values below **30** suggest it might be oversold (potential **buy** signal).
- **Implementation**: Use a time period (usually 14 days) to calculate the RSI, then buy when the RSI falls below 30 and sell when it rises above 70.

## 3. Moving Average Convergence Divergence (MACD)
- **How It Works**: MACD uses the difference between two exponential moving averages (typically the 12-day and 26-day EMAs). It also includes a signal line (usually the 9-day EMA of the MACD).
- **Implementation**: Calculate the MACD line and the signal line. When the MACD line crosses **above** the signal line, it can indicate a **buy**; when it crosses **below**, it’s a potential **sell** signal.

## 4. Mean Reversion Strategy
- **How It Works**: Mean reversion assumes that prices tend to revert to their historical average. If a stock price moves significantly away from its average, it might revert back.
- **Implementation**: Calculate a historical average price (e.g., 30-day moving average). If the current price is significantly **above** this average, consider **selling**; if it's significantly **below**, consider **buying**.

## 5. Bollinger Bands Strategy
- **How It Works**: Bollinger Bands consist of a moving average and two standard deviation lines. When the stock price touches the **upper band**, it may indicate overbought conditions; when it touches the **lower band**, it may indicate oversold conditions.
- **Implementation**: Set up the bands (e.g., 20-day moving average with ±2 standard deviations) and **buy** when the price touches the lower band and **sell** when it touches the upper band.

## 6. Breakout Strategy
- **How It Works**: This strategy is based on price breakout from a defined resistance or support level, assuming it will continue in that direction.
- **Implementation**: Identify support and resistance levels. **Buy** when the price breaks above resistance and **sell** when it breaks below support.

## 7. Trend Following with Simple Moving Average
- **How It Works**: If a stock has been trending upward for an extended period, it may continue that trend. You could apply this by entering when a short-term moving average crosses above a longer-term average, as in a basic trend-following approach.
- **Implementation**: Use the moving averages of your choice (e.g., 50-day and 200-day SMA), setting **buy** and **sell** triggers on crossovers.

---
