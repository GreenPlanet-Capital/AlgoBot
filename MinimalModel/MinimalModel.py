import pandas as import pd
import numpy as np
import math 

'''
inputs: base_lookback, multiplier1, multiplier2, filter-percentile
output: ordered list
'''
class OptimisedModel: 
    def __init__(self, dict_of_dataframes, base_lookback, multiplier1, multiplier2, lin_reg_filter_multiplier, number_of_readings, filter_percentile = 75, filter_activation_flag = True, long_only_flag = False):
        self.base_lookback = base_lookback
        self.lin_reg_filter_multiplier = lin_reg_filter_multiplier
        self.multiplier1 = multiplier1
        self.multiplier2 = multiplier2
        self.number_of_readings = number_of_readings
        self.filter_percentile = filter_percentile
        self.filter_activation_flag = filter_activation_flag

    def array_slicer(self, df_input)
        df_input['Typical Price'] = ((df_input['HIGH'] + df_input['LOW'] + df_input['CLOSE']) / 3).round(2)
        price_array = np.array(df_input['Typical Price'])

        linreg_lookback = math.ceil(self.base_lookback*self.lin_reg_filter_multiplier)
        lookback1 = math.ceil(self.base_lookback*self.multiplier1)
        lookback2 = math.ceil(self.base_lookback*self.multiplier2) 
        ft_lookback = self.base_lookback*2

        lin_reg_array = price_array[-linreg_lookback:] 
        main_lookback_array = price_array[-self.base_lookback:]
        multiplier1_lookback_array = price_array[-lookback1:]
        multiplier2_lookback_array = price_array[-lookback2:]
        fisher_transform = price_array[-ft_lookback:]
        present_price = price_array[-1]

        return present_price, lin_reg_array,main_lookback_array, multiplier1_lookback_array, multiplier2_lookback_array, fisher_transform_array
    
    def generate_listOfTickers(self):
        in_dict = self.dict_of_dataframes
        ticker_list = []
        for ticker in in_dict:
            ticker_list.append(ticker)
        return ticker_list

    def lin_reg(self, price_array):
        n = len(price_array)
        sum_y = 0
        sum_xy = 0
        sum_x = (n+1)*n/2
        sum_x2 = n*(n+1)*(2*n+1)/6
        for i,j in enumerate(price_array):
            sum_y += j
            sum_xy += (i+1)*j 
        lin_reg = (n*sum_xy - (sum_x*sum_y))/((n*sum_x2) - (sum_x*sum_x))
        return lin_reg
    
    def std(self, price_array):
        std_val = np.std(price_array)
        return std_val

    def wma(self, price_array):
        sum_val = 0 
        div = len(price_array)
        for j,i in enumerate(price_array):
            sum_val += (j+1)*i
        wma_val = (sum_val*2)/(div*(div+1))
        return wma_val

    def sma(self, price_array):
        sma_val = np.sum(price_array)/len(price_array)
        return sma_val

    def mcg(self, price_array, lookback):
        len_pa = len(price_array)
        base_val_array = price_array[:len_pa - 1]
        base_val = np.sum(base_val_array)/len(base_val_array)
        numer = (price_array[-1] - base_val)
        denom = len_pa*((price_array[-1]/base_val)**4
        frac = numer/denom
        mcg_val = frac + base_val
        return mcg_val
    
    def envelope_score(self, df_input):
        present_price, lin_reg_array,main_lookback_array, multiplier1_lookback_array, multiplier2_lookback_array, fisher_transform_array = self.array_slicer(df_input)
        
        bol_std_val1 = 1
        bol_std_val2 = 1.3
        bol_std_val3 = 1.6
        env_std_val1 = 0.017
        env_std_val2 = 0.02
        env_std_val3 = 0.023

        #Base_Lookback Envelopes
        bl_bol1_threshold = self.sma()

        #Multiplier1_Lookback Envelopes

        #Multiplier2_Lookback Envelopes




    

        

