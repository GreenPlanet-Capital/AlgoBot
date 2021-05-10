'''
Name: RELATIVE STRENGTH INDEX

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: RSI + lookback_period 
    Signal Generated DataFrame head: RSI REVERSAL SIGNAL + lookbcak_period
    Signum Generated DataFrame head: RSI REVERSAL SIGNUM + lookbcak_period

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Long/Short Strength

Usage Notes:
* The RSI will rise as the number and size of positive closes increase, and it will fall as the number and size of losses increase. The second part of the calculation smooths the result, so the RSI will only near 100 or 0 in a strongly trending market.
* Can be used as an oscillator
* Bullish Swing Rejection Signal: 
* * RSI falls into oversold territory.
* * RSI crosses back above 30%.
* * RSI forms another dip without crossing back into oversold territory.
* * RSI then breaks its most recent high.
* Bearish Swing Rejection Signal
* * RSI rises into overbought territory.
* * RSI crosses back below 70%.
* * RSI forms another high without crossing back into overbought territory.
* * RSI then breaks its most recent low.
* A bullish divergence occurs when the RSI creates an oversold reading followed by a higher low that matches correspondingly lower lows in the price. This indicates rising bullish momentum, and a break above oversold territory could be used to trigger a new long position.
* A bearish divergence occurs when the RSI creates an overbought reading followed by a lower high that matches corresponding higher highs on the price. 
    
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

class RelativeStrengthIndex:

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
        df = self.dataframe_input
        n = self.lookback_period
        df_indicators = pd.DataFrame()
        df['TYP PRICE'] = (df['LOW'] + df['HIGH'] + df['CLOSE'] + df['OPEN'])/4
        
        temp_list = [None for i in range(len(df))]
        indic_columnhead = 'RSI ' + str(n)
        df_indicators[indic_columnhead] = temp_list
        
        rsi_list = [None for i in range(n + 1)]
        
        initial_start_ctr = 1
        initial_end_ctr = n+1
        
        for i in range(len(df) - n - 1):
            avg_gain = 0
            avg_loss = 0
            
            prev_price_list = list(df['TYP PRICE'].iloc[(initial_start_ctr - 1) : (initial_end_ctr - 1)])
            current_price_list = list(df['TYP PRICE'].iloc[initial_start_ctr : initial_end_ctr])
            
            for i,j in zip(prev_price_list,current_price_list):
                if (j > i):
                    avg_gain += (j - i)
                elif (i <= j):
                    avg_loss += (i - j)
            try:         
                rs = avg_gain/avg_loss
            except ZeroDivisionError as e:
                rs = max(avg_gain,avg_loss)
            finally:
                rsi = 100 - (100/(1+rs))
            rsi_list.append(rsi)
            
            initial_start_ctr += 1
            initial_end_ctr += 1

        df_indicators[indic_columnhead] = rsi_list
        
        self.df_generatedIndicators = df_indicators
    
#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'RSI'):
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
                append_val = -100
            elif (long[i] == False and short[i] == True):
                append_val = 100
            else:
                append_val = 0 
            indic_out.append(append_val)
            
        df_out[indic_name + ' REVERSAL SIGNUM ' + str(n)] = indic_out
        
        self.df_generatedSignal = df_out

#######################
#Train Test Function
#######################

    def train_test(self, indic_name = 'RSI REVERSAL', stop_percent = 0.05):
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
        indic_name = 'RSI REVERSAL'
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
