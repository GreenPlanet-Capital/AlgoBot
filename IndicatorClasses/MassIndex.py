'''
Name: ACCUMULATION DISTRIBUTION

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: MASS INDEX + lookback_period
    Signal Generated DataFrame head: MASS INDEX SIGNAL + lookback_period
    Signum Generated DataFrame head: MASS INDEX SIGNUM + lookback_period

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal

Type of Indicator: Reversal Strength

Usage Notes: 
* Intuitively, a higher value may indicate that a reversal may be in the works
* In essence, indiates the speed of rise and fall in volatility
* Has low correlation to price action
    
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
Inputs: dataframe_input, lookback_period, sensitivity = 0.9, absolute_sensitivity = 50
Outputs: live_signal
'''
import math
import pandas as pd
import json 
import datetime
import numpy as np
import sys
import oauth2client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.text

class MassIndex:
    def __init__(self, dataframe_input, lookback_period, sensitivity = 0.9, absolute_sensitivity = 50):
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
        def ema(input_list, lookback_period):    
            ctr = 0
            for i in input_list:
                if (str(i) == 'nan'):
                    input_list.remove(i)
                    ctr += 1
                elif (i == None):
                    input_list.remove(None)
                    ctr += 1
            n = lookback_period

            ema = [None for i in range(n + ctr)]

            initial_start_ctr = 1
            initial_end_ctr = n + 1

            sum_var = sum(input_list[0 : n])
            base_val = sum_var/n
            ema.append(base_val)
                
            for i in range(len(input_list) - n - 1):

                price_list = input_list[initial_start_ctr : initial_end_ctr]
                k = 2 / (n+1)
                price_t = input_list[initial_end_ctr]

                ema_val = price_t*k + base_val*(1 - k)
                ema.append(ema_val)

                initial_start_ctr += 1
                initial_end_ctr += 1
                base_val = ema_val
            return ema
        
        df = self.dataframe_input
        n = self.lookback_period
        df_indicators = pd.DataFrame()
        df_indicators['DATE'] = df['DATE']
        
        df['DIF'] =  df['HIGH'] - df['LOW']   
        dif_list = list(df['DIF']) 

        ema_list_1 = ema(dif_list,n)
        df_indicators['DIFEMA1 ' + str(n)] = ema_list_1
        ema_list_2 = ema(dif_list,2*n)
        df_indicators['DIFEMA2 ' + str(n)] = ema_list_2
        
        indic_columnhead = 'MASS INDEX ' + str(n)
        df_indicators[indic_columnhead] = df_indicators['DIFEMA1 ' + str(n)] / df_indicators['DIFEMA2 ' + str(n)]
        
        self.df_generatedIndicators = df_indicators
    

#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'MASS INDEX'):
        indic_df = self.df_generatedIndicators
        sensitivity = self.sensitivity
        n = self.lookback_period
        
        df_internal = pd.DataFrame()
        df_internal['DATE'] = indic_df['DATE']
        df_out = pd.DataFrame()
        df_out['DATE'] = indic_df['DATE']
        
        indic_list = list(indic_df[indic_name + ' ' + str(n)])
        indic_list = indic_list[3*n:]
        
        a = min(indic_list)
        b = max(indic_list)
        b_dash = 100
        a_dash = 0
        scaled_signal_list = [None for i in range(3*n)]
        for i in indic_list:
            frac = (i - a)/(b - a)
            val1 = frac*(b_dash - a_dash)
            scaled_val = val1 + a_dash
            scaled_signal_list.append(scaled_val)

        df_out[indic_name + ' SIGNAL' + ' ' + str(n)] = scaled_signal_list
        
        #signum truth table construction
        indic_mean = df_out[indic_name + ' SIGNAL ' + str(n)].mean()
        indic_std = df_out[indic_name +  ' SIGNAL ' + str(n)].std()
        
        df_internal[indic_name + ' SIGNUM ' + str(n)] = df_out[indic_name + ' SIGNAL ' + str(n)] >  (indic_mean + indic_std * sensitivity)
        
        #indicator signum
        long = list(df_internal[indic_name + ' SIGNUM ' + str(n)])
        
        indic_out = [] 
        for i in range(len(long)):
            append_val = 0
            if (long[i] == True):
                append_val = 100
            else:
                append_val = 0 
            indic_out.append(append_val)
            
        df_out[indic_name + ' SIGNUM ' + str(n)] = indic_out
        
        self.df_generatedSignal = df_out


    def live_signal(self, live_lookback = 1):
        indic_name = 'MASS INDEX'
        mid_string = 'SIGNUM'
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
