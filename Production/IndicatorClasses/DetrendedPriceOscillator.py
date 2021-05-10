'''
Name: DETRENDED PRICE OSCILLATOR

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: 
    Signal Generated DataFrame head: 
    Signum Generated DataFrame head: 

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal

Type of Indicator: Whipsaw/Volatility

Usage Notes:
* The detrended price oscillator seeks to help a trader identify an asset's price cycle. It does this by comparing an SMA to a historical price that is near the middle of the look-back period
* By looking at historical peaks and troughs on the indicator, which aligned with peaks and troughs in price, traders will typically draw vertical lines at these junctures and then count how much time elapsed between them
* Measuring the average time of reversal allows us to predict the next reversal that may be coming soon.
    
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
Inputs: dataframe_input, lookback_period, sensitivity = , absolute_sensitivity = 
Outputs: weight, live_signal
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

class DetrendedPriceOscillator:

    def __init__(self, dataframe_input, lookback_period, sensitivity = 1, absolute_sensitivity = 50):
        df_generatedIndicators = pd.DataFrame() #Generated from indicator_generator

        df_generatedSignal = pd.DataFrame() #Generated from signal_generation

        self.dataframe_input = dataframe_input
        self.lookback_period = lookback_period
        
#######################
#Indicator Generator Function
#######################

    def indicator_generator(self):
        df = self.dataframe_input
        n = self.lookback_period
        
        df['TYP PRICE'] =  (df['CLOSE'] +  df['LOW'] +  df['HIGH'] +  df['OPEN'])/4
        
        df_indicators = pd.DataFrame()
        
        temp_list = [None for i in range(len(df))]
        indic_columnhead = 'DPO ' + str(n)
        df_indicators[indic_columnhead] = temp_list
        
        initial_gap = len(df) - int(len(df)/n)*n
        
        dpo = [None for i in range(n)]
        
        initial_start_ctr = 0
        initial_end_ctr = n
        
        for i in range(len(df) - n):
            
            price_list = list(df['TYP PRICE'].iloc[initial_start_ctr : initial_end_ctr])
            median_price = df['TYP PRICE'].iloc[initial_start_ctr + int(n/2 + 1)]

            sum_var = sum(price_list)
            sma_val = sum_var/n

            dpo_val =  median_price - sma_val
            dpo.append(dpo_val)
                
            initial_start_ctr += 1
            initial_end_ctr += 1

        df_indicators[indic_columnhead] = dpo
        
        self.df_generatedIndicators = df_indicators
    
#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'DPO'):
        n = self.lookback_period
        indic_df = self.df_generatedIndicators
        
        df_internal = pd.DataFrame()
        
        indic_list = list(indic_df[indic_name + ' ' + str(n)])
        indic_list = indic_list[n:]
        
        a = min(indic_list)
        b = max(indic_list)
        b_dash = 100
        a_dash = 0
        scaled_signal_list = [None for i in range(n)]
        for i in indic_list:
            try:
                frac = (i - a)/(b - a)
                val1 = frac*(b_dash - a_dash)
                scaled_val = val1 + a_dash
                scaled_signal_list.append(scaled_val)
            except:
                scaled_signal_list.append(0)
        
        df_internal[indic_name + ' SIGNAL ' + str(n)] = scaled_signal_list
        
        self.df_generatedSignal = df_internal

#######################
#Live Signal Generation Function
#######################

    def live_signal(self, live_lookback = 1):
        indic_name = 'DPO'
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
