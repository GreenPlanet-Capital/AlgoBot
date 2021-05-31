import math
from Production.StockDataExtraction.BasketStockData_Backtest import BasketStockData_Backtest
from Production.Backtesters.V1.Portfolio import Portfolio
from Production.Backtesters.V1.Position import Position
from Engines.OptimisedModel import OptimisedModel
import warnings

class Backtester:

    def __init__(self, *, StockDataDict, list_stock, initial_capital, base_lookback, training_period, start_date, end_date, update_data = True, percentRisk_PerTrade = 0.1):
        self.StockDataDict = StockDataDict
        self.list_stock = list_stock
        self.initial_capital = initial_capital
        self.base_lookback = base_lookback
        self.training_period = training_period
        self.start_date = start_date
        self.end_date = end_date
        self.update_data = update_data
        self.percentRisk_PerTrade = percentRisk_PerTrade
        self.max_position_size = self.initial_capital * self.percentRisk_PerTrade
        self.n_today = self.training_period
    
    def validate_StockDataDict(self):
        for ticker,df in self.StockDataDict.items():
            if 0 in list(df["HIGH"]):
                del self.StockDataDict[ticker]
                warnings.warn("Deleting Ticker: " + str(ticker) + " due to insufficient data")

    def dictionary_grafting(self):
        out_dict = {}
        for i in self.list_stock:
            out_dict[i] = self.StockDataDict[i].iloc[self.n_today-self.training_period: self.n_today]
        return out_dict

    def get_str_date(self,n):
        return self.StockDataDict[self.list_stock[0]].loc[n,'DATE']
        
    def newPositions(self, *, dict_of_dataframes, wallet, today):
        number_of_new_positions = math.floor((wallet/self.max_position_size))
        obj = OptimisedModel(dict_of_dataframes = dict_of_dataframes, base_lookback = self.base_lookback, multiplier1 = 1.5, multiplier2 = 2, lin_reg_filter_multiplier = 0.8, number_of_readings = self.number_of_readings, filter_percentile = 80, filter_activation_flag = True, long_only_flag = False)
        position_list = obj.run()
        
        for i in range(number_of_new_positions):
            ticker,strength_val = position_list[i]
            entry_price = dict_of_dataframes[ticker].loc[-1,"TYPICAL PRICE"]
            number_of_shares = int(math.floor(self.max_position_size/entry_price))
            today = self.get_str_date(self.n_today)
            entry_date = today

            position_type = ""
            if(strength_val > 0):
                position_type = "LONG"
            elif(strength_val < 0):
                position_type = "SHORT"

            #Generating the Unique ID
            unique_ID = str(ticker) + str(today)
            positionObj = Position(unique_id = unique_ID, ticker = ticker, entry_price = entry_price, number_of_shares = number_of_shares, entry_date = entry_date, position_type = position_type)
            Portfolio.enter(unique_id = unique_ID, position = positionObj)
      
    def run(self):
        with open('backtest_results.txt', 'w') as f:
            f.write('')
        
        self.StockDataDict = BasketStockData_Backtest().generate_dict(start = self.start, end = self.end, list_of_tickers = self.list_stock, update_data = self.update_data)
        self.validate_StockDataDict()
        portfolio = Portfolio(initial_capital = 100000)
        dict_of_dataframes = self.dictionary_grafting()
        today = self.get_str_date(self.n_today)
        self.newPositions(dict_of_dataframes=dict_of_dataframes, wallet = portfolio.wallet, today=today)
        self.n_today += 1
        
        while self.get_str_date(self.n_today) != self.get_str_date(-1):
            dict_of_dataframes 
            today = self.get_str_date(self.n_today)
            portfolio.update_portfolio(NewStockDataDict=dict_of_dataframes, today=today)
            self.n_today += 1
            self.newPositions(dict_of_dataframes=dict_of_dataframes, wallet = portfolio.wallet, today=today)
