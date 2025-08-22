# import pandas as pd
# df = pd.read_csv('all_stocks_5yr.csv')
# df.rename(columns={'Name': 'Ticker'}, inplace=True)
# df.to_csv('stocks.csv', index=False)

# import pandas as pd
# df = pd.read_csv('stocks.csv')  # Or 'all_stocks_5yr.csv'
# print(df.columns)

# import pandas as pd
# df = pd.read_csv('all_stocks_5yr.csv')  # Or your CSV file
# df.rename(columns={'date': 'Date', 'Name': 'Ticker', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
# df.to_csv('stocks.csv', index=False)

import pandas as pd
df = pd.read_csv('stocks.csv')  # Or 'all_stocks_5yr.csv'
print(df.columns)
print(df.head())