import multiprocessing
import pandas as pd
import yfinance as yf
import concurrent.futures

def gen_df(ticker):
    yf_obj = yf.Ticker(ticker)
    df1 = yf_obj.history(period = 'max', interval="1d")

    df_out = pd.DataFrame()
    df_out['OPEN'] = df1['Open']
    df_out['HIGH'] = df1['High']
    df_out['LOW'] = df1['Low']
    df_out['CLOSE'] = df1['Close']
    df_out['VOLUME'] = df1['Volume']
    training_period = 100
    return df_out.iloc[-training_period:]

def retrieve(list_tickers):
    p = multiprocessing.Pool(processes = len(list_tickers))
    result = p.map(gen_df, [i for i in list_tickers])
    return result

def extract(list_tickers):
    dataframe_iterator = retrieve(list_tickers)
    df_list = [i for i in dataframe_iterator]
    dict_out = {} 
    for i,j in enumerate(df_list):
        dict_out[list_tickers[i]] = j
    return dict_out

def main(list_tickers):
    return extract(list_tickers)
    
if __name__ == '__main__':
    x = main(['AAPL', 'MSFT', 'JPM', 'GS', 'GM', 'TSLA', 'FB', 'GOOGL', 'JNJ', 'DIS', 'CSCO', 'INTC', 'ABT', 'KO', 'ABBV'])
    print(x)