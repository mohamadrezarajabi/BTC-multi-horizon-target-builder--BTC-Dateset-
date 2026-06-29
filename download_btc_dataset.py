import requests
import zipfile
import pandas as pd
import os
from pathlib import Path

# -----------------------------------------------
# تابع کمکی - قابل import از فایل‌های دیگه
# -----------------------------------------------
def get_output_file(symbol, interval):
    return f"{symbol}_{interval}_raw.csv"


VALID_INTERVALS = {
    "1m", "3m", "5m", "15m", "30m",
    "1h", "2h", "4h", "6h", "8h", "12h",
    "1d", "3d", "1w", "1mo",
}


# -----------------------------------------------
# دانلود فایل‌ها
# -----------------------------------------------
def download_all(symbol, interval, start_year, end_year, temp_dir):
    base_url = f"https://data.binance.vision/data/spot/monthly/klines/{symbol}/{interval}/"
    downloaded = []

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            month_str = str(month).zfill(2)
            filename = f"{symbol}-{interval}-{year}-{month_str}.zip"
            url = base_url + filename
            save_path = temp_dir / filename

            if save_path.exists():
                print(f"[SKIP] {filename} already exists")
                downloaded.append(save_path)
                continue

            try:
                response = requests.get(url, timeout=30)
            except requests.RequestException:
                print(f"[ERROR] Could not connect: {filename}")
                continue
            if response.status_code == 200:
                with open(save_path, "wb") as f:
                    f.write(response.content)
                print(f"[OK] Downloaded {filename}")
                downloaded.append(save_path)
            else:
                print(f"[SKIP] {filename} not available yet")

    return downloaded


# -----------------------------------------------
# خواندن و ترکیب همه فایل‌ها
# -----------------------------------------------
def build_dataframe(zip_files):
    dfs = []

    for zip_path in sorted(zip_files):
        try:
            with zipfile.ZipFile(zip_path) as z:
                csv_name = z.namelist()[0]
                df = pd.read_csv(z.open(csv_name), header=None)
                dfs.append(df)
                print(f"[READ] {zip_path.name} -> {len(df)} rows")
        except Exception as e:
            print(f"[ERROR] {zip_path}: {e}")

    if not dfs:
        raise ValueError("No data found!")

    data = pd.concat(dfs, ignore_index=True)

    data.columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ]

    data["open_time"] = pd.to_numeric(data["open_time"], errors="coerce")
    data["close_time"] = pd.to_numeric(data["close_time"], errors="coerce")

    sample = data["open_time"].iloc[0]
    if sample > 1e15:
        print("[INFO] Detected microsecond timestamps, converting to ms...")
        data["open_time"] = data["open_time"] // 1000
        data["close_time"] = data["close_time"] // 1000

    data["open_time"] = pd.to_datetime(data["open_time"], unit="ms")
    data["close_time"] = pd.to_datetime(data["close_time"], unit="ms")

    numeric_cols = ["open", "high", "low", "close", "volume",
                    "quote_volume", "trades", "taker_buy_base", "taker_buy_quote"]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.sort_values("open_time").reset_index(drop=True)
    data = data.drop(columns=["ignore"])
    data = data.drop_duplicates(subset=["open_time"]).reset_index(drop=True)

    return data


def cleanup_zips(temp_dir):
    for file in temp_dir.glob("*.zip"):
        file.unlink()

    try:
        temp_dir.rmdir()
    except OSError:
        pass


# -----------------------------------------------
# اجرا - فقط وقتی مستقیم run میشه
# -----------------------------------------------
if __name__ == "__main__":
    # دریافت ورودی
    while True:
        SYMBOL = input("Symbol (BTCUSDT or BTC): ").strip().upper()
        if not SYMBOL:
            print("❌ Symbol cannot be empty.")
            continue
        if not SYMBOL.endswith("USDT"):
            SYMBOL += "USDT"
        break

    while True:
        INTERVAL = input("TimeFrame: ").strip().lower()
        if INTERVAL in VALID_INTERVALS:
            break
        print("❌ Invalid timeframe.")

    START_YEAR = 2025
    END_YEAR = 2026
    OUTPUT_FILE = get_output_file(SYMBOL, INTERVAL)

    BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
    TEMP_DIR = BASE_DIR / "temp_zips"
    TEMP_DIR.mkdir(exist_ok=True)

    print("=== Binance Dataset Downloader ===")
    print(f"Symbol: {SYMBOL} | Interval: {INTERVAL}")
    print(f"Period: {START_YEAR} - {END_YEAR}")
    print(f"Saving zips to: {TEMP_DIR}")
    print()

    print("Step 1: Downloading files...")
    zip_files = download_all(SYMBOL, INTERVAL, START_YEAR, END_YEAR, TEMP_DIR)
    print(f"Total zip files: {len(zip_files)}")

    print("\nStep 2: Building DataFrame...")
    df = build_dataframe(zip_files)

    output_path = BASE_DIR / OUTPUT_FILE
    print(f"\nStep 3: Saving to {output_path}...")
    df.to_csv(output_path, index=False)

    cleanup_zips(TEMP_DIR)

    print("\n=== Done ===")
    print(f"Total candles : {len(df):,}")
    print(f"From          : {df['open_time'].iloc[0]}")
    print(f"To            : {df['open_time'].iloc[-1]}")
    print(f"File          : {output_path}")
    print()
    print(df[["open_time", "open", "high", "low", "close", "volume"]].head(3))