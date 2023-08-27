import pandas as pd
import yfinance as yf
import datetime
from tqdm import tqdm
import logging
import json
import sys

# Initialize logging
logging.basicConfig(filename='stock_data.log', level=logging.INFO)

def fetch_stock_data(symbols, start, end):
    stock_data = {}
    error_symbols = []
    
    for symbol in tqdm(symbols):
        try:
            stock_data[symbol] = yf.download(symbol, start=start, end=end)['Adj Close']
        except Exception as e:
            error_symbols.append(symbol)
            logging.error(f"Error fetching data for {symbol}: {e}")
    
    return stock_data, error_symbols

def main(file_path):
    # Read stock symbols from given CSV file
    try:
        stock_df = pd.read_csv(file_path)
    except FileNotFoundError:
        logging.error(f"{file_path} not found.")
        return
    
    symbols = stock_df['Symbol']
    
    # Set date range
    end = datetime.date.today()
    start = datetime.datetime(2009, 1, 1)
    
    # Fetch stock data
    stock_data, error_symbols = fetch_stock_data(symbols, start, end)
    
    # Log error symbols
    if error_symbols:
        logging.error(f"Failed to retrieve data for symbols: {error_symbols}")
    
    # Create DataFrame from stock data
    df_stock = pd.DataFrame(stock_data)
    
    # Save to JSON
    df_stock.to_json("sp500stock_improved.json", date_format='iso')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_csv_file>")
    else:
        main(sys.argv[1])
