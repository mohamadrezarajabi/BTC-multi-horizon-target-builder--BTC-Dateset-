import pandas as pd
import zipfile
import glob

files = glob.glob("BTCUSDT-1h-2025-*.zip")

dfs = []

for file in sorted(files):
    with zipfile.ZipFile(file) as z:
        csv_file = z.namelist()[0]
        df = pd.read_csv(z.open(csv_file), header=None)
        dfs.append(df)

data = pd.concat(dfs, ignore_index=True)

data.columns = [
    'open_time','open','high','low','close','volume',
    'close_time','quote_volume','trades',
    'taker_buy_base','taker_buy_quote','ignore'
]

# تبدیل open_time از میکروثانیه به میلی‌ثانیه
data['open_time'] = pd.to_numeric(data['open_time'], errors='coerce') // 1000

# تبدیل datetime
data['open_time'] = pd.to_datetime(data['open_time'], unit='ms')

# پاکسازی ستون‌های عددی
numeric_cols = ['open','high','low','close','volume','trades','taker_buy_base']
for col in numeric_cols:
    data[col] = pd.to_numeric(data[col], errors='coerce')

data = data.dropna(subset=['close'])

print(data.head())
print(data.tail())

data.to_csv("BTCUSDT_1h_2025_clean.csv", index=False)
print("Saved successfully.")
