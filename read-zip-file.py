import zipfile
import glob

# پیدا کردن اولین فایل زیپ
files = glob.glob("BTCUSDT-1h-2025-*.zip")
if files:
    target_file = sorted(files)[0]
    print(f"Reading raw data from: {target_file}")
    with zipfile.ZipFile(target_file) as z:
        csv_file = z.namelist()[0]
        with z.open(csv_file) as f:
            # خواندن ۵ سطر اول به صورت متنی خام
            for _ in range(5):
                line = f.readline().decode('utf-8')
                print(repr(line))
else:
    print("No zip files found!")
