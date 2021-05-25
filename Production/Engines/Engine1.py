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
from OptimisedIndicatorClasses.McG_McG_Osc import McG_McG_Osc
from OptimisedIndicatorClasses.DM_DM_Osc import DM_DM_Osc
from OptimisedIndicatorClasses.Lin_Reg import Lin_Reg
import yfinance as yf
import numpy as np
import pandas as pd
import multiprocessing as mp
import math


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
        multiplier1 = 2

        bol_mcg_obj = BollingerMcG(price_array = price_list , lookback = lookback1, multiplier = 2)
        bol_mcg_reading, bol_mcg_weight = bol_mcg_obj.run()
        bol_mcg_weight = self.weight_adjust(bol_mcg_weight)

        bol_sma_obj = BollingerSMA(price_array = price_list , lookback = lookback1, multiplier = 1.5)
        bol_sma_reading, bol_sma_weight = bol_sma_obj.run()
        bol_sma_weight = self.weight_adjust(bol_sma_weight)

        bol_wma_obj = BollingerWMA(price_array = price_list , lookback = lookback1, multiplier = 1)
        bol_wma_reading, bol_wma_weight = bol_wma_obj.run()
        bol_wma_weight = self.weight_adjust(bol_wma_weight)

        env_mcg_obj = EnvelopeMcG(price_array = price_list , lookback = lookback1, multiplier = 0.03)
        env_mcg_reading, env_mcg_weight = env_mcg_obj.run()
        env_mcg_weight = self.weight_adjust(env_mcg_weight)

        env_sma_obj = EnvelopeSMA(price_array = price_list , lookback = lookback1, multiplier = 0.025)
        env_sma_reading, env_sma_weight = env_sma_obj.run()
        env_sma_weight = self.weight_adjust(env_sma_weight)

        env_wma_obj = EnvelopeWMA(price_array = price_list , lookback = lookback1, multiplier = 0.02)
        env_wma_reading, env_wma_weight = env_wma_obj.run()
        env_wma_weight = self.weight_adjust(env_wma_weight)

        dm_dm_obj = DM_DM_Osc(price_array = price_list , short_lookback = lookback1, long_lookback = math.ceil(lookback1 * multiplier1))
        dm_dm_reading, dm_dm_weight = dm_dm_obj.run()
        dm_dm_weight = self.weight_adjust(dm_dm_weight)

        mcg_mcg_obj = McG_McG_Osc(price_array = price_list , short_lookback = lookback1, long_lookback = math.ceil(lookback1 * multiplier1))
        mcg_mcg_reading, mcg_mcg_weight = mcg_mcg_obj.run()
        mcg_mcg_weight = self.weight_adjust(mcg_mcg_weight)


        sma_mcg_obj = SMA_McG_Osc(price_array = price_list , short_lookback = lookback1, long_lookback = math.ceil(lookback1 * multiplier1))
        sma_mcg_reading, sma_mcg_weight = sma_mcg_obj.run()
        sma_mcg_weight = self.weight_adjust(sma_mcg_weight)
        
        sma_sma_obj = SMA_SMA_Osc(price_array = price_list , short_lookback = lookback1, long_lookback = math.ceil(lookback1 * multiplier1))
        sma_sma_reading, sma_sma_weight = sma_sma_obj.run()
        sma_sma_weight = self.weight_adjust(sma_sma_weight)
        
        wma_mcg_obj = WMA_McG_Osc(price_array = price_list , short_lookback = lookback1, long_lookback = math.ceil(lookback1 * multiplier1))
        wma_mcg_reading, wma_mcg_weight = wma_mcg_obj.run()
        wma_mcg_weight = self.weight_adjust(wma_mcg_weight)
        
        wma_sma_obj = WMA_SMA_Osc(price_array = price_list , short_lookback = lookback1, long_lookback = math.ceil(lookback1 * multiplier1))
        wma_sma_reading, wma_sma_weight = wma_sma_obj.run()
        wma_sma_weight = self.weight_adjust(wma_sma_weight)
        
        wma_wma_obj = WMA_WMA_Osc(price_array = price_list , short_lookback = lookback1, long_lookback = math.ceil(lookback1 * multiplier1))
        wma_wma_reading, wma_wma_weight = wma_wma_obj.run()
        wma_wma_weight = self.weight_adjust(wma_wma_weight)

        lin_reg_obj = Lin_Reg(price_array = price_list, lookback = lookback1)
        lin_reg_reading, lin_reg_weight = lin_reg_obj.run()
        lin_reg_weight = self.weight_adjust(lin_reg_weight)
        lin_reg_abs = lin_reg_obj.linreg_array[-1]

        total1 = (
                bol_mcg_weight + 
                bol_sma_weight +
                bol_wma_weight +
                env_sma_weight +
                env_mcg_weight +
                env_wma_weight + 
                dm_dm_weight + 
                mcg_mcg_weight + 
                sma_mcg_weight + 
                sma_sma_weight + 
                wma_mcg_weight + 
                wma_sma_weight +
                wma_wma_weight
                )
        
        reading1 = (
                (bol_mcg_reading * bol_mcg_weight +
                bol_sma_reading * bol_sma_weight +
                bol_wma_reading * bol_wma_weight + 
                env_mcg_reading * bol_mcg_weight +
                env_sma_reading * bol_sma_weight +
                env_wma_reading * bol_wma_weight)*1.5 + 
                (dm_dm_reading * dm_dm_weight +
                sma_sma_reading * sma_sma_weight +
                wma_wma_reading * wma_wma_weight + 
                mcg_mcg_reading * mcg_mcg_weight +
                sma_mcg_reading * sma_mcg_weight +
                wma_sma_reading * wma_sma_weight + 
                wma_mcg_reading * wma_mcg_weight) + 
                lin_reg_reading * lin_reg_weight
                )  
        reading = reading1/total1

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
            raise IndexError("The number of readings is too high, reduce to less than the length of the input")

        pool = mp.Pool(mp.cpu_count())
        try:
            generated_dict = dict(pool.map(self.generate_parallel, [ticker for ticker in self.generate_listOfTickers()]))
        except Exception as e:
            pool.close()
            raise e

        short_book = []
        long_book = []

        sorted_list = sorted(generated_dict.items(),key = lambda kv: kv[1])
        for i, ((short_ticker,short_data),(long_ticker,long_data)) in enumerate(zip(sorted_list,reversed(sorted_list))):
            if(i==num):
                break
            if(short_data<0):
                short_book.append((short_ticker, short_data))
            if(long_data>0):
                long_book.append((long_ticker,long_data))

        return long_book, short_book