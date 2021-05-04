'''
Name: FISHER TRANSFORM REVERSAL

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: FISHER TRANSFORM + lookback_period
    Signal Generated DataFrame head: FISHER TRANSFORM REVERSAL SIGNAL + lookback_period
    Signum Generated DataFrame head: FISHER TRANSFORM REVERSAL SIGNUM + lookback_period

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Long/Short Strength

Usage Notes:
* The Fisher Transform indicator is unbounded, which means extremes can occur for a long time. An extreme is based on the historical readings for the asset in question. For some assets, a high reading may be seven or eight, while a low reading may be -4. For another asset, these values may differ.
* An extreme reading indicates the possibility of a reversal. This should be confirmed by the Fisher Transform changing direction. For example, following a strong price rise and the Fisher Transform reaching an extremely high level, when the Fisher Transform starts to head lower that could signal the price is going to drop, or has already started dropping.
* _Signal Line:_ The Fisher Transform frequently has a signal line attached to it. This is a moving average of the Fisher Transform value, so it moves slightly slower than the Fisher Transform line. When the Fisher Transform crosses the trigger line it is used by some traders as a trade signal. For example, when the Fisher Transform drops below the signal line after hitting an extreme high, that could be used as a signal to sell a current long position.
    
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

class FisherTransformReversal:

    def __init__(self, dataframe_input, lookback_period, sensitivity = 1.2, absolute_sensitivity = 50):
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
        df_indicators['DATE'] = df['DATE']
        df['TYP PRICE'] =  (df['CLOSE'] +  df['LOW'] +  df['HIGH'] +  df['OPEN'])/4
        indic_columnhead = 'FISHER TRANSFORM ' + str(n)
        fisher_transform = [None for i in range(n)]
        
        initial_start_ctr = 0
        initial_end_ctr = n
        
        for i in range(len(df) - n):
            
            min_price = min(list(df['LOW'].iloc[initial_start_ctr : initial_end_ctr]))
            max_price = max(list(df['HIGH'].iloc[initial_start_ctr : initial_end_ctr]))
            current_price = df['TYP PRICE'].iloc[initial_end_ctr]
            
            X = ((current_price - min_price)*2/(max_price - min_price)) - 1
            frac = abs((1 - X)/(1 + X))
            transform_val = 0.5*math.log(frac)*100
            
            fisher_transform.append(transform_val)

            initial_start_ctr += 1
            initial_end_ctr += 1

        df_indicators[indic_columnhead] = fisher_transform
        df_indicators['MA ' + indic_columnhead] = df_indicators[indic_columnhead].rolling(n).mean()
        df_indicators['OSC FISH TRANS ' + str(n)] =   df_indicators[indic_columnhead] - df_indicators['MA ' + indic_columnhead]
        
        self.df_generatedIndicators = df_indicators
    
#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'FISHER TRANSFORM'):
        indic_df = self.df_generatedIndicators
        n = self.lookback_period
        sensitivity = self.sensitivity
        
        df_internal = pd.DataFrame()
        df_internal['DATE'] = indic_df['DATE']
        df_out = pd.DataFrame()
        df_out['DATE'] = indic_df['DATE']
        
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

    def train_test(self, indic_name = 'FISHER TRANSFORM REVERSAL', stop_percent = 0.05):
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
        indic_name = 'FISHER TRANSFORM REVERSAL'
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
