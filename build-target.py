import numpy as np
import pandas as pd

# -------------------
# Load Data
# -------------------

data = pd.read_csv(r"C:\Users\Acer\Desktop\BTC\BTCUSDT_1h_2025_clean.csv")

df = data.copy()

# اطمینان از عددی بودن close
df["close"] = pd.to_numeric(df["close"], errors="coerce")

# مرتب بودن دیتا از قدیم به جدید (خیلی مهم)
df = df.sort_values("open_time").reset_index(drop=True)

# -------------------
# 1️⃣ Log return لحظه‌ای (1h)
# -------------------

df["log_return_1h"] = np.log(df["close"] / df["close"].shift(1))

# -------------------
# 2️⃣ Horizons
# -------------------

horizons = {
    "6h": 6,
    "12h": 12,
    "24h": 24,
    "7d": 168
}

for name, step in horizons.items():

    future_price = df["close"].shift(-step)

    # ✅ Simple Return
    df[f"return_{name}"] = (future_price - df["close"]) / df["close"]

    # ✅ Log Return (نسخه استاندارد پیشنهادی)
    df[f"logreturn_{name}"] = np.log(future_price / df["close"])

    # ✅ Direction (classification target)
    df[f"direction_{name}"] = (future_price > df["close"]).astype(int)

    # ✅ 3% move classification
    df[f"up3pct_{name}"] = (future_price >= df["close"] * 1.03).astype(int)

# -------------------
# حذف ردیف‌های انتهایی که future ندارند
# -------------------

df = df.dropna().reset_index(drop=True)

# -------------------
# Save
# -------------------

df.to_csv(r"C:\Users\Acer\Desktop\BTC\BTCUSDT_targets_ready.csv", index=False)

print(" Targets created successfully.")
print(df.head())
