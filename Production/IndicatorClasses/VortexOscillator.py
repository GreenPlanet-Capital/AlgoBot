'''
Name: VORTEX OSCILLATOR

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: VORTEX OSCILLATOR + lookback_period
    Signum Generated DataFrame head: VORTEX OSCILLATOR REVERSAL SIGNUM + lookback_period

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Long/Short Strength

Usage Notes:
* Crossovers of the two trend lines signal a reversal
* Highest divergence between the two trend line indicates a possible lower confidence in the trend

    
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
Inputs: dataframe_input, lookback_period, sensitivity = 1.3, absolute_sensitivity = 50
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

class VortexOscillator:

    def __init__(self, dataframe_input, lookback_period, sensitivity = 1.3, absolute_sensitivity = 50):
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
        def atr(dataframe_input, lookback_period):
            df = dataframe_input
            n = lookback_period

            df_indicators = pd.DataFrame()

            temp_list = [None for i in range(len(df))]
            indic_columnhead = 'ATR ' + str(lookback_period)
            df_indicators[indic_columnhead] = temp_list

            initial_gap = len(df) - int(len(df)/n)*n
        
            low_list = [None for i in range(n)]
            high_list = [None for i in range(n)]
            close_list = [None for i in range(n)]
            atr = [None for i in range(n)]

            initial_start_ctr = 0
            initial_end_ctr = n

            for i in range(len(df) - n):

                low_price = min(list(df['LOW'].iloc[initial_start_ctr : initial_end_ctr]))
                low_list.append(low_price)

                high_price = max(list(df['HIGH'].iloc[initial_start_ctr : initial_end_ctr]))
                high_list.append(high_price)

                close_price = df['CLOSE'].iloc[initial_end_ctr]
                close_list.append(close_price)

                atr_val = max([abs(high_price - low_price), abs(high_price - close_price), abs(low_price - close_price)])

                atr_val = atr_val/n

                atr.append(atr_val)

                initial_start_ctr += 1
                initial_end_ctr += 1

            df_indicators[indic_columnhead] = atr

            return df_indicators
        
        df = self.dataframe_input
        n = self.lookback_period
        
        df_indicators = pd.DataFrame()
        
        temp_list = [None for i in range(len(df))]
        indic_columnhead1 = 'VORTEX+ ' + str(n)
        indic_columnhead2 = 'VORTEX- ' + str(n)
        df_indicators[indic_columnhead1] = temp_list
        df_indicators[indic_columnhead2] = temp_list
        
        atr_df = atr(df,n)
        
        ref_col = 'ATR ' + str(n) 
        atr_df[ref_col] = atr_df[ref_col]*n
        
        initial_gap = len(df) - int(len(df)/n)*n
        
        VIn_plus = [None for i in range(n+1)]
        VIn_minus = [None for i in range(n+1)]
        
        vortex = [None for i in range(n)]
        
        initial_start_ctr = 1
        initial_end_ctr = n + 1
        
        for i in range(len(df) - n - 1):
            
            today_low_price = min(list(df['LOW'].iloc[initial_start_ctr : initial_end_ctr]))
            prev_low_price = min(list(df['LOW'].iloc[(initial_start_ctr - 1) : (initial_end_ctr - 1)]))
            today_high_price = max(list(df['HIGH'].iloc[initial_start_ctr : initial_end_ctr]))
            prev_high_price = max(list(df['HIGH'].iloc[(initial_start_ctr - 1) : (initial_end_ctr - 1)]))
            
            sum_atr_val = atr_df[ref_col].iloc[initial_end_ctr]
            
            vm_plus = abs(today_high_price - prev_low_price)
            vm_minus = abs(today_low_price - prev_high_price)
            
            VIn_plus_val = vm_plus/sum_atr_val
            VIn_minus_val = (vm_minus/sum_atr_val)
                                
            VIn_plus.append(VIn_plus_val)
            VIn_minus.append(VIn_minus_val)
                                
            initial_start_ctr += 1
            initial_end_ctr += 1

        df_indicators[indic_columnhead1] = VIn_plus
        df_indicators[indic_columnhead2] = VIn_minus
        
        df_indicators['VORTEX OSCILLATOR ' + str(n)] = df_indicators[indic_columnhead1] - df_indicators[indic_columnhead2]
                                
        self.df_generatedIndicators = df_indicators
    
#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'VORTEX OSCILLATOR'):
        indic_df = self.df_generatedIndicators
        sensitivity = self.sensitivity
        n = self.lookback_period
        
        df_internal = pd.DataFrame()
        df_out = pd.DataFrame()
        
        indic_list = list(indic_df[indic_name + ' ' + str(n)])
        indic_list = indic_list[n:]
        
        #signum truth table construction
        indic_mean = indic_df[indic_name + ' ' + str(n)].mean()
        indic_std = indic_df[indic_name +  ' ' + str(n)].std()
        
        df_internal[indic_name + ' SIGNUM BUY ' + str(n)] = indic_df[indic_name + ' ' + str(n)] <  (indic_mean + (indic_std * sensitivity))
        df_internal[indic_name + ' SIGNUM SELL ' + str(n)] = indic_df[indic_name + ' ' + str(n)] >=  (indic_mean - (indic_std * sensitivity))

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
            
        df_out[indic_name + ' REVERSAL SIGNUM ' + str(n)] = indic_out
        
        self.df_generatedSignal = df_out

#######################
#Train Test Function
#######################

    def train_test(self, indic_name = 'VORTEX OSCILLATOR REVERSAL', stop_percent = 0.05):
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
        indic_name = 'VORTEX OSCILLATOR REVERSAL'
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
