'''
Name: HISTORICAL VOLATILITY

Function List:
    indicator_generator
    signal_generation
    run

Type of Indicator: Volatility

Usage Notes: Historical Volatility
    
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
Outputs: value of hist_volatility
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

class HistoricalVolatility:

    def __init__(self, dataframe_input):
        self.dataframe_input = dataframe_input

#######################
#Indicator Generator Function
#######################

    def indicator_generator(self):
        df = self.dataframe_input
        
        df_indicators = pd.DataFrame()
        df_indicators['TYP PRICE'] =  (df['CLOSE'] + df['OPEN'] + df['HIGH'] + df['LOW'])/4
        hist_vol = df_indicators['TYP PRICE'].std()

        return hist_vol

#######################
#Run Function
#######################

    def run(self, garbage_value = 1):
        return self.indicator_generator()
