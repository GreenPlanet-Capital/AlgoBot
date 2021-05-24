import numpy as np
import math
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import yfinance as yf

class WMA_WMA_Osc:
    plot_width = 5
    plot_length = 3
    indic_runtime = 0
    signal_runtime = 0
    signum_runtime = 0
    bias_runtime = 0
    efficacy_runtime = 0
    live_output = 0
    efficacy_value = 0

    def __init__(self, price_array, short_lookback, long_lookback):
        self.price_array = price_array
        self.short_lookback = short_lookback 
        self.long_lookback = long_lookback
        self.osc_array = np.array([])
        self.signal_array = np.array([])
        self.signum_array = np.array([])
        self.bias_array = np.array([])
        self.long_book = np.array([])
        self.short_book = np.array([])
        self.long_cash = 0
        self.short_cash = 0

    def wma_wma_osc_gen(self):
        price_array = self.price_array
        short_lookback = self.short_lookback
        long_lookback = self.long_lookback

        out_array = np.array([None for i in range(long_lookback)])
        def wma(price_array, lookback):
            out_array = np.array([None for i in range(lookback)])
            for i in range(price_array.size - lookback):
                in_array = (price_array[i:i+lookback])
                sum_val = 0
                for j in range(lookback):
                    sum_val += in_array[j]*(j+1)
                out_val = sum_val*2/(lookback*(lookback+1))
                out_array = np.append(out_array,out_val)
            return out_array
        out_arr = np.subtract(wma(price_array, short_lookback)[long_lookback:], wma(price_array, long_lookback)[long_lookback:])
        out_array = np.append(out_array,out_arr)
        
        self.osc_array = out_array

    def signal_generation(self):
        oscillator_array = self.osc_array
        long_lookback = self.long_lookback

        out_array = np.array([0 for i in range(long_lookback + 1)])
        start_val = long_lookback + 1
        for i in range(start_val, oscillator_array.size):
            append_val = 0
            if (oscillator_array[i] > 0 and oscillator_array[i - 1]  <= 0):
                append_val = oscillator_array[i] - oscillator_array[i - 1]
            elif (oscillator_array[i] < 0 and oscillator_array[i - 1]  >= 0):
                append_val = oscillator_array[i] - oscillator_array[i - 1]
            out_array = np.append(out_array, append_val)
        
        self.signal_array = out_array
    
    def signum_generation(self):
        signal_array = self.signal_array
        sensitivity = 1.5
        out_arr = np.empty(0)
        std = np.std(signal_array)
        for i in signal_array:
            append_val = 0
            if (i > std*sensitivity):
                append_val = 100
            elif (i < -std*sensitivity):
                append_val = -100
            out_arr = np.append(out_arr, append_val)
        
        self.signum_array = out_arr

    def current_bias(self):
        signal_array = self.signal_array
        signum_array = self.signum_array
        bias = 0
        bias_list = []
        for i,j in zip(signal_array,signum_array):
            if (bias == 0):
                if (j == 100):
                    bias = 100
                elif(j == -100):
                    bias = -100
            elif(bias == -100):
                if (j == 100 and i > 0):
                    bias = 100
                elif(j != 100 and i > 0):
                    bias = 0
            elif(bias == 100):
                if (j == -100 and i < 0):
                    bias = -100
                elif (j != -100 and i < 0):
                    bias = 0
            bias_list.append(bias)
        bias_array = np.array(bias_list)

        self.bias_array = bias_array

    def efficacy_generator (self):
        price_array = self.price_array
        signum_array = self.signum_array
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
        for i,j,k in zip(price_array, bias_array,signum_array):
            if (stop_loss_flag):
                if(k == 100 or k == -100):
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
        self.wma_wma_osc_gen()
        end = time.time()
        self.indic_runtime = end - start 

        start = time.time()
        self.signal_generation()
        end = time.time()
        self.signal_runtime = end - start

        start = time.time()
        self.signum_generation()
        end = time.time()
        self.signum_runtime = end - start

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
        osc_array = self.osc_array 
        sign_gen = self.signal_array
        signum_gen = self.signum_array
        bias_array = self.bias_array
        long_book = self.long_book
        short_book = self.short_book

        figure(figsize=(plot_width, plot_length))
        ax1 = plt.subplot()
        plt.plot(np.arange(price_list.size), price_list)

        figure(figsize=(plot_width, plot_length))
        ax2 = plt.subplot()
        plt.plot(np.arange(osc_array .size), osc_array, color = 'darkgreen')

        figure(figsize=(plot_width, plot_length))
        ax3 = plt.subplot()
        plt.plot(np.arange(sign_gen.size), sign_gen, color = 'orange')

        figure(figsize=(plot_width, plot_length))
        ax4 = plt.subplot()
        plt.plot(np.arange(signum_gen.size), signum_gen, color = 'orange')

        figure(figsize=(plot_width, plot_length))
        ax5 = plt.subplot()
        plt.plot(np.arange(bias_array.size), bias_array, color = 'green')

        figure(figsize=(plot_width, plot_length))
        ax6 = plt.subplot()
        plt.bar(np.arange(bias_array.size), long_book , color = 'green')
        plt.bar(np.arange(bias_array.size), short_book , color = 'red')

        plt.show()

    def diagnostics(self):
        print("\n" + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" "\n")
        print("Note: Run diagnostics only after calling self.run() function")
        print("Indicator Name: Weighted Moving Average Oscillator")
        print("Short Lookback: " + str(self.short_lookback))
        print("Long Lookback: " + str(self.long_lookback))
        print("Training Period: " + str(self.price_array.size))
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
            "Signal Generations Time: " + str(self.signal_runtime) + "\n" + 
            "Signum Generations Time: " + str(self.signum_runtime) + "\n" + 
            "Bias Load Time: " + str(self.bias_runtime) + "\n" + 
            "Efficacy Value Load time: " + str(self.efficacy_runtime) + "\n"
            "Total Time: " + str(self.indic_runtime + self.signal_runtime + self.signum_runtime + self.bias_runtime + self.efficacy_runtime)
            )

        print("\n" + "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" "\n")

def main():
    extract_obj = yf.Ticker("AAPL")
    data = extract_obj.history(period="1y")
    data['Typical Price'] = ((data['High'] + data['Low'] + data['Close']) / 3).round(2)
    data = data.iloc[-50:]
    price_list = np.array(data['Typical Price'])

    indic_obj = WMA_WMA_Osc(price_list, 5, 8)
    x = indic_obj.run()
    indic_obj.diagnostics()

if __name__ == '__main__':
    main()

