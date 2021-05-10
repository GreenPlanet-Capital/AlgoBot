'''
Name: LOCAL VOLATILITY

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: LOVALVOL + lookback_period
    Signal Generated DataFrame head: LOVALVOL SIGNAL + lookback_period

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Volatility

Usage Notes: Voltaility within the specified lookback
    
'''
'''
Function Checklist
- a function to take the dataframe input and clean it, in order to keep just the HIGH, LOW, CLOSE and VOLUME
- indicator generation function
- signal generation function
- train test function, that returns the efficacy
- current long/short strength 
'''
'''
Inputs: dataframe_input, lookback_period 
Outputs:  live_signal
'''

import math
import pandas as pd
import json 
import numpy as np
import sys
import oauth2client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.text

class LocalVolatility:

    def __init__(self, dataframe_input, lookback_period, sensitivity = 1, absolute_sensitivity = 50):
        df_generatedIndicators = pd.DataFrame() #Generated from indicator_generator

        df_generatedSignal = pd.DataFrame() #Generated from signal_generation

        df_trainTest = pd.DataFrame() #Generated from train_test
        total_return = 0
        return_potential_ratio = 0

        self.dataframe_input = dataframe_input
        self.lookback_period = lookback_period
        self.sensitivity = sensitivity
        self.absolute_sensitivity = absolute_sensitivity

#######################
#Indicator Generator Function
#######################

    def indicator_generator(self):
        def std(input_list):
            mean = sum(input_list) / len(input_list)
            variance = sum([((x - mean) ** 2) for x in input_list]) / len(input_list)
            res = variance ** 0.5
            
            return res
        
        df = self.dataframe_input
        n = self.lookback_period
        
        df['TYP PRICE'] =  (df['CLOSE'] +  df['LOW'] +  df['HIGH'] +  df['OPEN'])/4
        
        df_indicators = pd.DataFrame()
        
        temp_list = [None for i in range(len(df))]
        indic_columnhead = 'LOCALVOL ' + str(n)
        df_indicators[indic_columnhead] = temp_list
        
        local_vol = [None for i in range(n)]
        
        initial_start_ctr = 0
        initial_end_ctr = n
        
        for i in range(len(df) - n):
            
            lookback_list = list(df['TYP PRICE'].iloc[initial_start_ctr : initial_end_ctr])
            sigma = std(lookback_list)
            
            local_vol.append(sigma)
                
            initial_start_ctr += 1
            initial_end_ctr += 1

        df_indicators[indic_columnhead] = local_vol
        
        self.df_generatedIndicators = df_indicators

#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'LOCALVOL'):
        indic_df = self.df_generatedIndicators
        n = self.lookback_period
        
        df_internal = pd.DataFrame()
        
        indic_list = list(indic_df[indic_name + ' ' + str(n)])
        indic_list = indic_list[n:]
        
        a = min(indic_list)
        b = max(indic_list)
        b_dash = 100
        a_dash = 0
        scaled_signal_list = [None for i in range(n)]
        for i in indic_list:
            frac = (i - a)/(b - a)
            val1 = frac*(b_dash - a_dash)
            scaled_val = val1 + a_dash
            scaled_signal_list.append(scaled_val)
        
        df_internal[indic_name + ' SIGNAL ' + str(n)] = scaled_signal_list
        
        self.df_generatedSignal = df_internal

#######################
#Live Signal Generation Function
#######################

    def live_signal(self, live_lookback = 1):
        indic_name = 'LOCALVOL'
        mid_string = 'SIGNAL'
        n = self.lookback_period
        col_head = indic_name + ' ' + mid_string + ' ' + str(n)
        out_list = []
        for i in range(-live_lookback, 0):
            out_list.append(self.df_generatedSignal[col_head].iloc[i])
        return out_list

#######################
#Run Function
#######################

    def run(self, live_lookback = 1):
        self.indicator_generator()
        self.signal_generation()
        live_signal = self.live_signal(live_lookback)

        return live_signal
