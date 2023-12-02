import yfinance as yf
import pandas as pd
from datetime import datetime
import argparse

def download_stock_data(tickers):
    # 現在の日付を取得
    current_date = datetime.now().strftime("%Y-%m-%d")

    # 終値を保存するためのディクショナリ
    close_prices = {}

    # 各ティッカーに対して終値を取得
    for ticker in tickers:
        data = yf.download(ticker, start="2011-01-01", end=current_date)
        close_prices[ticker] = data['Close']

    return close_prices

def main():
    parser = argparse.ArgumentParser(description="指定したティッカーの株価終値を取得します。")
    parser.add_argument('tickers', nargs='+', help='ティッカーシンボルのリスト (例: 2633.T 1545.T)')

    args = parser.parse_args()

    # 株価データをダウンロード
    stock_data = download_stock_data(args.tickers)

    # データフレームに変換
    df = pd.DataFrame(stock_data)

    # CSVファイルに保存
    df.to_csv("index_prices.csv")
    print("CSVファイルが生成されました。")

if __name__ == "__main__":
    main()
