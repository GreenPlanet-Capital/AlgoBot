import pandas as pd
import numpy as np
import math 
import multiprocessing as mp

'''
inputs: 
    dict_of_dataframes
    base_lookback
    multiplier1
    multiplier2
    lin_reg_filter_multiplier
    number_of_readings 
    filter_percentile = 75
    filter_activation_flag = True 
    long_only_flag = False
output: ordered list

ticker_data_list format: (ticker, breakout_score, filter_linreg, ls_strength)
'''
class OptimisedModel: 
    ticker_data_list = []
    percentile_limit = 0
    unordered_dict= {}
    def __init__(self, dict_of_dataframes, base_lookback, multiplier1, multiplier2, lin_reg_filter_multiplier, number_of_readings, filter_percentile = 75, filter_activation_flag = True, long_only_flag = False):
        self.base_lookback = base_lookback
        self.dict_of_dataframes = dict_of_dataframes
        self.lin_reg_filter_multiplier = lin_reg_filter_multiplier
        self.multiplier1 = multiplier1
        self.multiplier2 = multiplier2
        self.number_of_readings = number_of_readings
        self.filter_percentile = filter_percentile
        self.filter_activation_flag = filter_activation_flag
        self.long_only_flag = long_only_flag

    def array_slicer(self, df_input):
        df_input['Typical Price'] = ((df_input['HIGH'] + df_input['LOW'] + df_input['CLOSE']) / 3).round(2)
        price_array = np.array(df_input['Typical Price'])

        linreg_lookback = math.ceil(self.base_lookback*self.lin_reg_filter_multiplier)
        lookback1 = math.ceil(self.base_lookback*self.multiplier1)
        lookback2 = math.ceil(self.base_lookback*self.multiplier2) 

        lin_reg_array = price_array[-linreg_lookback:] 
        main_lookback_array = price_array[-self.base_lookback:]
        multiplier1_lookback_array = price_array[-lookback1:]
        multiplier2_lookback_array = price_array[-lookback2:]
        present_price = price_array[-1]
        return present_price, lin_reg_array,main_lookback_array, multiplier1_lookback_array, multiplier2_lookback_array
    
    def generate_listOfTickers(self):
        in_dict = self.dict_of_dataframes
        ticker_list = []
        for ticker in in_dict:
            ticker_list.append(ticker)
        return ticker_list

    def lin_reg(self, price_array):
        n = len(price_array)
        sum_y = 0
        sum_xy = 0
        sum_x = (n+1)*n/2
        sum_x2 = n*(n+1)*(2*n+1)/6
        for i,j in enumerate(price_array):
            sum_y += j
            sum_xy += (i+1)*j 
        lin_reg = (n*sum_xy - (sum_x*sum_y))/((n*sum_x2) - (sum_x*sum_x))
        return lin_reg
    
    def std(self, price_array):
        std_val = np.std(price_array)
        return std_val

    def wma(self, price_array):
        sum_val = 0 
        div = len(price_array)
        for j,i in enumerate(price_array):
            sum_val += (j+1)*i
        wma_val = (sum_val*2)/(div*(div+1))
        return wma_val

    def sma(self, price_array):
        sma_val = np.sum(price_array)/len(price_array)
        return sma_val

    def mcg(self, price_array):
        len_pa = len(price_array)
        base_val_array = price_array[:len_pa - 1]
        base_val = np.sum(base_val_array)/len(base_val_array)
        numer = (price_array[-1] - base_val)
        denom = len_pa*((price_array[-1]/base_val)**4)
        frac = numer/denom
        mcg_val = frac + base_val
        return mcg_val
    
    def envelope_score(self, df_input):
        present_price, lin_reg_array,main_lookback_array, multiplier1_lookback_array, multiplier2_lookback_array = self.array_slicer(df_input)

        bol_std_val1 = 1
        bol_std_val2 = 1.3
        bol_std_val3 = 1.6
        env_std_val1 = 0.017
        env_std_val2 = 0.02
        env_std_val3 = 0.023

        std1 = self.std(main_lookback_array)
        std2 = self.std(multiplier1_lookback_array)
        std3 = self.std(multiplier2_lookback_array)

        sma1 = self.sma(main_lookback_array)
        sma2 = self.sma(multiplier1_lookback_array)
        sma3 = self.sma(multiplier2_lookback_array)

        wma1 = self.wma(main_lookback_array)
        wma2 = self.wma(multiplier1_lookback_array)
        wma3 = self.wma(multiplier2_lookback_array)

        mcg1 = self.mcg(main_lookback_array)
        mcg2 = self.mcg(multiplier1_lookback_array)
        mcg3 = self.mcg(multiplier2_lookback_array)

        long_iterator = []
        short_iterator = []
        ls_iterator = []

        #SMA
        #Base_Lookback Envelopes
        long_iterator.append(sma1 + (bol_std_val1*std1))
        long_iterator.append(sma1 + (bol_std_val2*std1))
        long_iterator.append(sma1 + (bol_std_val3*std1))

        long_iterator.append(sma1 + (env_std_val1*sma1))
        long_iterator.append(sma1 + (env_std_val2*sma1))
        long_iterator.append(sma1 + (env_std_val3*sma1))

        short_iterator.append(sma1 - (bol_std_val1*std1))
        short_iterator.append(sma1 - (bol_std_val2*std1))
        short_iterator.append(sma1 - (bol_std_val3*std1))

        short_iterator.append(sma1 - (env_std_val1*sma1))
        short_iterator.append(sma1 - (env_std_val2*sma1))
        short_iterator.append(sma1 - (env_std_val3*sma1))
        
        #Multiplier1_Lookback Envelopes
        long_iterator.append(sma2 + (bol_std_val1*std2))
        long_iterator.append(sma2 + (bol_std_val2*std2))
        long_iterator.append(sma2 + (bol_std_val3*std2))

        long_iterator.append(sma2 + (env_std_val1*sma2))
        long_iterator.append(sma2 + (env_std_val2*sma2))
        long_iterator.append(sma2 + (env_std_val3*sma2))

        short_iterator.append(sma2 - (bol_std_val1*std2))
        short_iterator.append(sma2 - (bol_std_val2*std2))
        short_iterator.append(sma2 - (bol_std_val3*std2))

        short_iterator.append(sma2 - (env_std_val1*sma2))
        short_iterator.append(sma2 - (env_std_val2*sma2))
        short_iterator.append(sma2 - (env_std_val3*sma2))

        #Multiplier2_Lookback Envelopes
        long_iterator.append(sma3 + (bol_std_val1*std3))
        long_iterator.append(sma3 + (bol_std_val2*std3))
        long_iterator.append(sma3 + (bol_std_val3*std3))

        long_iterator.append(sma3 + (env_std_val1*sma3))
        long_iterator.append(sma3 + (env_std_val2*sma3))
        long_iterator.append(sma3 + (env_std_val3*sma3))

        short_iterator.append(sma3 - (bol_std_val1*std3))
        short_iterator.append(sma3 - (bol_std_val2*std3))
        short_iterator.append(sma3 - (bol_std_val3*std3))

        short_iterator.append(sma3 - (env_std_val1*sma3))
        short_iterator.append(sma3 - (env_std_val2*sma3))
        short_iterator.append(sma3 - (env_std_val3*sma3))

        #WMA
        #Base_Lookback Envelopes
        long_iterator.append(wma1 + (bol_std_val1*std1))
        long_iterator.append(wma1 + (bol_std_val2*std1))
        long_iterator.append(wma1 + (bol_std_val3*std1))

        long_iterator.append(wma1 + (env_std_val1*wma1))
        long_iterator.append(wma1 + (env_std_val2*wma1))
        long_iterator.append(wma1 + (env_std_val3*wma1))

        short_iterator.append(wma1 - (bol_std_val1*std1))
        short_iterator.append(wma1 - (bol_std_val2*std1))
        short_iterator.append(wma1 - (bol_std_val3*std1))

        short_iterator.append(wma1 - (env_std_val1*wma1))
        short_iterator.append(wma1 - (env_std_val2*wma1))
        short_iterator.append(wma1 - (env_std_val3*wma1))
        
        #Multiplier1_Lookback Envelopes
        long_iterator.append(wma2 + (bol_std_val1*std2))
        long_iterator.append(wma2 + (bol_std_val2*std2))
        long_iterator.append(wma2 + (bol_std_val3*std2))

        long_iterator.append(wma2 + (env_std_val1*wma2))
        long_iterator.append(wma2 + (env_std_val2*wma2))
        long_iterator.append(wma2 + (env_std_val3*wma2))

        short_iterator.append(wma2 - (bol_std_val1*std2))
        short_iterator.append(wma2 - (bol_std_val2*std2))
        short_iterator.append(wma2 - (bol_std_val3*std2))

        short_iterator.append(wma2 - (env_std_val1*wma2))
        short_iterator.append(wma2 - (env_std_val2*wma2))
        short_iterator.append(wma2 - (env_std_val3*wma2))

        #Multiplier2_Lookback Envelopes
        long_iterator.append(wma3 + (bol_std_val1*std3))
        long_iterator.append(wma3 + (bol_std_val2*std3))
        long_iterator.append(wma3 + (bol_std_val3*std3))

        long_iterator.append(wma3 + (env_std_val1*wma3))
        long_iterator.append(wma3 + (env_std_val2*wma3))
        long_iterator.append(wma3 + (env_std_val3*wma3))

        short_iterator.append(wma3 - (bol_std_val1*std3))
        short_iterator.append(wma3 - (bol_std_val2*std3))
        short_iterator.append(wma3 - (bol_std_val3*std3))

        short_iterator.append(wma3 - (env_std_val1*wma3))
        short_iterator.append(wma3 - (env_std_val2*wma3))
        short_iterator.append(wma3 - (env_std_val3*wma3))

        #MCG
        #Base_Lookback Envelopes
        long_iterator.append(mcg1 + (bol_std_val1*std1))
        long_iterator.append(mcg1 + (bol_std_val2*std1))
        long_iterator.append(mcg1 + (bol_std_val3*std1))

        long_iterator.append(mcg1 + (env_std_val1*mcg1))
        long_iterator.append(mcg1 + (env_std_val2*mcg1))
        long_iterator.append(mcg1 + (env_std_val3*mcg1))

        short_iterator.append(mcg1 - (bol_std_val1*std1))
        short_iterator.append(mcg1 - (bol_std_val2*std1))
        short_iterator.append(mcg1 - (bol_std_val3*std1))

        short_iterator.append(mcg1 - (env_std_val1*mcg1))
        short_iterator.append(mcg1 - (env_std_val2*mcg1))
        short_iterator.append(mcg1 - (env_std_val3*mcg1))
        
        #Multiplier1_Lookback Envelopes
        long_iterator.append(mcg2 + (bol_std_val1*std2))
        long_iterator.append(mcg2 + (bol_std_val2*std2))
        long_iterator.append(mcg2 + (bol_std_val3*std2))

        long_iterator.append(mcg2 + (env_std_val1*mcg2))
        long_iterator.append(mcg2 + (env_std_val2*mcg2))
        long_iterator.append(mcg2 + (env_std_val3*mcg2))

        short_iterator.append(mcg2 - (bol_std_val1*std2))
        short_iterator.append(mcg2 - (bol_std_val2*std2))
        short_iterator.append(mcg2 - (bol_std_val3*std2))

        short_iterator.append(mcg2 - (env_std_val1*mcg2))
        short_iterator.append(mcg2 - (env_std_val2*mcg2))
        short_iterator.append(mcg2 - (env_std_val3*mcg2))

        #Multiplier2_Lookback Envelopes
        long_iterator.append(mcg3 + (bol_std_val1*std3))
        long_iterator.append(mcg3 + (bol_std_val2*std3))
        long_iterator.append(mcg3 + (bol_std_val3*std3))

        long_iterator.append(mcg3 + (env_std_val1*mcg3))
        long_iterator.append(mcg3 + (env_std_val2*mcg3))
        long_iterator.append(mcg3 + (env_std_val3*mcg3))

        short_iterator.append(mcg3 - (bol_std_val1*std3))
        short_iterator.append(mcg3 - (bol_std_val2*std3))
        short_iterator.append(mcg3 - (bol_std_val3*std3))

        short_iterator.append(mcg3 - (env_std_val1*mcg3))
        short_iterator.append(mcg3 - (env_std_val2*mcg3))
        short_iterator.append(mcg3 - (env_std_val3*mcg3))

        #CCI_SMA1
        cci_sma1 = (present_price - sma1)/std1*0.015
        #CCI_SMA2
        cci_sma2 = (present_price - sma2)/std2*0.015
        #CCI_SMA3
        cci_sma3 = (present_price - sma3)/std3*0.015

        #CCI_WMA1
        cci_wma1 = (present_price - wma1)/std1*0.015
        #CCI_WMA2
        cci_wma2 = (present_price - wma2)/std2*0.015
        #CCI_WMA3
        cci_wma3 = (present_price - wma3)/std3*0.015

        #CCI_MCG1
        cci_mcg1 = (present_price - mcg1)/std1*0.015
        #CCI_MCG2
        cci_mcg2 = (present_price - mcg2)/std2*0.015
        #CCI_MCG3
        cci_mcg3 = (present_price - mcg3)/std3*0.015

        #SMA1_SMA2
        sma1_sma2 = sma1 - sma2
        #SMA2_SMA3
        sma2_sma3 = sma2 - sma3
        #SMA1_SMA3
        sma1_sma3 = sma1 - sma3

        #WMA1_WMA2
        wma1_wma2 = wma1 - wma2
        #WMA2_WMA3
        wma2_wma3 = wma2 - wma3
        #WMA1_WMA3
        wma1_wma3 = wma1 - wma3
        
        #MCG1_MCG2
        mcg1_mcg2 = mcg1 - mcg2
        #MCG2_MCG3
        mcg2_mcg3 = mcg2 - mcg3
        #MCG1_MCG3
        mcg1_mcg3 = mcg1 - mcg3

        #WMA1_SMA1
        wma1_sma1 = wma1 - sma1
        #WMA1_MCG1
        wma1_mcg1 = wma1 - mcg1

        #WMA2_SMA2
        wma2_sma2 = wma2 - sma2
        #WMA2_MCG2
        wma2_mcg2 = wma2 - mcg2

        #WMA3_SMA3
        wma3_sma3 = wma3 - sma3
        #WMA3_MCG3
        wma3_mcg3 = wma3 - mcg3

        #Lin Regression 
        linreg1 = self.lin_reg(main_lookback_array)
        linreg2 = self.lin_reg(multiplier1_lookback_array)
        linreg3 = self.lin_reg(multiplier2_lookback_array)

        ls_iterator = [
            cci_sma1, cci_sma2, cci_sma3, 
            cci_wma1, cci_wma2, cci_wma3, 
            cci_mcg1, cci_mcg2, cci_mcg3, 
            sma1_sma2, sma2_sma3, sma1_sma3,
            wma1_wma2, wma2_wma3, wma1_wma3,
            mcg1_mcg2, mcg2_mcg3, mcg1_mcg3,
            linreg1, linreg2, linreg3
            ]
        
        breakout_score = 0
        for i,j in zip(long_iterator,short_iterator):
            if (present_price >= i):
                breakout_score += 1
            if (present_price <= j):
                breakout_score -= 1
 
        ls_strength = 0
        for i in ls_iterator:
            if (i > 0):
                ls_strength += 1
            elif (i < 0):
                ls_strength -= 1

        filter_linreg = self.lin_reg( lin_reg_array)

        return breakout_score, filter_linreg, ls_strength        


    def data_generator(self):
        stock_list = self.generate_listOfTickers()
        for ticker in stock_list:
            breakout_score, filter_linreg, ls_strength = self.envelope_score(self.dict_of_dataframes[ticker])
            self.ticker_data_list.append((ticker, breakout_score, filter_linreg, ls_strength))

    def percentile_limit_gen(self):
        abs_percentile_array = np.array([])
        if(self.long_only_flag):
            for i in self.ticker_data_list:
                if(i[1] > 0):
                    abs_percentile_array = np.append(abs_percentile_array,i[1])
        else:
            for i in self.ticker_data_list:
                abs_percentile_array = np.append(abs_percentile_array, abs(i[1]))
        percentile_limit = np.percentile(abs_percentile_array, self.filter_percentile)
        self.percentile_limit = percentile_limit

    def filters(self):
        filtered_dict = {}
        for i in self.ticker_data_list:
            try:
                #LinReg Filter
                if (i[1] > 0 and i[2] < 0):
                    self.ticker_data_list.remove(i)
                elif(i[1] < 0 and i[2] > 0):
                    self.ticker_data_list.remove(i)
                elif(i[1] == 0):
                    self.ticker_data_list.remove(i)

                #Contradiction Filter
                if (i[1] > 0 and i[3] < 0):
                    self.ticker_data_list.remove(i)
                elif(i[1] < 0 and i[3] > 0):
                    self.ticker_data_list.remove(i)
            except ValueError:
                continue

            #Percentile Filter
            if(self.long_only_flag):
                if (i[1] >= self.percentile_limit):
                    if((i[3] + i[1]) > 0):
                        filtered_dict[i[0]] = i[3] + i[1]
            else:
                if (abs(i[1]) >= self.percentile_limit):
                    filtered_dict[i[0]] = i[3] + i[1]


        self.unordered_dict = filtered_dict

    def pure_breakout_signal(self):
        out_dict = {}
        for i in self.ticker_data_list:
            out_dict[i[0]] = i[3] + i[1]
        self.unordered_dict = out_dict

#ticker_data_list format: (ticker, breakout_score, filter_linreg, ls_strength)

    def ordering(self):
        generated_dict = self.unordered_dict
        num = self.number_of_readings
        short_book = []
        long_book = []
        sorted_list = sorted(generated_dict.items(),key = lambda kv: kv[1])
        for i, ((short_ticker,short_data),(long_ticker,long_data)) in enumerate(zip(sorted_list,reversed(sorted_list))):
            if(i==num):
                break
            if(short_data<0):
                short_book.append((short_ticker, short_data))
            if(long_data>0):
                long_book.append((long_ticker,long_data))
        return long_book, short_book

    def run(self):
        self.data_generator()
        if (self.filter_activation_flag):
            self.percentile_limit_gen()
            self.filters()
        else:
            self.pure_breakout_signal()
        print(self.ordering())

            

    

        

