import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# Define symbols and weights
symbols = ["ES=F", "NQ=F", "RTY=F", "YM=F"]  # Yahoo Finance tickers for ES1!, NQ1!, RTY1!, YM1!
weight = 0.25  # Equal weight (25%)

# Fetch historical data (1 year)
end_date = datetime.now()
start_date = datetime(end_date.year - 1, end_date.month, end_date.day)
data = {symbol: yf.download(symbol, start=start_date, end=end_date, interval="1d") for symbol in symbols}

# Ensure all symbols have data
for symbol in symbols:
    if data[symbol].empty:
        raise ValueError(f"No data retrieved for {symbol}")

# Align dates across symbols
dfs = [data[symbol][["Open", "High", "Low", "Close", "Volume"]] for symbol in symbols]
aligned_data = pd.concat(dfs, axis=1, keys=symbols, join="inner").dropna()

# Calculate TMI OHLC and volume
tmi_open = sum(aligned_data[(symbol, "Open")] * weight for symbol in symbols)
tmi_high = sum(aligned_data[(symbol, "High")] * weight for symbol in symbols)
tmi_low = sum(aligned_data[(symbol, "Low")] * weight for symbol in symbols)
tmi_close = sum(aligned_data[(symbol, "Close")] * weight for symbol in symbols)
tmi_volume = sum(aligned_data[(symbol, "Volume")] for symbol in symbols)

# Create TMI DataFrame
tmi_df = pd.DataFrame({
    "time": aligned_data.index.strftime("%Y-%m-%d"),
    "open": tmi_open,
    "high": tmi_high,
    "low": tmi_low,
    "close": tmi_close,
    "volume": tmi_volume
})

# Save to CSV in 'data' folder
os.makedirs("data", exist_ok=True)
csv_path = "data/TMI.csv"
tmi_df.to_csv(csv_path, index=False)
print(f"TMI CSV saved to {csv_path}")
