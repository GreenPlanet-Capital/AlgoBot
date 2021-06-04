"""
# Enter the sheet number between 0 to 9
# Function returns a dataframe with the price from 2016 to present day
# small_data_flag is set to true is the last 100 trading days quotes are required
"""
from copy import Error
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import yfinance as yf
import os
from pathlib import Path
import math

class BasketStockData_Backtest:
    def __init__(self):
        self.out_dict = {}

    def generate_dict(self, start = "0000-00-00", end = "0000-00-00", list_of_tickers = [], update_data=True):
        ctr = 1
        Indicator_CSVs = Path(os.getcwd()) / 'Indicator_CSVs'

        if update_data:        
            basket_data = yf.download(
            tickers = list_of_tickers,
            start = start,
            end = end,
            interval = '1d',
            group_by = 'ticker',
            auto_adjust = True,
            prepost = False,
            threads = True,
            proxy = None
            )
            basket_data = basket_data.T

            for ticker in list_of_tickers:
                basket_data.loc[(ticker,),].T.to_csv((Indicator_CSVs / f'{ticker}.csv'), sep=',', encoding='utf-8')

        empty_dates_indices = []
        df1 = pd.read_csv(Indicator_CSVs / f"{list_of_tickers[0]}.csv")
        empty_dates_indices = self.getIndexes(df1['High'])

        for ticker in list_of_tickers:
            df1 = pd.read_csv(Indicator_CSVs / f"{ticker}.csv")
            df_out = pd.DataFrame()
            df_out['OPEN'] = df1['Open']
            df_out['HIGH'] = df1['High']
            df_out['LOW'] = df1['Low']
            df_out['CLOSE'] = df1['Close']
            df_out['VOLUME'] = df1['Volume']
            df_out['DATE'] = df1['Date']
            df_out['TYPICAL PRICE'] = ((df_out['HIGH'] + df_out['LOW'] + df_out['CLOSE']) / 3).round(2)
            
            df_out = df_out.drop(empty_dates_indices, inplace=False)
            self.out_dict[ticker] = df_out

        return self.out_dict

    def getIndexes(self, npArray):
        listOfPos = list()
        npArray_list = list(npArray)
        for i, price in enumerate(npArray_list):
            if math.isnan(price):
                listOfPos.append(i)
        return listOfPos
    
    def __str__(self):
        return (self.out_dict.to_string())

def main():
    stock_data = BasketStockData_Backtest()
    x = stock_data.generate_dict(start="2020-01-01", end = "2021-01-01", list_of_tickers = ['AAPL', 'MSFT'], update_data=True)
    print(x)
    

if __name__ == '__main__':
    main()





