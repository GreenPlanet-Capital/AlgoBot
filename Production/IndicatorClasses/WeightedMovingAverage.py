'''
Name: WEIGHTED MOVING AVERAGE

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: OSC WMA + lookback_period1 + WMA + lookback_period2 
    Signal Generated DataFrame head: OSC WMA + lookback_period1 + WMA SIGNAL + lookback_period2
    Signum Generated DataFrame head: OSC WMA + lookback_period1 + WMA SIGNUM + lookback_period2

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Long/Short Strength

Usage Notes: 
* It is the relative movement of close prices on a log graph. Uses an oscillator generator
* Constantly Measures slope in order to ascertain the average directional movement of the stock
* Flatlining Directional Movement may show entry or exit points, if confidence in a trend is slowing down

    
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
Inputs: dataframe_input, lookback_period1, lookback_period2, sensitivity = 1, absolute_sensitivity = 50 
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

class WeightedMovingAverage:

    def __init__(self, dataframe_input, lookback_period1, lookback_period2, sensitivity = 1.2, absolute_sensitivity = 50):
        df_generatedIndicators = pd.DataFrame() #Generated from indicator_generator

        df_generatedSignal = pd.DataFrame() #Generated from signal_generation

        df_trainTest = pd.DataFrame() #Generated from train_test
        total_return = 0
        return_potential_ratio = 0

        self.dataframe_input = dataframe_input
        self.lookback_period1 = lookback_period1
        self.lookback_period2 = lookback_period2
        self.sensitivity = sensitivity
        self.absolute_sensitivity = absolute_sensitivity

#######################
#Indicator Generator Function
#######################

    def indicator_generator(self):
        def wma(dataframe_input, lookback_period):
            df = dataframe_input
            n = lookback_period
            
            df['TYP PRICE'] =  (df['CLOSE'] +  df['LOW'] +  df['HIGH'] +  df['OPEN'])/4
            
            df_indicators = pd.DataFrame()
            
            temp_list = [None for i in range(len(df))]
            indic_columnhead = 'WMA ' + str(lookback_period)
            df_indicators[indic_columnhead] = temp_list
            
            initial_gap = len(df) - int(len(df)/n)*n
            
            wma = [None for i in range(n)]
            
            initial_start_ctr = 0
            initial_end_ctr = n
            
            for i in range(len(df) - n):
                
                price_list = list(df['TYP PRICE'].iloc[initial_start_ctr : initial_end_ctr])
                
                weighted_list = []
                weight = 1
                for ii in price_list:
                    weighted_list.append(ii*weight)
                    weight += 1
                    
                weighted_sum = sum(weighted_list) 
                m = n*(n+1)/2
                    
                wma_val = weighted_sum/m
                wma.append(wma_val)
                    
                initial_start_ctr += 1
                initial_end_ctr += 1

            df_indicators[indic_columnhead] = wma
            
            return df_indicators

        osc_df = pd.DataFrame()
        df = self.dataframe_input
        short_lookback = self.lookback_period1
        long_lookback = self.lookback_period2
        shorterterm_df = wma(df, short_lookback)
        longerterm_df = wma(df, long_lookback)
        shortindic_name = 'WMA'
        longindic_name = 'WMA'     
        
        short_name = shortindic_name + ' ' + str(short_lookback)
        long_name = longindic_name + ' ' + str(long_lookback)
        osc_df_colname = 'OSC ' + short_name + ' ' + long_name
        osc_df[osc_df_colname] = shorterterm_df[short_name] - longerterm_df[long_name]
        
        self.df_generatedIndicators = osc_df
    
#######################
#Signal Generation Dividers
#######################

    def signal_generation(self):
        osc_df = self.df_generatedIndicators
        shortindic_name = 'WMA'
        short_lookback = self.lookback_period1
        longindic_name = 'WMA'
        long_lookback = self.lookback_period2
        sensitivity = self.sensitivity

        indic_name = 'OSC ' + shortindic_name + ' ' + str(short_lookback) + ' ' + longindic_name
        n = long_lookback
        indic_df = osc_df
        
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
            frac = (i - a)/(b - a)
            val1 = frac*(b_dash - a_dash)
            scaled_val = val1 + a_dash
            scaled_signal_list.append(scaled_val)
        
        df_out = pd.DataFrame()
        df_out[indic_name + ' SIGNAL' + ' ' + str(n)] = scaled_signal_list
        
        #signum truth table construction
        indic_mean = df_out[indic_name + ' SIGNAL ' + str(n)].mean()
        absolute_mean = 0
        indic_std = df_out[indic_name +  ' SIGNAL ' + str(n)].std()
        absolute_std = self.absolute_sensitivity
        
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

    def train_test(self, stop_percent = 0.05):
        df = self.dataframe_input
        signal_df = self.df_generatedSignal
        indic_name = 'OSC WMA ' + str(self.lookback_period1) + ' WMA'
        n = self.lookback_period2
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
        indic_name = 'OSC WMA ' + str(self.lookback_period1) + ' WMA'
        mid_string = 'SIGNUM'
        n = self.lookback_period2
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
