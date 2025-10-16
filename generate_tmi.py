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
data = {symbol: yf.download(symbol, start=start_date, end=end_date, interval="1d", auto_adjust=False) for symbol in symbols}

# Ensure all symbols have data
for symbol in symbols:
    if data[symbol].empty:
        raise ValueError(f"No data retrieved for {symbol}")

# Combine data into a single DataFrame with aligned dates
dfs = [data[symbol][["Open", "High", "Low", "Close", "Volume"]].rename(columns=lambda x: f"{symbol}_{x}") for symbol in symbols]
aligned_data = pd.concat(dfs, axis=1, join="inner").dropna()

# Debug: Print column names and sample data
print("Aligned data columns:", aligned_data.columns.tolist())
print("Sample aligned data:", aligned_data.head().to_string())

# Calculate TMI OHLC and volume
tmi_open = aligned_data[[f"{symbol}_Open" for symbol in symbols]].mean(axis=1)
tmi_high = aligned_data[[f"{symbol}_High" for symbol in symbols]].mean(axis=1)
tmi_low = aligned_data[[f"{symbol}_Low" for symbol in symbols]].mean(axis=1)
tmi_close = aligned_data[[f"{symbol}_Close" for symbol in symbols]].mean(axis=1)
tmi_volume = aligned_data[[f"{symbol}_Volume" for symbol in symbols]].sum(axis=1)

# Debug: Print shapes of calculated series
print("tmi_open shape:", tmi_open.shape)
print("tmi_volume shape:", tmi_volume.shape)

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
