# POWEREARNINGSCALE Algorithm

## Overview
The `POWEREARNINGSCALE` algorithm is a quantitative trading strategy designed to analyze earnings gaps and price strength in the days following earnings reports for S&P 500 companies. The algorithm operates from April 30, 2023, to September 2, 2023, starting with a cash balance of $100,000 and aiming to identify promising stock opportunities based on post-earnings performance. Key features include dynamic stock selection, earnings gap analysis, and portfolio diversification.


## Components

### Initialize
- **Set Dates and Cash**: Defines the backtesting period from April 30, 2023, to September 2, 2023, with an initial cash balance of $100,000.
- **Equity and Universe Selection**:
  - SPY is set as the base equity symbol.
  - Adds a universe filter to select stocks with sufficient liquidity and market cap, narrowing down potential stocks with earnings data.
- **Scheduled Action**: Checks the stocks every day, one minute after market open.

### Universe Selection
- **Coarse Filter**: Filters the stock universe to include assets with:
  - Dollar volume greater than $1,000,000,
  - Price over $10,
  - Fundamental data available.
  - The top 500 stocks, sorted by dollar volume, are selected for further filtering.
- **Fine Filter**: Further refines the universe based on:
  - Basic earnings data,
  - Market cap greater than $1 billion.

### Earnings Gap Analysis
- **AfterMarketOpen Method**:
  - Loops through the filtered stocks, excluding SPY.
  - Requests historical data for the past 7 days to access open, close, and high prices after earnings.
  - **Gap Calculation**:
    - Calculates the price gap and the percentage change between the close before and open after earnings.
    - Measures close strength, determining if the price closed strong or faded.
  - **Conditions for Stock Analysis**:
    - If the price gap is greater than 5%, the algorithm evaluates whether the stock closed strong or faded.

### Portfolio Management
- **OnData Method**:
  - Sets portfolio holdings in three symbols (SPY, BND, AAPL) with a balanced allocation of 33% each, provided the portfolio has no active investments.

## Logging and Debugging
- Uses `self.Debug()` statements to provide insights during the algorithm's operation, especially when history data is unavailable or specific earnings gap conditions are met.

## Dependencies
- The algorithm relies on the `AlgorithmImports` library from QuantConnect.

## Execution Summary
This algorithm identifies stocks with significant earnings gaps and assesses post-earnings price strength to inform potential investments. With a diversified approach and careful earnings analysis, it seeks to capitalize on market trends around earnings reports.
