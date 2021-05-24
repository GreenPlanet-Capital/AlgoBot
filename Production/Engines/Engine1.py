from OptimisedIndicatorClasses.BollingerSMA import BollingerSMA
from OptimisedIndicatorClasses.BollingerWMA import BollingerWMA
from OptimisedIndicatorClasses.BollingerMcG import BollingerMcG
from OptimisedIndicatorClasses.EnvelopeMcG import EnvelopeMcG
from OptimisedIndicatorClasses.EnvelopeSMA import EnvelopeSMA
from OptimisedIndicatorClasses.EnvelopeWMA import EnvelopeWMA
from OptimisedIndicatorClasses.SMA_SMA_Osc import SMA_SMA_Osc
from OptimisedIndicatorClasses.WMA_SMA_Osc import WMA_SMA_Osc
from OptimisedIndicatorClasses.WMA_WMA_Osc import WMA_WMA_Osc
from OptimisedIndicatorClasses.WMA_McG_Osc import WMA_McG_Osc
from OptimisedIndicatorClasses.SMA_McG_Osc import SMA_McG_Osc
from OptimisedIndicatorClasses.DM_DM_Osc import DM_DM_Osc
from OptimisedIndicatorClasses.Lin_Reg import Lin_Reg
import yfinance as yf
import numpy as np
import pandas as pd
import multiprocessing as mp


class Engine1:
    def __init__(self, dict_of_dataframes, base_lookback, number_of_readings):
        self.dict_of_dataframes = dict_of_dataframes
        self.base_lookback = base_lookback
        self.number_of_readings = number_of_readings
    
    def weight_adjust(self, input_weight):
        if (input_weight <= 0.01):
            return 0.01
        else:
            return input_weight

    def generate_longShortStrength(self, df_input):
        df_input['Typical Price'] = ((df_input['HIGH'] + df_input['LOW'] + df_input['CLOSE']) / 3).round(2)
        price_list = np.array(df_input['Typical Price'])
        lookback1 = self.base_lookback

        bol_mcg_obj = BollingerMcG(price_array = price_list , lookback = lookback1, multiplier = 1.2)
        bol_mcg_reading, bol_mcg_weight = bol_mcg_obj.run()
        bol_mcg_weight = self.weight_adjust(bol_mcg_weight)

        bol_sma_obj = BollingerSMA(price_array = price_list , lookback = lookback1, multiplier = 1.2)
        bol_sma_reading, bol_sma_weight = bol_sma_obj.run()
        bol_sma_weight = self.weight_adjust(bol_sma_weight)

        bol_wma_obj = BollingerWMA(price_array = price_list , lookback = lookback1, multiplier = 1.2)
        bol_wma_reading, bol_wma_weight = bol_wma_obj.run()
        bol_wma_weight = self.weight_adjust(bol_wma_weight)

        env_mcg_obj = EnvelopeMcG(price_array = price_list , lookback = lookback1, multiplier = 1.2)
        env_mcg_reading, env_mcg_weight = env_mcg_obj.run()
        env_mcg_weight = self.weight_adjust(env_mcg_weight)

        env_sma_obj = EnvelopeSMA(price_array = price_list , lookback = lookback1, multiplier = 1.2)
        env_sma_reading, env_sma_weight = env_sma_obj.run()
        env_sma_weight = self.weight_adjust(env_sma_weight)

        env_wma_obj = EnvelopeWMA(price_array = price_list , lookback = lookback1, multiplier = 1.2)
        env_wma_reading, env_wma_weight = env_wma_obj.run()
        env_wma_weight = self.weight_adjust(env_wma_weight)

        total = (
                bol_mcg_weight + 
                bol_sma_weight +
                bol_wma_weight +
                env_sma_weight +
                env_mcg_weight +
                env_wma_weight
                )
        
        reading = (
                bol_mcg_reading * bol_mcg_weight +
                bol_sma_reading * bol_sma_weight +
                bol_wma_reading * bol_wma_weight + 
                env_mcg_reading * bol_mcg_weight +
                env_sma_reading * bol_sma_weight +
                env_wma_reading * bol_wma_weight  
                )
        reading = reading/total
        return reading

    def generate_listOfTickers(self):
        in_dict = self.dict_of_dataframes
        ticker_list = []
        for ticker in in_dict:
            ticker_list.append(ticker)
        
        return ticker_list  

    def generate_parallel(self, ticker):
        data_var = self.dict_of_dataframes[ticker]
        output = self.generate_longShortStrength(data_var)

        return (ticker,output)

    def generate(self): 
        num = self.number_of_readings
        in_dict = self.dict_of_dataframes
        generated_dict = {}

        if (num >= len(in_dict)):
            raise IndexError("The number of readings is too high, reduce to less than half the length of the input")

        pool = mp.Pool(mp.cpu_count())
        try:
            generated_dict = dict(pool.map(self.generate_parallel, [ticker for ticker in self.generate_listOfTickers()]))
        except Exception as e:
            pool.close()
            raise e

        copy_dict_list = generated_dict.items()

        copy_dict = {}
        for ticker, data in copy_dict_list:
            copy_dict[ticker] = abs(data)

        sorted_dictionary = sorted(copy_dict.items(), key = lambda kv: kv[1])
        sorted_dict = dict(sorted_dictionary)

        ticker_list = [i for i in sorted_dict] 

        long_book = {}
        short_book = {}
        long_ctr = 0
        short_ctr = 0

        for i in reversed(ticker_list):
            if (long_ctr >= num):
                break
            if (generated_dict[i] > 0):
                long_book[i] = generated_dict[i]
                long_ctr += 1

        for i in reversed(ticker_list):
            if (short_ctr >= num):
                break
            if (generated_dict[i] < 0):
                short_book[i] = generated_dict[i]
                short_ctr += 1 

        return long_book, short_book