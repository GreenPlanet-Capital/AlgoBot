import pandas as pd
import yfinance as yf

data = yf.download(tickers = "ADANIPORTS.NS", period = "1d", interval = "1m", threads = True)
print(data)
