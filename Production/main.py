from StockDataExtraction.StockData import SingleStockData
from IndicatorClasses.TradingRange import TradingRange
import yfinance as yf
from StockDataExtraction.BasketStockData_Backtest import BasketStockData_Backtest
from Engines.Engine1 import Engine1
from Engines.FilteredTrend import Engine2
from Engines.OptimisedModel import OptimisedModel
import time
import sys
from SecuritySelection.Baskets import Markets


def main():

    basket = Markets.snp
    begin = time.time()
    stock_data = BasketStockData_Backtest()
    if len(sys.argv)>1:
        if sys.argv[1]=='--update':
            update_data = True
    else:
        update_data = False
    x = stock_data.generate_dict(start='2020-01-01', end='2021-06-01', list_of_tickers=basket, update_data=update_data)
    end = time.time()
    print(f'Time taken to extract data: {end - begin}')

    begin1 = time.time()
    # dict_of_dataframes = x
    # base_lookback = 7
    # number_of_readings = 20

    # eng_obj = Engine2(dict_of_dataframes = dict_of_dataframes, base_lookback = base_lookback, number_of_readings = number_of_readings)
    # longs, shorts = eng_obj.generate(absolute_list = False)
    # print ("Metrics " + '\n' + "Base Lookback: " + str(base_lookback) + '\n' + "Number of Readings: " + str(number_of_readings))
    # print("Longs: ")
    # print(longs)
    # print()
    # print("Shorts: ")
    # print(shorts)
    # print()
    obj = OptimisedModel(dict_of_dataframes = x, base_lookback = 17, multiplier1 = 1.5, multiplier2 = 2, lin_reg_filter_multiplier = 0.5, number_of_readings = 30, filter_percentile = 70, filter_activation_flag = True, long_only_flag = False)
    print(obj.run())

    end1 = time.time()

    print(f"Time taken to compute data: {end1 - begin1}")

if __name__ == '__main__':
    main()
# ['FB'])
# print(dict1)
