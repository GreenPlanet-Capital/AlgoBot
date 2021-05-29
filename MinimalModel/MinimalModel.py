import pandas as import pd
import numpy as np
import math 

'''
inputs: base_lookback, multiplier1, multiplier2, filter-percentile
output: ordered list
'''
class OptimisedModel: 
    def __init__(self, input_dict_dataframe, base_lookback, multiplier1, multiplier2, filter_percentile, filter_activation_flag = True):
        self.base_lookback = base_lookback
        self.multiplier1 = multiplier1
        self.multiplier2 = multiplier2
        self.filter_percentile = filter_percentile
        self.filter_activation_flag = filter_activation_flag

    def array_slicer(self)

        return main_lookback_array, multiplier1_lookback_array, multiplier2_lookback_array
    
    def lin_reg(self, price_array, lookback):

        return lin_reg_value
    
    def std(self, price_array, lookback):

        return std_val

    def wma(self, price_array, lookback):

        return wma_val

    def sma(self, price_array, lookback):

        return sma_val

    def mcg(self, price_array, lookback):

        return mcg_val

    def fish_transform(self, price_array, lookback):

        return fish_transform_val
