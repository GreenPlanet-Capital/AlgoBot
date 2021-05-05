'''
Name: ACCUMULATION DISTRIBUTION

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: 
    Signal Generated DataFrame head: 
    Signum Generated DataFrame head: 

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal

Type of Indicator: 

Usage Notes:
    
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

class TradingRange:

    def __init__(self, dataframe_input, lookback_period, sensitivity = 1.2, absolute_sensitivity = 50):
        df_generatedIndicators = pd.DataFrame() #Generated from indicator_generator

        self.dataframe_input = dataframe_input
        self.lookback_period = lookback_period
        self.trading_range = 0

#######################
#Indicator Generator Function
#######################

    def indicator_generator(self):
        df = self.dataframe_input
        n = self.lookback_period

        df_highlist = list(df['HIGH'])
        df_lowlist = list(df['LOW'])

        trading_range = max(df_highlist[-n:]) - min(df_lowlist[-n:])
        self.trading_range = trading_range

#######################
#Run Function
#######################

    def run(self, live_lookback = 1):
        self.indicator_generator()
        out = self.trading_range
        return out
