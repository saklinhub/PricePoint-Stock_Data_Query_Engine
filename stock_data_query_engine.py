import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def connect_to_db():
    """Connect to SQLite database."""
    try:
        conn = sqlite3.connect('stock_market.db')
        print("Connected to SQLite database 'stock_market.db'")
        return conn
    except sqlite3.Error as err:
        print(f"Error connecting to SQLite: {err}")
        exit(1)

def setup_database(conn):
    """Create stocks table if it doesn't exist."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            Date TEXT,
            Ticker TEXT,
            Open REAL,
            High REAL,
            Low REAL,
            Close REAL,
            Volume INTEGER,
            PRIMARY KEY (Date, Ticker)
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ticker ON stocks (Ticker)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON stocks (Date)')
    conn.commit()
    print("Table 'stocks' created or already exists")
    return cursor

def load_csv_data(conn, cursor,csv_file='stocks.csv'):
    """Load data from CSV into SQLite with validation."""
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"{csv_file} not found. Please ensure the file is in the project directory.")
    
    df = pd.read_csv(csv_file)
    
    # Verify required columns
    required_columns = ['Date','Ticker','Open','High','Low','Close','Volume']
    if not all(col in df.columns for col in required_columns):
        missing = [col for col in required_columns if col not in df.columns]
        raise KeyError(f"Missing required columns: {missing}")
    
    # Validate for Volume column 
    df['Volume'] = pd.to_numeric(df['Volume'],errors='coerce')
    invalid_volumes = df[df['Volume'].isna() | (df['Volume'] < 0)]
    if not invalid_volumes.empty:
        print(f"Warning: Found {len(invalid_volumes)} rows with invalid volumes. Skipping these rows.")
        df = df[df['Volume'].notna() & (df['Volume'] >= 0)]
    
    # Convert Volume to integer
    df['Volume'] = df['Volume'].astype('Int64')
    
    # Ensure Date column is in YYYY-MM-DD format
    df['Date'] = pd.to_datetime(df['Date'],errors='coerce').dt.strftime('%Y-%m-%d')
    if df['Date'].isnull().any():
        raise ValueError("Date column contains invalid or null dates. Please check the CSV data.")
    
    insert_query = '''
        INSERT OR IGNORE INTO stocks (Date,Ticker,Open,High,Low,Close,Volume)
        VALUES (?,?,?,?,?,?,?)
    '''
    try:
        cursor.executemany(insert_query, df[['Date','Ticker','Open','High','Low','Close','Volume']].values.tolist())
        conn.commit()
        print(f"Inserted {cursor.rowcount} rows into 'stocks' table")
    except sqlite3.Error as err:
        print(f"Error inserting data: {err}")
        conn.rollback()
        raise

def validate_date(date_str):
    """Validate date format and return True if valid, False otherwise."""
    try:
        datetime.strptime(date_str,'%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_ticker(cursor,ticker):
    """Check if ticker exists in the database."""
    cursor.execute('SELECT COUNT(*) FROM stocks WHERE Ticker = ?', (ticker,))
    return cursor.fetchone()[0] > 0

def plot_price_trend(cursor, ticker, save_plot=False):
    """Plot closing price trend for a ticker."""
    if not validate_ticker(cursor, ticker):
        print(f"No data found for ticker {ticker}")
        return
    
    cursor.execute('''
        SELECT Date, Close
        FROM stocks
        WHERE Ticker = ?
        ORDER BY Date
    ''',(ticker,))
    data = cursor.fetchall()
    if not data:
        print(f"No data found for {ticker}")
        return
    
    dates = [row[0] for row in data]
    closes = [row[1] for row in data]
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates,closes,label=f'{ticker} Closing Price',color='#1f77b4')
    plt.xlabel('Date')
    plt.ylabel('Closing Price ($)')
    plt.title(f'{ticker} Price Trend')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_plot:
        plt.savefig(f'{ticker}_price_trend.png')
        print(f"Plot saved as {ticker}_price_trend.png")
    plt.show()

def run_queries(cursor, ticker='AAPL', date='2023-01-01'):
    """Run predefined analysis queries."""
    if not validate_ticker(cursor, ticker):
        print(f"Invalid ticker: {ticker}. No data found.")
        return
    

    if not validate_date(date):
        print(f"Invalid date format: {date}. Please use YYYY-MM-DD.")
        return
    
    #Check if date exists in database
    cursor.execute('SELECT COUNT(*) FROM stocks WHERE Date = ?', (date,))
    if cursor.fetchone()[0] == 0:
        print(f"No data found for date {date}")
        return

    #Average closing price
    cursor.execute('''
        SELECT AVG(Close)
        FROM stocks
        WHERE Ticker = ?
    ''', (ticker,))
    avg_close = cursor.fetchone()[0]
    if avg_close is not None:
        print(f"\nAverage closing price for {ticker}: ${avg_close:.2f}")
    else:
        print(f"\nNo closing price data for {ticker}")

    #Top 5 high-volume days
    cursor.execute('''
        SELECT Date, Volume
        FROM stocks
        WHERE Ticker = ?
        ORDER BY Volume DESC
        LIMIT 5
    ''', (ticker,))
    high_volume_days = cursor.fetchall()
    print(f"\nTop 5 high-volume days for {ticker}:")
    if high_volume_days:
        for day in high_volume_days:
            print(f"Date: {day[0]}, Volume: {day[1]}")
    else:
        print("No volume data found.")

    #Price increases on a specific date
    cursor.execute('''
        SELECT Ticker,Open,Close
        FROM stocks
        WHERE Date = ? AND Close > Open
    ''', (date,))
    price_increases = cursor.fetchall()
    print(f"\nStocks with price increase on {date}:")
    if price_increases:
        for stock in price_increases:
            print(f"Ticker: {stock[0]}, Open: ${stock[1]:.2f},Close: ${stock[2]:.2f}")
    else:
        print("No stocks with price increase found.")

    # Query 4: Volatility (standard deviation of closing price)
    cursor.execute('''
        SELECT 
            SQRT(
                AVG((Close - sub.avg_close) * (Close - sub.avg_close))
            ) as stddev
        FROM stocks, 
            (SELECT AVG(Close) as avg_close FROM stocks WHERE Ticker = ?) as sub
        WHERE Ticker = ?
    ''', (ticker, ticker))
    volatility = cursor.fetchone()[0]
    if volatility is not None:
        print(f"\nVolatility (stddev of Close) for {ticker}: ${volatility:.2f}")
    else:
        print(f"\nNo volatility data for {ticker}")

def custom_query(cursor):
    """Allow user to input a custom SQL query."""
    print("\nEnter your custom SQL query (or 'exit' to quit):")
    query = input("> ")
    if query.lower() == 'exit':
        return False
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        if results:
            print("\nQuery Results:")
            for row in results:
                print(row)
        else:
            print("No results returned or query executed successfully (e.g., INSERT/UPDATE).")
        return True
    except sqlite3.Error as err:
        print(f"Error executing query: {err}")
        return True

def main():
    conn = connect_to_db()
    cursor = setup_database(conn)
    
    # Load data
    load_csv_data(conn, cursor)
    
    # Interactive query loop
    while True:
        print("\nPricePoint: Stock Data Query Engine")
        print("1. Run predefined queries")
        print("2. Run custom SQL query")
        print("3. Plot price trend")
        print("4. Exit")
        choice = input("Select an option (1-4): ")
        
        if choice == '1':
            ticker = input("Enter ticker (e.g., AAPL): ") or 'AAPL'
            date = input("Enter date (YYYY-MM-DD, e.g., 2023-01-01): ") or '2023-01-01'
            run_queries(cursor,ticker,date)
        elif choice == '2':
            if not custom_query(cursor):
                break
        elif choice == '3':
            ticker = input("Enter ticker for price trend (e.g., AAPL): ") or 'AAPL'
            save_plot = input("Save plot to file? (y/n): ").lower() == 'y'
            plot_price_trend(cursor,ticker,save_plot)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")
    
    cursor.close()
    conn.close()
    print("\nDatabase connection closed")

if __name__ == "__main__":
    main()