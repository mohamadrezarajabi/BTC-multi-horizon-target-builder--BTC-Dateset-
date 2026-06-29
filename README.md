# Bitcoin Multi-Horizon Target Builder

A reproducible data engineering pipeline for building **machine-learning-ready Bitcoin datasets** with **multi-horizon prediction targets**.

This project downloads raw BTCUSDT data from Binance, converts raw ZIP files into a clean dataset, and generates prediction targets used in quantitative trading models.

---

# Project Goal

In quantitative finance, predicting **raw prices** is usually not ideal.

Instead, models predict:

- returns
- log returns
- direction (up/down)
- threshold events (for example +3% moves)

This repository prepares those targets for multiple prediction horizons.

---

# Prediction Horizons

Targets are generated for the following future horizons:

- 6 hours
- 12 hours
- 24 hours
- 7 days

---

# Repository Structure

download-btc-dataset.py  
Download BTCUSDT historical data from Binance.

read-zip-file.py  
Inspect the structure of raw Binance ZIP files.

zip-to-csv.py  
Merge monthly ZIP files and convert them into a clean CSV dataset.

build-target.py  
Generate machine learning targets such as return, log return, direction, and breakout labels.

---

# Installation

Clone the repository:

git clone https://github.com/yourusername/btc-multi-horizon-target-builder.git

cd btc-multi-horizon-target-builder

Install dependencies:

pip install pandas numpy

---

# Pipeline Execution (Step-by-Step)

Run the scripts in the following order.

---

Step 1 — Download Bitcoin Dataset

python download-btc-dataset.py

This script downloads BTCUSDT historical 1-hour data from Binance.

Example output files:

BTCUSDT-1h-2025-01.zip  
BTCUSDT-1h-2025-02.zip  
BTCUSDT-1h-2025-03.zip  

---

Step 2 — Inspect Raw ZIP Files (optional but useful)

python read-zip-file.py

This script helps you inspect the raw structure of Binance data files.

It verifies:

- timestamp format
- column order
- file structure

This step is mainly useful for debugging or understanding the dataset.

---

Step 3 — Convert ZIP Files to a Clean CSV Dataset

python zip-to-csv.py

This script performs the following operations:

- reads all monthly ZIP files
- merges them into a single dataset
- fixes timestamp format
- converts timestamps from microseconds to milliseconds
- creates a clean CSV dataset

Output file:

BTCUSDT_1h_2025_clean.csv

---

Step 4 — Generate Multi-Horizon Targets

python build-target.py

This script generates prediction targets used in machine learning models.

---

Targets Generated

1) Instant Log Return (1 hour)

Column name:

log_return_1h

Formula:

ln(P_t / P_{t-1})

This measures the logarithmic return between consecutive candles.

---

2) Multi-Horizon Targets

For each prediction horizon (6h, 12h, 24h, 7d), the following targets are created:

return_h  
logreturn_h  
direction_h  
up3pct_h  

Example:

return_6h  
logreturn_6h  
direction_6h  
up3pct_6h  

---

Target Definitions

Return

Percentage price change between now and the future time:

(P_future - P_now) / P_now

---

Log Return

Logarithmic return used widely in quantitative finance:

ln(P_future / P_now)

Advantages:

- additive across time
- more statistically stable
- preferred in financial modeling

---

Direction

Binary classification target.

1 → price goes up  
0 → price goes down

---

3% Breakout

Detects strong upward moves.

1 → price ≥ +3%  
0 → otherwise

---

Final Output

BTCUSDT_targets_ready.csv

This dataset includes:

- OHLCV price data
- instant log returns
- multi-horizon regression targets
- multi-horizon classification targets

It is ready for use in:

- XGBoost
- LightGBM
- LSTM models
- Transformer models
- quantitative trading strategies
- financial machine learning pipelines

---

Future Improvements

Possible next steps include:

- adding technical indicators (RSI, EMA, MACD, ATR)
- volatility and rolling statistical features
- feature engineering pipelines
- backtesting frameworks
- probabilistic forecasting models

---

Persian Explanation (توضیح فارسی)

این پروژه یک پایپ‌لاین داده برای آماده‌سازی دیتاست بیت‌کوین جهت استفاده در مدل‌های یادگیری ماشین است.

در این پروژه مراحل زیر انجام می‌شود:

1) دانلود دیتای تاریخی BTCUSDT از بایننس  
2) بررسی ساختار فایل‌های ZIP  
3) تبدیل داده‌های خام به یک فایل CSV تمیز  
4) ساخت تارگت‌های پیش‌بینی برای چند افق زمانی  

---

هدف پروژه

در مدل‌های مالی حرفه‌ای معمولاً قیمت مستقیم پیش‌بینی نمی‌شود.

به جای آن این مقادیر پیش‌بینی می‌شوند:

- بازده (Return)
- لاگ بازده (Log Return)
- جهت حرکت قیمت
- حرکت‌های بزرگ مثل رشد ۳٪

---

افق‌های زمانی پیش‌بینی

در این پروژه تارگت برای بازه‌های زیر ساخته می‌شود:

6 ساعت  
12 ساعت  
24 ساعت  
7 روز  

---

تارگت‌های ساخته شده

برای هر افق زمانی ستون‌های زیر ساخته می‌شوند:

return_h  
logreturn_h  
direction_h  
up3pct_h  

---

خروجی نهایی

BTCUSDT_targets_ready.csv

این فایل شامل:

- داده‌های OHLCV
- لاگ ریترن یک ساعته
- تارگت‌های چند افق زمانی

و آماده استفاده در مدل‌های:

- XGBoost
- LightGBM
- LSTM
- Transformer
- سیستم‌های معاملاتی الگوریتمی

---

Suggested Repository Name

btc-multi-horizon-target-builder

---

Suggested GitHub Topics

bitcoin  
cryptocurrency  
quantitative-finance  
machine-learning  
time-series  
trading  
data-engineering  
binance  
python
`
