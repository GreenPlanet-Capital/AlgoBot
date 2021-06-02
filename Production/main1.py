from OptimisedIndicatorClasses.BollingerSMA import BollingerSMA
from OptimisedIndicatorClasses.BollingerWMA import BollingerWMA
from OptimisedIndicatorClasses.BollingerMcG import BollingerMcG
from OptimisedIndicatorClasses.EnvelopeMcG import EnvelopeMcG
from OptimisedIndicatorClasses.EnvelopeSMA import EnvelopeSMA
from OptimisedIndicatorClasses.EnvelopeWMA import EnvelopeWMA
from OptimisedIndicatorClasses.McG_McG_Osc import McG_McG_Osc
from OptimisedIndicatorClasses.SMA_SMA_Osc import SMA_SMA_Osc
from OptimisedIndicatorClasses.WMA_SMA_Osc import WMA_SMA_Osc
from OptimisedIndicatorClasses.WMA_WMA_Osc import WMA_WMA_Osc
from OptimisedIndicatorClasses.WMA_McG_Osc import WMA_McG_Osc
from OptimisedIndicatorClasses.SMA_McG_Osc import SMA_McG_Osc
from OptimisedIndicatorClasses.DM_DM_Osc import DM_DM_Osc
from OptimisedIndicatorClasses.Lin_Reg import Lin_Reg
from StockDataExtraction.StockData import BasketStockData
from StockDataExtraction.BasketStockData_Backtest import BasketStockData_Backtest
from Engines.OptimisedModel import OptimisedModel as OptimisedModel
import yfinance as yf
import numpy as np

list_stock = ['AAPL', 'LDOS', 'IPG', 'AAP', 'FLIR', 'AKAM']
stock_data = BasketStockData(True, 30)
dict_of_dataframes_from_basket_stock_data = stock_data.generate_dict(list_stock, update_data=False)
dict_of_dataframes_from_backtester_basket_stock_data = BasketStockData_Backtest().generate_dict(start='2020-01-07', end='2020-02-22', list_of_tickers=list_stock, update_data=False)


def dictionary_grafting(n_today):
    out_dict = {}
    for ticker, df in dict_of_dataframes_from_backtester_basket_stock_data.items():
        out_dict[ticker] = df.iloc[(n_today - 30): n_today].copy(deep=True)
    return out_dict

n_today = 30

with open('dict_of_dataframes_from_basket_stock_data.txt', 'w') as f:
    f.write('')

with open('dict_of_dataframes_from_backtester_basket_stock_data.txt', 'w') as f:
    f.write('')

for i in range(4):
    grafted_dict_of_dataframes = dictionary_grafting(n_today)
    with open('dict_of_dataframes_from_basket_stock_data.txt', 'a') as f:
        f.write(f'N_TODAY: {n_today}\n\n')
    with open('dict_of_dataframes_from_backtester_basket_stock_data.txt', 'a') as f:
        f.write(f'N_TODAY: {n_today}\n\n')
    is_same = False
    for ticker in list_stock:
        df1 = dict_of_dataframes_from_basket_stock_data[ticker]
        df2 = grafted_dict_of_dataframes[ticker]
        df2.drop('TYPICAL PRICE',inplace=True,axis=1)
        df2.drop('DATE', inplace=True, axis=1)
        with open('dict_of_dataframes_from_basket_stock_data.txt', 'a') as f:
            f.write(f'{ticker}\n')
            f.write(f'{str(df1)}\n\n')
        with open('dict_of_dataframes_from_backtester_basket_stock_data.txt', 'a') as f:
            f.write(f'{ticker}\n')
            f.write(f'{str(df2)}\n\n')
        if df1.equals(df2):
            is_same = True
        else:
            is_same = False
    
    df1_obj = OptimisedModel(dict_of_dataframes=dict_of_dataframes_from_basket_stock_data, base_lookback=10, multiplier1=1.5, multiplier2=2, lin_reg_filter_multiplier=0.8,
                             number_of_readings=30, filter_percentile=70, filter_activation_flag=True, long_only_flag=True)
    df2_obj = OptimisedModel(dict_of_dataframes=grafted_dict_of_dataframes, base_lookback=10, multiplier1=1.5, multiplier2=2, lin_reg_filter_multiplier=0.8, number_of_readings=30, filter_percentile=70, filter_activation_flag=True, long_only_flag=True)
    print(f'N_TODAY: {n_today}')
    print(df1_obj.run())
    print(df2_obj.run())
    print()

    if is_same:
        print(f'is_same triggerd for n_today={n_today}')
    
    n_today += 1

