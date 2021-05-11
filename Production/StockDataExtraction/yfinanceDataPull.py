import multiprocessing
import pandas as pd
import yfinance as yf
import concurrent.futures

class gen:
    main_list = []
    def __init__(self):
        pass
    def gen_df(self, ticker):
        yf_obj = yf.Ticker(ticker)
        df1 = yf_obj.history(period = 'max', interval="1d")

        df_out = pd.DataFrame()
        df_out['OPEN'] = df1['Open']
        df_out['HIGH'] = df1['High']
        df_out['LOW'] = df1['Low']
        df_out['CLOSE'] = df1['Close']
        df_out['VOLUME'] = df1['Volume']

        main_list.append(df_out)

    list_tickers = ['AAPL', 'MSFT', 'JPM', 'GS', 'GM', 'TSLA', 'FB', 'GOOGL', 'JNJ', 'DIS', 'CSCO', 'INTC', 'ABT', 'KO', 'ABBV']

    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(gen_df, list_tickers)
    print(main_list)