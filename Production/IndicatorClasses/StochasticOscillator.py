'''
Name: STOCHASTIC OSCILLATOR

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: STOCH OSC + lookback_period
    Signal Generated DataFrame head: STOCH OSC SIGNAL + lookback_period
    Signum Generated DataFrame head: STOCH OSC SIGNUM + lookback_period

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Long/Short Strength 

Usage Notes:
* The general theory serving as the foundation for this indicator is that in a market trending upward, prices will close near the high, and in a market trending downward, prices close near the low. 
* Transaction signals are created when the %K crosses through a three-period moving average, which is called the %D.

* Traditionally, readings over 80 are considered in the overbought range, and readings under 20 are considered oversold. 
* However, these are not always indicative of impending reversal; very strong trends can maintain overbought or oversold conditions for an extended period. 
* Stochastic oscillator charting generally consists of two lines: one reflecting the actual value of the oscillator for each session, and one reflecting its three-day simple moving average. Because price is thought to follow momentum, the intersection of these two lines is considered to be a signal that a reversal may be in the works, as it indicates a large shift in momentum from day to day.
* Divergence between the stochastic oscillator and trending price action is also seen as an important reversal signal. For example, when a bearish trend reaches a new lower low, but the oscillator prints a higher low, it may be an indicator that bears are exhausting their momentum and a bullish reversal is brewing.

    
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
Inputs: dataframe_input, lookback_period, sensitivity = 1, absolute_sensitivity = 50
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

class StochasticOscillator:

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
        df = self.dataframe_input
        n = self.lookback_period
        df_indicators = pd.DataFrame()
        
        temp_list = [None for i in range(len(df))]
        indic_columnhead = 'STOCH OSC ' + str(n)
        df_indicators[indic_columnhead] = temp_list
        
        percent_k_list = [None for i in range(n)]
        
        initial_start_ctr = 0
        initial_end_ctr = n
        
        for i in range(len(df) - n):
            
            low_price = min(list(df['LOW'].iloc[initial_start_ctr : initial_end_ctr]))
            high_price = max(list(df['HIGH'].iloc[initial_start_ctr : initial_end_ctr]))       
            close_price = df['CLOSE'].iloc[initial_end_ctr]
                            
            percent_k = (close_price - low_price)*100/(high_price - low_price)
            percent_k_list.append(percent_k)
            
            initial_start_ctr += 1
            initial_end_ctr += 1
                            
        df_indicators['PERCENT K ' + str(n)] = percent_k_list
        df_indicators['PERCENT D ' + str(n)] = df_indicators['PERCENT K '  + str(n)].rolling(3).mean()
        df_indicators[indic_columnhead] = df_indicators['PERCENT K '  + str(n)] - df_indicators['PERCENT D ' + str(n)]
        
        self.df_generatedIndicators = df_indicators
    
#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'STOCH OSC'):
        indic_df = self.df_generatedIndicators 
        sensitivity = self.sensitivity
        n = self.lookback_period
        
        df_internal = pd.DataFrame()
        
        indic_list = list(indic_df[indic_name + ' ' + str(n)])
        indic_list = indic_list[n - 1:]
        
        signal_append = 0
        signal_list = []
        
        for i in range(len(indic_list) - 1):
            if (indic_list[i] > 0 and indic_list[i + 1] <= 0):
                signal_append = indic_list[i + 1] - indic_list[i]
            elif (indic_list[i] < 0 and indic_list[i + 1] >= 0):
                signal_append = indic_list[i + 1] - indic_list[i]
            else:
                signal_append = 0
            signal_list.append(signal_append)
        
        a = min(signal_list)
        b = max(signal_list)
        b_dash = 100
        a_dash = -100
        scaled_signal_list = [None for i in range(n)]
        for i in signal_list:
            try: 
                frac = (i - a)/(b - a)
                val1 = frac*(b_dash - a_dash)
                scaled_val = val1 + a_dash
                scaled_signal_list.append(scaled_val)
            except:
                scaled_signal_list.append(0)
        
        df_out = pd.DataFrame()
        df_out[indic_name + ' SIGNAL' + ' ' + str(n)] = scaled_signal_list
        
        #signum truth table construction
        indic_mean = df_out[indic_name + ' SIGNAL ' + str(n)].mean()
        absolute_mean = 0
        indic_std = df_out[indic_name +  ' SIGNAL ' + str(n)].std()
        absolute_std = 50
        
        df_internal[indic_name + ' SIGNUM BUY ' + str(n)] = df_out[indic_name + ' SIGNAL ' + str(n)] >  (indic_mean + indic_std * sensitivity)
        df_internal[indic_name + ' SIGNUM SELL ' + str(n)] = df_out[indic_name + ' SIGNAL ' + str(n)] <=  (indic_mean - indic_std * sensitivity)
        df_internal['ABSOLUTE ' + indic_name + ' SIGNUM BUY ' + str(n)] = df_out[indic_name + ' SIGNAL ' + str(n)] >  (absolute_mean + (absolute_std * sensitivity))
        df_internal['ABSOLUTE ' + indic_name + ' SIGNUM SELL ' + str(n)] = df_out[indic_name + ' SIGNAL ' + str(n)] <=  (absolute_mean - (absolute_std * sensitivity))
        
        #indicator signum
        long = list(df_internal[indic_name + ' SIGNUM BUY ' + str(n)])
        short = list(df_internal[indic_name + ' SIGNUM SELL ' + str(n)])
        
        indic_out = [] 
        for i in range(len(long)):
            append_val = 0
            if (long[i] == True and short[i] == False):
                append_val = 100
            elif (long[i] == False and short[i] == True):
                append_val = -100
            else:
                append_val = 0 
            indic_out.append(append_val)
            
        df_out[indic_name + ' SIGNUM ' + str(n)] = indic_out
        
        #absolute signum
        abs_long = list(df_internal['ABSOLUTE ' + indic_name + ' SIGNUM BUY ' + str(n)])
        abs_short = list(df_internal['ABSOLUTE ' + indic_name + ' SIGNUM SELL ' + str(n)])
        
        abs_out = [] 
        for i in range(len(long)):
            append_val = 0
            if (abs_long[i] == True and abs_short[i] == False):
                append_val = 100
            elif (abs_long[i] == False and abs_short[i] == True):
                append_val = -100
            else:
                append_val = 0 
            abs_out.append(append_val)
        
        df_out['ABSOLUTE ' + indic_name + ' SIGNUM ' + str(n)] = abs_out
        
        self.df_generatedSignal = df_out

#######################
#Train Test Function
#######################

    def train_test(self, indic_name = 'STOCH OSC', stop_percent = 0.05):
        df = self.dataframe_input
        signal_df = self.df_generatedSignal
        n = self.lookback_period
        signum_colhead = indic_name + ' ' + 'SIGNUM' + ' ' + str(n)
        
        df_internal = pd.DataFrame()
        df_internal['TYP PRICE'] = (df['OPEN'] + df['CLOSE'] + df['HIGH'] + df['LOW'])/4
        df_internal['POSITION INDEX'] = [None for i in range(len(signal_df))]
        
        price_list = list(df_internal['TYP PRICE'])
        signum_list = list(signal_df[signum_colhead])
        
        position_list = []
        
        position_flag = 'NEUTRAL'
        entry_price = 0
        long_book = [None for i in range(len(price_list))]
        short_book = [None for i in range(len(price_list))]
        
        open_long = []
        open_short = []
        long_pos_list = []
        short_pos_list = []
        
        for x in range(len(price_list)):
            i = signum_list[x]
            j = price_list[x]
            if (x == (len(price_list) - 1)):
                long_pos_list.append(open_long)
                short_pos_list.append(open_short)
                
            if (position_flag == 'NEUTRAL'):   
                if (i == 100):
                    position_flag = 'LONG'
                    entry_price = j
                    long_book[x] = j
                    open_long.append(j)
                    continue 
                elif (i == -100):
                    position_flag = 'SHORT'
                    entry_price = j
                    short_book[x] = j
                    open_short.append(j)
                    continue
                elif (i == 0):
                    position_flag = 'NEUTRAL'
                    continue
            elif (position_flag == 'LONG'):
                if (i == 100):
                    open_long.append(j)
                    trailing_stop = max(open_long) - max(open_long)*stop_percent
                    absolute_stop = entry_price - entry_price*stop_percent
                    if (j < absolute_stop or j < trailing_stop):
                        position_flag = 'NEUTRAL'
                        entry_price = 0
                        long_pos_list.append(open_long)
                        open_long = []
                        continue
                    else:
                        position_flag = 'LONG'
                        long_book[x] = j
                        continue
                elif (i == -100):
                    position_flag = 'SHORT'
                    entry_price = j
                    short_book[x] = j
                    long_pos_list.append(open_long)
                    open_long = []
                    continue
                elif (i == 0):
                    open_long.append(j)
                    trailing_stop = max(open_long) - max(open_long)*stop_percent
                    absolute_stop = entry_price - entry_price*stop_percent
                    if (j < absolute_stop or j < trailing_stop):
                        position_flag = 'NEUTRAL'
                        entry_price = 0
                        long_pos_list.append(open_long)
                        open_long = []
                        continue
                    else:
                        position_flag = 'LONG'
                        long_book[x] = j
                        continue
            elif (position_flag == 'SHORT'):
                if (i == 100):
                    position_flag = 'LONG'
                    entry_price = j
                    long_book[x] = j
                    short_pos_list.append(open_short)
                    open_short = []
                    continue 
                elif (i == -100):
                    open_short.append(j)
                    trailing_stop = min(open_short) + max(open_short)*stop_percent
                    absolute_stop = entry_price + entry_price*stop_percent
                    if (j > absolute_stop or j > trailing_stop):
                        position_flag = 'NEUTRAL'
                        entry_price = 0
                        short_pos_list.append(open_short)
                        open_short = []
                        continue
                    else:
                        position_flag = 'SHORT'
                        short_book[x] = j
                        continue
                elif (i == 0):
                    open_short.append(j)
                    trailing_stop = min(open_short) + max(open_short)*stop_percent
                    absolute_stop = entry_price + entry_price*stop_percent
                    if (j > absolute_stop or j > trailing_stop):
                        position_flag = 'NEUTRAL'
                        entry_price = 0
                        short_pos_list.append(open_short)
                        open_short = []
                        continue
                    else:
                        position_flag = 'SHORT'
                        short_book[x] = j
                        continue
        long_return = 0
        short_return = 0
        for i in (long_pos_list):
            if (i == []):
                long_pos_list.remove(i)
                continue
            len_i = len(i) - 1
            long_return += i[len_i] - i[0]
            
        for j in (short_pos_list):
            if (j == []):
                short_pos_list.remove(j)
                continue
            len_j = len(j) - 1
            short_return += j[0] - j[len_j]
            
        total_return = long_return - short_return
        possible_return = abs(price_list[n] - min(price_list)) + abs(max(price_list) - min(price_list)) + abs(price_list[-1] - max(price_list))
        return_potential_ratio = total_return/possible_return
        
        df_internal['LONG BOOK'] = long_book
        df_internal['SHORT BOOK'] = short_book
        
        self.total_return = total_return
        self.return_potential_ratio = return_potential_ratio
        self.df_trainTest = df_internal

        return return_potential_ratio

#######################
#Live Signal Generation Function
#######################

    def live_signal(self, live_lookback = 1):
        indic_name = 'STOCH OSC'
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
        weight = self.train_test()
        live_signal = self.live_signal(live_lookback)

        return weight, live_signal
