'''
Name: ENVELOPE EMA

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: 
        Mid-Channel: ENVEMA + lookback_period + d_percentage
        Up_channel: ENVUPENVEMA + lookback_period + d_percentage
        Down-Channel: ENVDOWNENVEMA + lookback_period + d_percentage
    
    Signal Generated DataFrame head: ENVEMA SIGNAL + lookback_period + d_percentage
    Signum Generated DataFrame head: ENVEMA SIGNUM + lookback_period + d_percentage

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Long/Short Strength

Usage Notes:
* A moving average smooths out price fluctuations and allows us to see the broader pattern of the market. A moving average that slopes upward confirms that prices have been trending upwards. * Conversely, if a MA line slopes downward, it indicates a downtrend. With our Envelopes indicator, we can also look at the direction of our bands to inform us about the trend. If our bands are sloping upward, then it confirms an uptrend. If our bands are sloping downward, it confirms a downtrend.
* As a simple trend-following signal, we can look for those times when the current price crosses above a moving average line. This may be a signal for a breakout into a new upward trend. Likewise, a downward crossover of the price through the moving average may signal a new downtrend. We can use the Envelopes indicator in a similar manner. With our Envelopes, they display MA lines that have been shifted up and down.
    
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
Inputs: dataframe_input, lookback_period, d_percentage = 2, sensitivity = 1.3, absolute_sensitivity = 85
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

class EnvelopeEMA:
    def __init__(self, dataframe_input, lookback_period, d_percentage = 2, sensitivity = 1.3, absolute_sensitivity = 85):
        df_generatedIndicators = pd.DataFrame() #Generated from indicator_generator

        df_generatedSignal = pd.DataFrame() #Generated from signal_generation

        df_trainTest = pd.DataFrame() #Generated from train_test
        total_return = 0
        return_potential_ratio = 0

        self.dataframe_input = dataframe_input
        self.lookback_period = lookback_period
        self.d_percentage = d_percentage
        self.sensitivity = sensitivity
        self.absolute_sensitivity = absolute_sensitivity

#######################
#Indicator Generator Function
#######################

    def indicator_generator(self):
        df = self.dataframe_input
        n = self.lookback_period
        m = self.d_percentage

        df['TYP PRICE'] =  (df['CLOSE'] +  df['LOW'] +  df['HIGH'] +  df['OPEN'])/4
        
        df_indicators = pd.DataFrame()
                
        temp_list = [None for i in range(len(df))]
        indic_columnhead = 'ENVEMA ' + str(n) + ' ' + str(m)
        df_indicators[indic_columnhead] = temp_list
            
        ema = [None for i in range(n)]
        env_up = [None for i in range(n+1)]
        env_down = [None for i in range(n+1)]
        
        initial_start_ctr = 1
        initial_end_ctr = n + 1
        
        sum_var = sum(list(df['TYP PRICE'].iloc[0 : n]))
        base_val = sum_var/n
        ema.append(base_val)
        
        for i in range(len(df) - n - 1):
            
            lookback_list = list(df['TYP PRICE'].iloc[initial_start_ctr : initial_end_ctr])
            sigma = m/100
            
            price_list = lookback_list
            k = 2 / (n+1)
            price_t = df['TYP PRICE'].iloc[initial_end_ctr]
            
            ema_val = price_t*k + base_val*(1 - k)
            ema.append(ema_val)
            
            env_up.append(ema_val * (1+sigma))
            env_down.append(ema_val * (1-sigma))
            
            initial_start_ctr += 1
            initial_end_ctr += 1
            base_val = ema_val

        df_indicators[indic_columnhead] = ema
        df_indicators['ENVUP' + indic_columnhead] =  env_up
        df_indicators['ENVDOWN' + indic_columnhead] = env_down
        
        self.df_generatedIndicators = df_indicators
    
#######################
#Signal Generation Dividers
#######################

    def signal_generation(self, indic_name = 'ENVEMA'):
        df = self.dataframe_input
        indic_df = self.df_generatedIndicators
        d_percentage = self.d_percentage
        sensitivity = self.sensitivity
        df_internal = pd.DataFrame()
        n = self.lookback_period
        m = self.d_percentage
        
        df_internal['TYP PRICE'] =  (df['CLOSE'] +  df['LOW'] +  df['HIGH'] +  df['OPEN'])/4
        df_internal['UPBOUND'] = indic_df['ENVUPENVEMA ' + str(n) + ' ' + str(m)]
        df_internal['DOWNBOUND'] = indic_df['ENVDOWNENVEMA ' + str(n) + ' ' + str(m)]
        df_internal['MIDLINE'] = indic_df['ENVEMA ' + str(n) + ' ' + str(m)]
        
        df_internal['UPBOUND_DIST'] = abs(df_internal['TYP PRICE'] - df_internal['UPBOUND'])
        df_internal['DOWNBOUND_DIST'] = abs(df_internal['DOWNBOUND'] - df_internal['TYP PRICE'])
        df_internal['UPBREAKOUT_SIGNAL'] = df_internal['TYP PRICE'] > df_internal['UPBOUND']
        df_internal['DOWNBREAKOUT_SIGNAL'] = df_internal['TYP PRICE'] < df_internal['DOWNBOUND']
        
        upbound_dist_max = df_internal['UPBOUND_DIST'].max()
        downbound_dist_max = df_internal['DOWNBOUND_DIST'].max()
        
        price_list = list(df_internal['TYP PRICE'])
        upbound_dist_list = list(df_internal['UPBOUND_DIST'])
        downbound_dist_list = list(df_internal['DOWNBOUND_DIST'])
        upbreakout_list = list(df_internal['UPBREAKOUT_SIGNAL'])
        downbreakout_list = list(df_internal['DOWNBREAKOUT_SIGNAL'])
        mid_list = list(df_internal['MIDLINE'])
        interest_list = []
        
        for i in range(n + 1,len(indic_df)):
            long_interest = 0
            short_interest = 0
            if (upbreakout_list[i]):
                long_interest = upbound_dist_max + upbound_dist_list[i]
                short_interest = 0
            elif (downbreakout_list[i]):
                short_interest = downbound_dist_max + downbound_dist_list[i]
                long_interest = 0
            else:
                short_interest = upbound_dist_max - upbound_dist_list[i]
                long_interest = downbound_dist_max - downbound_dist_list[i]
                if (price_list[i] <= mid_list[i]):
                    short_interest = short_interest/2
                elif (price_list[i] > mid_list[i]):
                    long_interest = long_interest/2
            non_linear_projection = long_interest - short_interest
            interest_list.append(non_linear_projection)
            
        #scaling
        a = min(interest_list)
        b = max(interest_list)
        b_dash = 100
        a_dash = -100
        scaled_interest_list_out = [None for i in range(n + 1)]
        scaled_interest_list = []
        for i in interest_list:
            frac = (i - a)/(b - a)
            val1 = frac*(b_dash - a_dash)
            scaled_val = val1 + a_dash
            scaled_interest_list.append(scaled_val)
            scaled_interest_list_out.append(scaled_val)
            
        df_out = pd.DataFrame()
        df_out['ENVEMA SIGNAL ' + str(n) + ' ' + str(m)] = scaled_interest_list_out
        
        #signum truth table construction
        indic_mean = df_out['ENVEMA SIGNAL ' + str(n) + ' ' + str(m)].mean()
        absolute_mean = 0
        indic_std = df_out['ENVEMA SIGNAL ' + str(n) + ' ' + str(m)].std()
        absolute_std = self.absolute_sensitivity
        
        df_internal['ENVEMA SIGNUM BUY ' + str(n) + ' ' + str(m)] = df_out['ENVEMA SIGNAL ' + str(n) + ' ' + str(m)] >  (indic_mean + indic_std * sensitivity)
        df_internal['ENVEMA SIGNUM SELL ' + str(n) + ' ' + str(m)] = df_out['ENVEMA SIGNAL ' + str(n) + ' ' + str(m)] <=  (indic_mean - indic_std * sensitivity)
        df_internal['ABSOLUTE ENVEMA SIGNUM BUY ' + str(n) + ' ' + str(m)] = df_out['ENVEMA SIGNAL ' + str(n) + ' ' + str(m)] >  (absolute_mean + absolute_std * sensitivity)
        df_internal['ABSOLUTE ENVEMA SIGNUM SELL ' + str(n) + ' ' + str(m)] = df_out['ENVEMA SIGNAL ' + str(n)+ ' ' + str(m)] <=  (absolute_mean - absolute_std * sensitivity)
    
        #indicator signum
        long = list(df_internal['ENVEMA SIGNUM BUY ' + str(n) + ' ' + str(m)])
        short = list(df_internal['ENVEMA SIGNUM SELL ' + str(n) + ' ' + str(m)])
        
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
            
        df_out['ENVEMA SIGNUM ' + str(n) + ' ' + str(m)] = indic_out
        
        #absolute signum
        abs_long = list(df_internal['ABSOLUTE ENVEMA SIGNUM BUY ' + str(n) + ' ' + str(m)])
        abs_short = list(df_internal['ABSOLUTE ENVEMA SIGNUM SELL ' + str(n) + ' ' + str(m)])
        
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
        
        df_out['ABSOLUTE ENVEMA SIGNUM ' + str(n) + ' ' + str(m)] = abs_out
        
        self.df_generatedSignal = df_out

#######################
#Train Test Function
#######################

    def train_test(self, indic_name = 'ENVEMA', stop_percent = 0.05):
        df = self.dataframe_input
        signal_df = self.df_generatedSignal
        n = self.lookback_period
        m = self.d_percentage
        signum_colhead = indic_name + ' ' + 'SIGNUM' + ' ' + str(n) + ' ' + str(m)
        
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
        indic_name = 'ENVEMA'
        mid_string = 'SIGNUM'
        n = self.lookback_period
        m = self.d_percentage
        col_head = indic_name + ' ' + mid_string + ' ' + str(n) + ' ' + str(m)
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
