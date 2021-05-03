'''
Name: CHOPPINESS INDEX

Naming Convention of DataFrame Columns: 
    Indicator Generated DataFrame head: 
    Signal Generated DataFrame head: 
    Signum Generated DataFrame head: 

Function List:
    indicator_generator
    signal_generation
    train_test
    live_signal
    run

Type of Indicator: Whipsaw/Volatility Indicator

Usage Notes: Used to lower confidence in the current trend
    
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
Inputs: dataframe_input, lookback_period
Outputs: weight, live_signal
'''

