import numpy as np
import math
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import yfinance as yf

class EnvelopeSMA:
    plot_width = 5
    plot_length = 3
    indic_runtime = 0
    bias_runtime = 0
    efficacy_runtime = 0
    live_output = 0
    efficacy_value = 0

    def __init__(self, price_array, lookback, multiplier = 1.2):
        self.price_array = price_array
        self.lookback = lookback 
        self.multiplier = multiplier
        self.up_bound_array = np.array([])
        self.sma_arr = np.array([])
        self.down_bound_array = np.array([])
        self.bias_array = np.array([])
        self.long_book = np.array([])
        self.short_book = np.array([])
        self.long_cash = 0
        self.short_cash = 0

    def env_sma_gen(self):
        price_array = self.price_array
        lookback = self.lookback
        multiplier = self.multiplier
        up_bound_array = np.array([None for i in range(price_array.size)])
        down_bound_array = np.array([None for i in range(price_array.size)])
        
        def sma(price_array, lookback):
            out_array = np.array([None for i in range(lookback)])
            for i in range(price_array.size - lookback):
                out_val = (np.sum(price_array[i:i+lookback])/lookback)
                out_array = np.append(out_array,out_val)
            return out_array
        
        sma_arr = sma(price_array, lookback)
        for i in range(price_array.size - lookback):
            up_bound_array[i+lookback] = sma_arr[i+lookback] + (sma_arr[i+lookback]*multiplier)
            down_bound_array[i+lookback] = sma_arr[i+lookback] - (sma_arr[i+lookback]*multiplier)

        self.up_bound_array = up_bound_array
        self.sma_arr = sma_arr
        self.down_bound_array = down_bound_array

    def current_bias(self):
        price_array = self.price_array
        up_bound_array = self.up_bound_array
        down_bound_array = self.down_bound_array

        bias = 0
        bias_list = []
        for i,j,k in zip(price_array,up_bound_array, down_bound_array):
            try: 
                if(i >= j):
                    bias = 100
                elif(i <= k):
                    bias = -100
                elif(i > k and i < j):
                    bias = 0
            except TypeError:
                bias = 0
            bias_list.append(bias)
        bias_array = np.array(bias_list)
        self.bias_array = bias_array

    def efficacy_generator(self):
        price_array = self.price_array
        bias_array = self.bias_array
        stop_loss_percent = 0.3
        
        long_book = [0 for i in range(price_array.size)]
        short_book = [0 for i in range(price_array.size)]
        long_pos = []
        short_pos = []
        long_positions = []
        short_positions = []
        long_cash = 0
        short_cash = 0
        stop_loss_flag = False
        short_position_flag = False
        long_position_flag = False
        sub_stop = (max(price_array) - min(price_array))*stop_loss_percent
            
        ctr = 0
        for i,j in zip(price_array, bias_array):
            if (stop_loss_flag):
                if(j == 100 or j == -100):
                    stop_loss_flag = False                 
            elif (stop_loss_flag == False  and short_position_flag == False and long_position_flag == False):
                if(j == 100):
                    long_position_flag = True
                    long_pos.append(i)
                    long_book[ctr] = i
                elif(j == -100):
                    short_position_flag = True
                    short_pos.append(i)
                    short_book[ctr] = i
            elif(stop_loss_flag == False  and short_position_flag == True):
                short_pos.append(i)
                short_book[ctr] = i
                if (i > (min(short_pos) + sub_stop)):
                    short_position_flag = False
                    stop_loss_flag = True
                    short_positions.append(short_pos)
                    short_pos = []
                elif(j == 100):
                    short_position_flag = False
                    long_position_flag = True
                    short_positions.append(short_pos)
                    short_pos = []
                elif(j == 0):
                    short_position_flag = False
                    short_positions.append(short_pos)
                    short_pos = []
            elif(stop_loss_flag == False and long_position_flag == True):
                long_pos.append(i)
                long_book[ctr] = i
                if (i < (max(long_pos) - sub_stop)):
                    long_position_flag = False
                    stop_loss_flag = True
                    long_positions.append(long_pos)
                    long_pos = []
                elif (j == 0):
                    long_position_flag = False
                    long_positions.append(long_pos)
                    long_pos = []
                elif(j == -100):
                    long_position_flag = False
                    short_position_flag = True
                    long_positions.append(long_pos)
                    long_pos = []           
            ctr += 1
                
        if (long_pos != []):
            long_positions.append(long_pos)
        if (short_pos != []):
            short_positions.append(short_pos)
            
        for i in long_positions:
            long_cash += (i[-1] - i[0])
        for i in short_positions:
            short_cash += (i[0] - i[-1])
            
        efficacy_val = (long_cash+short_cash)/sub_stop

        self.long_book = long_book
        self.short_book = short_book
        self.long_cash = long_cash
        self.short_cash = short_cash

        return efficacy_val

    def run(self):
        start = time.time()
        self.env_sma_gen()
        end = time.time()
        self.indic_runtime = end - start 

        start = time.time()
        self.current_bias()
        end = time.time()
        self.bias_runtime = end - start 

        start = time.time()
        eff_val = self.efficacy_generator()
        end = time.time()
        self.efficacy_runtime = end - start 

        self.efficacy_value = eff_val
        self.live_output = self.bias_array[-1]
        return self.bias_array[-1], eff_val
        
    def graphing(self):
        plot_width = self.plot_width
        plot_length = self.plot_length
        price_list = self.price_array
        sma_array = self.sma_arr
        up_bol = self.up_bound_array
        down_bol = self.down_bound_array
        bias_array = self.bias_array
        long_book = self.long_book
        short_book = self.short_book

        figure(figsize=(plot_width, plot_length))
        ax1 = plt.subplot()
        plt.plot(np.arange(price_list.size), price_list)

        figure(figsize=(plot_width, plot_length))
        ax2 = plt.subplot()
        plt.plot(np.arange(sma_array.size), sma_array, color = 'black')

        figure(figsize=(plot_width, plot_length))
        ax3 = plt.subplot()
        plt.plot(np.arange(up_bol.size), up_bol, color = 'black')
        plt.plot(np.arange(sma_array.size), sma_array, color = 'orange')
        plt.plot(np.arange(down_bol.size), down_bol, color = 'black')
        plt.plot(np.arange(price_list.size), price_list, color = 'blue')

        figure(figsize=(plot_width, plot_length))
        ax4 = plt.subplot()
        plt.plot(np.arange(bias_array.size), bias_array, color = 'green')

        figure(figsize=(plot_width, plot_length))
        ax5 = plt.subplot()
        plt.bar(np.arange(bias_array.size), long_book, color = 'green')
        plt.bar(np.arange(bias_array.size), short_book, color = 'red')

        plt.show()

    def diagnostics(self):
        print("\n" + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" "\n")
        print("Note: Run diagnostics only after calling self.run() function")
        print("Indicator Name: Envelope Bands for Simple Moving Average")
        print("Lookback: " + str(self.lookback))
        print("Training Period: " + str(self.price_array.size))
        print("Multiplier: " + str(self.multiplier))
        print("=========================================")
        print("Current Reading: " + str(self.live_output))
        print("Efficacy Value: " + str(self.efficacy_value) )
        print("=========================================")        
        print("Bias History: ")
        print(self.bias_array)
        print("=========================================")  
        print("Returns on the Long Side: " + str(self.long_cash))
        print("Returns on the Short Side: " + str(self.short_cash))
        print("Total Returns: " + str(self.long_cash + self.short_cash))
        print("=========================================")  
        print("Long Book:")
        print(self.long_book)
        print()
        print("Short Book:")
        print(self.short_book)
        print("=========================================")  
        print(
            "Diagnostics \n" +
            "Indicator Generations Time: " + str(self.indic_runtime) + "\n" + 
            "Bias Load Time: " + str(self.bias_runtime) + "\n" + 
            "Efficacy Value Load time: " + str(self.efficacy_runtime) + "\n"
            "Total Time: " + str(self.indic_runtime + self.bias_runtime + self.efficacy_runtime)
            )

        print("\n" + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" "\n")


extract_obj = yf.Ticker("AAPL")
data = extract_obj.history(period="1y")
data['Typical Price'] = ((data['High'] + data['Low'] + data['Close']) / 3).round(2)
data = data.iloc[-50:]
price_list = np.array(data['Typical Price'])

indic_obj = EnvelopeSMA(price_list, 5, 0.02)
x = indic_obj.run()
indic_obj.diagnostics()

