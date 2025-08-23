-----
# Stock Data Query Engine

## Overview
The **Stock Data Query Engine** is a Python-based tool for analyzing stock market data stored in a SQLite database. It allows users to load stock data from a CSV file, run predefined analytical queries, execute custom SQL queries, and visualize stock price trends using matplotlib. The tool is designed for simplicity and flexibility, making it suitable for financial data analysis and experimentation.

### Features
- **Data Loading**: Import stock data from a CSV file into a SQLite database with robust validation.
- **Predefined Queries**: Analyze average closing prices, high-volume days, price increases, and volatility for specific stocks.
- **Custom Queries**: Execute user-defined SQL queries for flexible data exploration.
- **Visualization**: Generate plots of stock price trends with an option to save them as images.
- **Error Handling**: Includes validation for tickers, dates, and data integrity to ensure reliable operation.

## Requirements
- Python 3.8+
- Libraries:
  - `sqlite3` (built-in)
  - `pandas`
  - `matplotlib`
- A CSV file (`stocks.csv`) with the following columns:
  - `Date` (YYYY-MM-DD format)
  - `Ticker` (stock symbol, e.g., AAPL)
  - `Open` (opening price)
  - `High` (highest price)
  - `Low` (lowest price)
  - `Close` (closing price)
  - `Volume` (trading volume, non-negative integer)

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/stock-data-query-engine.git
   cd stock-data-query-engine

2. **Install Dependencies**:
   ```bash
   pip install pandas matplotlib

3. **Prepare the CSV File**:Ensure a stocks.csv file is in the project directory with the required columns. Example format:
   ```csv
   Date,Ticker,Open,High,Low,Close,Volume
   2023-01-01,AAPL,130.28,132.67,129.04,130.90,112117500
   2023-01-02,AAPL,130.90,133.15,128.90,129.60,105435600

 ## Usage
 1. **Run the Script**:
    ```bash
    python stock_data_query_engine.py

 2. **Interective Menu**:The script provides an interactive command-line interface with the following options:
    - **Option 1: Run Predefined Queries**
      - Prompts for a ticker (e.g., AAPL) and date (e.g., 2023-01-01).
      - Outputs average closing price, top 5 high-volume days, stocks with price increases on the specified date, and volatility (standard deviation of closing price).
    - **Option 2: Run Custom SQL Query**
      - Allows you to input a custom SQL query to explore the `stocks` table.
    - **Option 3: Plot Price Trend**
      - Allows you to input a custom SQL query to explore the stocks table.
    - **Option 4: Exit**
      - Closes the database connection and exits the program.

3. **Example Commands**:
   - To run predefined queries for Apple's stock on January 1, 2023:
     ```plain
     Select an option (1-4): 1
     Enter ticker (e.g., AAPL): AAPL
     Enter date (YYYY-MM-DD, e.g., 2023-01-01): 2023-01-01

   - To plot the price trend for Microsoft:
     ```plain
     Select an option (1-4): 3
     Enter ticker for price trend (e.g., AAPL): MSFT
     Save plot to file? (y/n): y

## Database Schema
The SQLite database (`stock_market.db`) contains a single table, `stocks`, with the following schema:
```sql
CREATE TABLE stocks (
    Date TEXT,
    Ticker TEXT,
    Open REAL,
    High REAL,
    Low REAL,
    Close REAL,
    Volume INTEGER,
    PRIMARY KEY (Date, Ticker)
);
- Indexes are created on Ticker and Date for efficient querying.
```

## Notes
  - Ensure the `stocks.csv` file is correctly formatted to avoid data loading errors.
  - Invalid tickers or dates will be handled gracefully with appropriate error messages.
  - The `Volume` column in the CSV must contain non-negative numeric values.
  - Plots can be saved as PNG files for use in reports or further analysis.
  - The volatility calculation uses a custom SQL query to compute the standard deviation, as SQLite does not support `STDEV`.

## Contributing
Contributions are welcome! To contribute:
 1. Fork the repository.
 2. Create a new branch (`git checkout -b feature-branch`).
 3. Make your changes and commit (`git commit -m "Add feature"`).
 4. Push to the branch (`git push origin feature-branch`).
 5. Open a pull request.


    
 
