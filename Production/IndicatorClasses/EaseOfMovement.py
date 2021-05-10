'''
Name: EASE OF MOVEMENT

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: EOM SMA + lookback_period
    Signal Generated DataFrame head: EOM SMA SIGNAL + lookback_period

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Whipsaw/Volatility

Usage Notes:
* Richard Arms' Ease of Movement indicator is a technical study that attempts to quantify a mix of momentum and volume information into one value. The intent is to use this value to discern whether prices are able to rise, or fall, with little resistance in the directional movement. Theoretically, if prices move easily, they will continue to do so for a period of time that can be traded effectively.
* Some analysts prefer to add a moving average to the EMV line and use it as a trigger line to generate trading signals. Traders may also look for divergences and convergences between the Ease of Movement and price as a signal of upcoming reversals. 
* Oscillates above and below the zero line
* Use the oscillator as a gauge to see how quickly we need get in or out of the trade.
* **USE FOR RATE OF THETA BURN**
    
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
Outputs: live_signal
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

class EaseOfMovement:

    def __init__(self, dataframe_input, lookback_period):
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
        
        df_indicators = pd.DataFrame()
                
        temp_list = [None for i in range(len(df))]
        indic_columnhead = 'EASE OF MOVEMENT ' + str(n)
        df_indicators[indic_columnhead] = temp_list
        
        order_mag = 10**(math.floor(math.log10(df['VOLUME'].iloc[0])))
        
        df_indicators['VOLUME ADJ'] = df['VOLUME']/order_mag
        df_indicators['BOX RATIO'] = df_indicators['VOLUME ADJ']/(df['HIGH'] - df['LOW'])
        
        df_copy = df
        df_shifted = df.shift(1)
        df_indicators['DISTANCE'] = ((df_copy['HIGH'] + df_copy['LOW']) - (df_shifted['HIGH'] + df_shifted['LOW']))/2
        
        df_indicators[indic_columnhead] = df_indicators['DISTANCE']/df_indicators['BOX RATIO']
        
        initial_start_ctr = 0
        initial_end_ctr = n
        
        df_indicators['EOM SMA ' + str(n)] = df_indicators[indic_columnhead].rolling(n).mean()
        self.df_generatedIndicators = df_indicators

#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'EOM SMA'):
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
        indic_name = 'EOM SMA'
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
