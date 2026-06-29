import numpy as np
import pandas as pd
import os
from download_btc_dataset import get_output_file

# -------------------
# دریافت ورودی از کاربر
# -------------------
SYMBOL = input("Symbol: ").strip().upper()
if not SYMBOL.endswith("USDT"):
    SYMBOL += "USDT"

INTERVAL = input("TimeFrame: ").strip().lower()

# -------------------
# Load Data
# -------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Fix: pass SYMBOL and INTERVAL as arguments to the function
input_file = get_output_file(SYMBOL, INTERVAL)

csv_path = os.path.join(BASE_DIR, input_file)
if not os.path.exists(csv_path):
    raise FileNotFoundError(
        f"❌ File not found: {csv_path}\n"
        f"   Run download_btc_dataset.py first to generate the raw CSV."
    )

data = pd.read_csv(csv_path)
df = data.copy()

# اطمینان از عددی بودن close
df["close"] = pd.to_numeric(df["close"], errors="coerce")

# مرتب بودن دیتا از قدیم به جدید (خیلی مهم)
df = df.sort_values("open_time").reset_index(drop=True)

# -------------------
# 1️⃣ Log return لحظه‌ای (time frame)
# -------------------
df["log_return_1h"] = np.log(df["close"] / df["close"].shift(1))

# -------------------
# 2️⃣ Horizons
# -------------------
horizons = {
    "4h": 4,
    "6h": 6,
    "12h": 12,
    "24h": 24,
    "7d": 168,
}

for name, step in horizons.items():
    future_price = df["close"].shift(-step)

    # ✅ Simple Return
    df[f"return_{name}"] = (future_price - df["close"]) / df["close"]

    # ✅ Log Return
    df[f"logreturn_{name}"] = np.log(future_price / df["close"])

    # ✅ Direction
    df[f"direction_{name}"] = (future_price > df["close"]).astype(int)

    # ✅ 3% Move Classification
    df[f"up3pct_{name}"] = (future_price >= df["close"] * 1.03).astype(int)

# -------------------
# حذف ردیف‌های انتهایی که future ندارند
# -------------------
df = df.dropna().reset_index(drop=True)

# -------------------
# Save
# -------------------
output_file = f"{SYMBOL}_{INTERVAL}_targets_ready.csv"
df.to_csv(os.path.join(BASE_DIR, output_file), index=False)

print("✅ Targets created successfully.")
print(f"Saved to: {output_file}")
print(f"Total rows: {len(df):,}")
print(df[["open_time", "close", "log_return_1h", "direction_24h", "up3pct_7d"]].head())