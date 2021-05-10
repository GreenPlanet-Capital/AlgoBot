'''
Name: CHAIKIN OSCILLATOR

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: CHAIKIN OSCILLATOR + lookback_period
    Signal Generated DataFrame head: CHAIKIN OSCILLATOR SIGNAL +  lookback_period
    Signum Generated DataFrame head: CHAIKIN OSCILLATOR SIGNUM +  lookback_period

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Long/Short Strength

Usage Notes: * The Chaikin oscillator utilizes two primary buy and 
sell signals. First, a positive divergence is confirmed with a center-line crossover
above the accumulation-distribution line. signaling a potential buying opportunity. 
* Second, a negative divergence is confirmed with a center-line crossover below the
accumulation-distribution line., signaling a potential selling opportunity.
    
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

class ChaikinOscillator:

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
        def ema(input_list, lookback_period):
            while None in input_list:
                input_list.remove(None)
            
            n = lookback_period

            ema = [None for i in range(n)]

            initial_start_ctr = 1
            initial_end_ctr = n + 1

            sum_var = sum(input_list[0 : n])
            base_val = sum_var/n
            ema.append(base_val)
                
            for i in range(len(input_list) - n - n):

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
        
        temp_list = [None for i in range(len(df))]
        indic_columnhead = 'CHAIKIN OSCILLATOR ' + str(n)
        df_indicators[indic_columnhead] = temp_list
        
        low_list = [None for i in range(n)]
        high_list = [None for i in range(n)]
        close_list = [None for i in range(n)]
        volume_list = [None for i in range(n)]
        cmfv_list = [None for i in range(n)]
        cmfv_final_list = [None]
        
        initial_start_ctr = 0
        initial_end_ctr = n
        
        for i in range(len(df) - n):
            
            low_price = min(list(df['LOW'].iloc[initial_start_ctr : initial_end_ctr]))
            low_list.append(low_price)
            
            high_price = max(list(df['HIGH'].iloc[initial_start_ctr : initial_end_ctr]))
            high_list.append(high_price)
            
            close_price = df['CLOSE'].iloc[initial_end_ctr]
            close_list.append(close_price)
            
            volume = sum(list(df['VOLUME'].iloc[initial_start_ctr : initial_end_ctr]))
            volume_list.append(volume)
            
            
            cmfv_val1 = (2*close_price - low_price - high_price) * volume
            cmfv_val2 = cmfv_val1 / (high_price - low_price)
            cmfv_list.append(cmfv_val2)
            
            initial_start_ctr += 1
            initial_end_ctr += 1

        for i in range(len(df) - 1):
            try:
                ad = cmfv_list[i] + cmfv_list[i+1]
                cmfv_final_list.append(ad)
            except:
                cmfv_final_list.append(None)
                
        df_indicators['ACCUMULATION DISTRIBUTION ' + str(n)] = cmfv_final_list

        while None in cmfv_final_list:
                cmfv_final_list.remove(None)
        
        co_up = ema(cmfv_final_list,n)
        co_down = ema(cmfv_final_list,2*n)
        
        co = [None for i in range(3*n)]
        for (i,j) in zip(co_up,co_down):
            try:
                co.append(i - j)
            except:
                co.append(None)
                
        
        df_indicators[indic_columnhead] = co
        
        self.df_generatedIndicator = df_indicators

#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'CHAIKIN OSCILLATOR'):
        sensitivity = self.sensitivity
        indic_name = 'CHAIKIN OSCILLATOR'
        n = self.lookback_period
        indic_df = self.df_generatedIndicator

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

    def train_test(self, indic_name = 'CHAIKIN OSCILLATOR', stop_percent = 0.05):
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
        indic_name = 'CHAIKIN OSCILLATOR'
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
