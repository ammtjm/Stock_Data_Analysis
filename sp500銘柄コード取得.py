import pandas as pd
url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"
sp500 = pd.read_csv(url, encoding="SHIFT_JIS")

# 1. 以下のコードを実行して、sp500の先頭5行を表示してください。
print(sp500.head())

# 2. シンボルとセクターの列だけをcsvに保存してください。
# GICS SectorはSectorと名前を変えて保存してください。
sp500[["Symbol", "GICS Sector"]].to_csv("sp500.csv", index=False)
