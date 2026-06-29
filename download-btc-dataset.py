import requests

base_url = "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1h/"

years = range(2025, 2026)
months = range(1,13)

for y in years:
    for m in months:
        month = str(m).zfill(2)
        file = f"BTCUSDT-1h-{y}-{month}.zip"
        url = base_url + file
        
        r = requests.get(url)
        if r.status_code == 200:
            with open(file,"wb") as f:
                f.write(r.content)
            print("downloaded",file)
