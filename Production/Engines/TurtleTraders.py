import pandas as pd
import numpy as np
import math 
import multiprocessing as mp

class TurtleTraders: 
    
    def __init__(self, *, dict_of_dataframes, base_lookback, number_of_readings, long_only_flag = False):
        self.base_lookback = base_lookback
        self.dict_of_dataframes = dict_of_dataframes
        self.number_of_readings = number_of_readings
        self.long_only_flag = long_only_flag
        self.ticker_data_list = []
        self.unordered_dict = {}

    def array_slicer(self, df_input):
        df_input['TYPICAL PRICE'] = ((df_input['HIGH'] + df_input['LOW'] + df_input['CLOSE']) / 3).round(2)
        price_array = np.array(df_input['TYPICAL PRICE'])

        main_lookback_array = price_array[-self.base_lookback:-1]
        present_price = price_array[-1]
        return present_price, main_lookback_array
    
    def generate_listOfTickers(self):
        in_dict = self.dict_of_dataframes
        ticker_list = []
        for ticker in in_dict:
            ticker_list.append(ticker)
        return ticker_list


    def envelope_score(self, df_input):
        present_price, main_lookback_array = self.array_slicer(df_input)

        max_val = np.amax(main_lookback_array)
        min_val = np.amin(main_lookback_array)
        score = 0
        if(present_price <= min_val):
            result = np.where(main_lookback_array ==  min_val)
            index = result[0][0]
            score = index - self.base_lookback
        elif(present_price >= max_val):
            result = np.where(main_lookback_array ==  max_val)
            index = result[0][0]
            score = self.base_lookback - index
        else:
            score = 0

        return score        

    def data_generator(self):
        stock_list = self.generate_listOfTickers()
        for ticker in stock_list:
            score = self.envelope_score(self.dict_of_dataframes[ticker])
            self.ticker_data_list.append((ticker, score))

    def ordering(self):
        if (self.long_only_flag):
            for ticker,score in self.ticker_data_list:
                if (score <= 0):
                    self.ticker_data_list.remove((ticker,score))
        abs_list = []
        for ticker,score in self.ticker_data_list:
            if(score != 0):
                abs_list.append(abs(score))

        abs_list.sort(reverse = True)
        out_list = []
        for abs_val in abs_list:
            for ticker,score in self.ticker_data_list:
                if(abs(score) == abs_val):
                    out_list.append((ticker,score))
                    self.ticker_data_list.remove((ticker,score))
        
        out_list = out_list[-self.number_of_readings:]
        return out_list

    def run(self):
        self.data_generator()
        out = self.ordering()
        return out

            

    

        

