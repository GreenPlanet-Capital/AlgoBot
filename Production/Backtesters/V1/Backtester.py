import math
from StockDataExtraction.BasketStockData_Backtest import BasketStockData_Backtest
from Backtesters.V1.Portfolio import Portfolio
from Backtesters.V1.Position import Position
from Engines.OptimisedModel import OptimisedModel
import numpy as np
import warnings
import copy
import math

class Backtester:

    def __init__(self, *, list_stock, initial_capital, base_lookback, multiplier1, multiplier2, lin_reg_filter_multiplier, stop_loss_percent, filter_percentile, filter_activation_flag, long_only_flag, training_period, current_account_size_csv, start_date, end_date, update_data=True, percentRisk_PerTrade=0.1):
        self.StockDataDict = {}
        self.list_stock = list_stock
        self.initial_capital = initial_capital
        self.base_lookback = base_lookback
        self.multiplier1 = multiplier1
        self.multiplier2 = multiplier2
        self.lin_reg_filter_multiplier = lin_reg_filter_multiplier
        self.stop_loss_percent = stop_loss_percent
        self.filter_percentile = filter_percentile
        self.filter_activation_flag = filter_activation_flag
        self.long_only_flag = long_only_flag
        self.training_period = training_period
        self.current_account_size_csv = current_account_size_csv
        self.start_date = start_date
        self.end_date = end_date
        self.update_data = update_data
        self.percentRisk_PerTrade = percentRisk_PerTrade
        self.max_position_size = self.initial_capital * self.percentRisk_PerTrade
        self.n_today = self.training_period
    
    def validate_StockDataDict(self):
        for ticker, df in copy.deepcopy(self.StockDataDict).items():
            if len([x for x in list(df["HIGH"]) if math.isnan(x)]) > 0:
                del self.StockDataDict[ticker]
                self.list_stock.remove(ticker)
                print("Deleting Ticker: " + str(ticker) + " due to insufficient data")

    def dictionary_grafting(self):
        out_dict = {}
        for ticker, df in self.StockDataDict.items():
            out_dict[ticker] = df.iloc[(self.n_today - self.training_period): self.n_today]
        return out_dict


    def get_str_date(self,n):
        if(n==-1):
            n = len(self.StockDataDict[self.list_stock[0]])
        return self.StockDataDict[self.list_stock[0]].iloc[n-1]['DATE']
        
    def newPositions(self, *, dict_of_dataframes, wallet, today):
        self.max_position_size = self.portfolio.get_current_account_size() * self.percentRisk_PerTrade
        number_of_new_positions = math.floor((wallet/self.max_position_size))
        if(number_of_new_positions==0):
            return 0
        obj = OptimisedModel(dict_of_dataframes=dict_of_dataframes, base_lookback=self.base_lookback, multiplier1=self.multiplier1, multiplier2=self.multiplier2, lin_reg_filter_multiplier=self.lin_reg_filter_multiplier,
                             number_of_readings=number_of_new_positions, filter_percentile=self.filter_percentile, filter_activation_flag=self.filter_activation_flag, long_only_flag=self.long_only_flag)
        position_list = obj.run()
        for new_position in position_list:
            ticker, strength_val = new_position
            entry_price = dict_of_dataframes[ticker].iloc[len(dict_of_dataframes[ticker])-1]["TYPICAL PRICE"]
            number_of_shares = int(math.floor(self.max_position_size/entry_price))
            today = self.get_str_date(self.n_today)
            entry_date = today

            position_type = ""
            if(strength_val > 0):
                position_type = "LONG"
            elif(strength_val < 0):
                position_type = "SHORT"

            #Generating the Unique ID
            unique_ID = ticker + today
            positionObj = Position(unique_id = unique_ID, ticker = ticker, entry_price = entry_price, number_of_shares = number_of_shares, entry_date = entry_date, position_type = position_type)
            self.portfolio.enter(unique_id = unique_ID, position = positionObj)
      
    def run(self):
        with open('backtest_results.txt', 'w') as f:
            f.write('')

        with open(f'{self.current_account_size_csv}.csv', 'w') as f:
            f.write('Date,Current Account Size\n')
        
        self.StockDataDict = BasketStockData_Backtest().generate_dict(start = self.start_date, end = self.end_date, list_of_tickers=self.list_stock, update_data=self.update_data)
        self.validate_StockDataDict()
        self.portfolio = Portfolio(initial_capital = self.initial_capital, base_lookback=self.base_lookback)

        while self.get_str_date(self.n_today) != self.get_str_date(-1):
            print(f'N_TODAY: {self.n_today}')
            dict_of_dataframes = self.dictionary_grafting()
            today = self.get_str_date(self.n_today)
            self.newPositions(dict_of_dataframes=dict_of_dataframes, wallet=self.portfolio.wallet, today=today)
            self.portfolio.update_portfolio(
                NewStockDataDict=dict_of_dataframes, stop_loss_percent=self.stop_loss_percent, current_date=today, current_account_size_csv=self.current_account_size_csv)
            self.n_today += 1
        print(f'N_TODAY: {self.n_today}')
        dict_of_dataframes = self.dictionary_grafting()
        today = self.get_str_date(self.n_today)
        self.newPositions(dict_of_dataframes=dict_of_dataframes,
                          wallet=self.portfolio.wallet, today=today)
        self.portfolio.update_portfolio(
            NewStockDataDict=dict_of_dataframes, stop_loss_percent=self.stop_loss_percent, current_date=today, current_account_size_csv=self.current_account_size_csv)
        self.n_today += 1
