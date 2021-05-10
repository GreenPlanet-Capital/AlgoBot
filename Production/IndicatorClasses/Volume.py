'''
Name: VOLUME

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: 
    Signal Generated DataFrame head: 
    Signum Generated DataFrame head: 

Function List:
    indicator_generator
    run

Type of Indicator: Volume

Usage Notes:
1. **Trend Confirmation:**
A rising market should see rising volume. Buyers require increasing numbers and increasing enthusiasm in order to keep pushing prices higher. Increasing price and decreasing volume might suggest a lack of interest, and this is a warning of a potential reversal. This can be hard to wrap your mind around, but the simple fact is that a price drop (or rise) on little volume is not a strong signal. A price drop (or rise) on large volume is a stronger signal that something in the stock has fundamentally changed.
2. **Exhaustion Moves and Volume:**
In a rising or falling market, we can see exhaustion moves. These are generally sharp moves in price combined with a sharp increase in volume, which signals the potential end of a trend. Participants who waited and are afraid of missing more of the move pile in at market tops, exhausting the number of buyers. At a market bottom, falling prices eventually force out large numbers of traders, resulting in volatility and increased volume. We will see a decrease in volume after the spike in these situations, but how volume continues to play out over the next days, weeks, and months can be analyzed using the other volume guidelines.
3. **Bullish Signs:**
Volume can be useful in identifying bullish signs. For example, imagine volume increases on a price decline and then the price moves higher, followed by a move back lower. If the price on the move back lower doesn't fall below the previous low, and volume is diminished on the second decline, then this is usually interpreted as a bullish sign.
4. **Volume and Price Reversals:** 
After a long price move higher or lower, if the price begins to range with little price movement and heavy volume, this might indicate that a reversal is underway, and prices will change direction.
5. **Volume and Breakouts vs. False Breakouts:**
On the initial breakout from a range or other chart pattern, a rise in volume indicates strength in the move. Little change in volume or declining volume on a breakout indicates a lack of interest and a higher probability for a false breakout. 
    
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
Inputs: dataframe_input
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

class Volume:

    def __init__(self, dataframe_input):
        df_generatedIndicators = pd.DataFrame() #Generated from indicator_generator
        self.dataframe_input = dataframe_input
        
#######################
#Indicator Generator Function
#######################

    def indicator_generator(self):
        df = self.dataframe_input
        df_indicators = pd.DataFrame()
        
        signal_list = list(df['VOLUME'])
        a = min(signal_list)
        b = max(signal_list)
        b_dash = 100
        a_dash = -100
        scaled_signal_list = []
        for i in signal_list:
            frac = (i - a)/(b - a)
            val1 = frac*(b_dash - a_dash)
            scaled_val = val1 + a_dash
            scaled_signal_list.append(scaled_val)
            
        df_indicators['VOLUME'] = scaled_signal_list
        
        self.df_generatedIndicators = df_indicators

#######################
#Live Signal Generation Function
#######################

    def live_signal(self, live_lookback = 1):
        indic_name = 'VOLUME'
        col_head = indic_name
        out_list = []
        for i in range(-live_lookback, 0):
            out_list.append(self.df_generatedIndicators[col_head].iloc[i])
        return out_list

#######################
#Run Function
#######################

    def run(self, live_lookback = 1):
        self.indicator_generator()
        live_signal = self.live_signal(live_lookback)

        return live_signal
