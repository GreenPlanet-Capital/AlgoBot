from Engines.FilteredTrend import Engine2
import numpy as np
import pandas as pd
import math

"""
Data Format for Positions
[[TICKER, LONG/SHORT, Number_Of_Shares_Traded, Entry_Price, maximum_position_value, position_size, Days_Since_Entry]]
"""
class SwingLongShortBacktest:
    initial_capital = 100000
    current_account_size = initial_capital
    cash = initial_capital
    position_list = []
    transaction_cost_per_trade = 20
    after_trade_profits = 0
    number_of_live_positions = 0
    base_lookback = 7
    number_of_readings = 5
    pnl_list = []
    num_empty_positions = 0
    def __init__(self, input_dict, training_period, test_period, position_expiry, max_positions = 10, stop_loss_percent = 0.07):
        self.input_dict = input_dict
        self.training_period = training_period
        self.test_period = test_period
        self.position_expiry = position_expiry
        self.max_positions = max_positions
        self.stop_loss_percent = stop_loss_percent

    def clean_dictionary(self):
        input_dict = self.input_dict
        list_tickers = list(input_dict.keys())

        requirement_length = self.training_period + self.test_period
        for i in list_tickers:
            if (len(input_dict[i]) <= requirement_length):
                print(len(input_dict[i]))
                print("Deleting Ticker: " + i + " due to insufficient data")
                del self.input_dict[i]
            self.input_dict[i] = self.input_dict[i].iloc[-requirement_length:]

    def test(self):
        def initial_generate_positions(input_dictionary):
            eng_obj = Engine2(dict_of_dataframes = input_dictionary, base_lookback = self.base_lookback, number_of_readings = self.number_of_readings)
            longs, shorts = eng_obj.generate(absolute_list = False)
            print("Longs: ")
            print(longs)
            print("Shorts: ")
            print(shorts)

            account_size = self.initial_capital

            if(len(longs) <= self.number_of_readings):
                longs = longs[:self.number_of_readings]

            if(len(shorts) <= self.number_of_readings):
                shorts = shorts[:self.number_of_readings]

            self.number_of_live_positions = len(longs) + len(shorts)
            
            pcnt_allocation_longs = (len(longs)/self.number_of_live_positions)
            print(pcnt_allocation_longs)
            pcnt_allocation_shorts = (len(shorts)/self.number_of_live_positions)
            print(pcnt_allocation_shorts)

            total_long_strength = 0
            total_short_strength = 0

            for i in longs:
                total_long_strength += abs(i[1].round(1))
            
            for i in shorts:
                total_short_strength += abs(i[1].round(1))

            for i in longs:
                datapoint_df = input_dictionary[i[0]].iloc[-1]
                present_price = ((datapoint_df['HIGH'] + datapoint_df['LOW'] + datapoint_df['CLOSE'])/3).round(2)
                ticker = i[0]
                strength = i[1].round(1)
                pcnt_pos = abs(strength/total_long_strength)
                allocation = (pcnt_pos*pcnt_allocation_longs*account_size).round(1)
                num_of_shares = int((allocation/present_price).round(0))
                num_of_shares = int(num_of_shares - num_of_shares*0.1)
                self.position_list.append([ticker, "LONG", num_of_shares, present_price, present_price, present_price*num_of_shares,  1])
                self.cash -= num_of_shares*present_price
                if(self.cash < 0.05*self.initial_capital):
                    break

            for i in shorts:
                datapoint_df = input_dictionary[i[0]].iloc[-1]
                present_price = ((datapoint_df['HIGH'] + datapoint_df['LOW'] + datapoint_df['CLOSE'])/3).round(2)
                ticker = i[0]
                strength = i[1].round(1)
                pcnt_pos = abs(strength/total_short_strength)
                allocation = (pcnt_pos*pcnt_allocation_shorts*account_size).round(1)
                num_of_shares = int((allocation/present_price).round(0))
                num_of_shares = int(num_of_shares - num_of_shares*0.1)
                self.position_list.append([ticker, "SHORT", num_of_shares, present_price, present_price, present_price*num_of_shares, 1])
                self.cash -= num_of_shares*present_price
                if(self.cash < 0.05*self.initial_capital):
                    break

            self.cash -= self.transaction_cost_per_trade*self.number_of_live_positions
            self.current_account_size -= self.transaction_cost_per_trade*self.number_of_live_positions

        def portfolio_maintenance(todays_dict_dataframe):
            for i in self.position_list:
                df_input = todays_dict_dataframe[i[0]]
                df_input['Typical Price'] = ((df_input['HIGH'] + df_input['LOW'] + df_input['CLOSE']) / 3).round(2)
                price_array = np.array(df_input['Typical Price'])
                present_price = price_array[-1]

                if(i[1] == "LONG"):
                    i[4] = max(i[3],present_price)
                    self.current_account_size += (present_price - i[3])*i[2]
                elif(i[1] == "SHORT"):
                    i[4] = min(i[3],present_price)
                    self.current_account_size += (i[3] - present_price)*i[2]
                
                i[6] += 1

                trading_range = max(price_array) - min(price_array)
                ma_val = np.sum(price_array[-(self.base_lookback):])/(self.base_lookback)

                if(i[1] == "LONG"):
                    if(present_price <= ma_val):
                        stock_profit = present_price - i[3]
                        total_profit = i[2]*stock_profit
                        i[4] = present_price
                        self.after_trade_profits += total_profit
                        self.cash += present_price * i[2]
                        self.current_account_size += total_profit
                        print("Exiting Position: Due to Trend Slowing")
                        print(i[0] + "|" + i[1] + "|No. of shares: " + str(i[2]) + "|Entry Price: " + str(i[3]) + "|Exit Price: " + str(i[4]) +"|Position Size: " + str(i[5]) +  "|Days held: " + str(i[6]))
                        self.position_list.remove(i)

                    elif(present_price <= i[4] - trading_range*self.stop_loss_percent):
                        stock_profit = present_price - i[3]
                        total_profit = i[2]*stock_profit
                        i[4] = present_price
                        self.after_trade_profits += total_profit
                        self.cash += present_price * i[2]
                        self.current_account_size += total_profit
                        print("Exiting Position: Due to Stop Loss")
                        print(i[0] + "|" + i[1] + "|No. of shares: " + str(i[2]) + "|Entry Price: " + str(i[3]) + "|Exit Price: " + str(i[4]) + "|Position Size: " + str(i[5]) + "|Days held: " + str(i[6]))
                        self.position_list.remove(i)
                        
                elif(i[1] == "SHORT"):
                    if(present_price >= ma_val):
                        stock_profit = i[3] - present_price 
                        total_profit = i[2]*stock_profit
                        i[4] = present_price
                        self.after_trade_profits += total_profit
                        self.cash += present_price * i[2]
                        self.current_account_size += total_profit
                        print("Exiting Position: Due to Trend Slowing")
                        print(i[0] + "|" + i[1] + "|No. of shares: " + str(i[2]) + "|Entry Price: " + str(i[3]) + "|Exit Price: " + str(i[4]) + "|Position Size: " + str(i[5]) + "|Days held: " + str(i[6]))
                        self.position_list.remove(i)

                    elif(present_price >= i[4] + trading_range*self.stop_loss_percent):
                        stock_profit = i[3] - present_price 
                        total_profit = i[2]*stock_profit
                        i[4] = present_price
                        self.after_trade_profits += total_profit
                        self.cash += present_price * i[2]
                        self.current_account_size += total_profit
                        print("Exiting Position: Due to Stop Loss")
                        print(i[0] + "|" + i[1] + "|No. of shares: " + str(i[2]) + "|Entry Price: " + str(i[3]) + "|Exit Price: " + str(i[4]) + "|Position Size: " + str(i[5]) + "|Days held: " + str(i[6]))
                        self.position_list.remove(i)

            if(self.cash >  (self.current_account_size/self.max_positions)):
                print("Adding Position Now")
                eng_obj = Engine2(dict_of_dataframes = todays_dict_dataframe, base_lookback = self.base_lookback, number_of_readings = self.number_of_readings)
                longs, shorts = eng_obj.generate(absolute_list = False)
                potentials_list = []

                print("Longs: ")
                print(longs)
                print("Shorts: ")
                print(shorts)
                
                if(longs == []):
                    potentials_list = shorts
                elif(shorts == []):
                    potentials_list = longs
                elif(longs != [] and shorts != []):
                    for ctr in range(len(longs) + len(shorts)):
                        try: 
                            if (ctr%2 == 0 or ctr == 0):
                                potentials_list.append(longs[ctr])
                            else:
                                potentials_list.append(shorts[ctr - 1])
                        except IndexError as e:
                            break
                    
                print("Potentials List: ")
                print(potentials_list)
                for x in potentials_list:
                    ticker = x[0]
                    df_input = todays_dict_dataframe[ticker]
                    df_input['Typical Price'] = ((df_input['HIGH'] + df_input['LOW'] + df_input['CLOSE']) / 3).round(2)
                    price_array = np.array(df_input['Typical Price'])
                    present_price = price_array[-1]

                    allocation = self.initial_capital/self.max_positions
                    num_of_shares = int(((allocation/present_price).round(0)))
                    num_of_shares = int(num_of_shares - num_of_shares*0.1)

                    position_type = ""
                    if(x[1] > 0):
                        position_type = "LONG"
                    elif(x[1] <= 0):
                        position_type = "SHORT"
                    
                    self.position_list.append([ticker, position_type, num_of_shares, present_price, present_price, present_price*num_of_shares, 1])
                    self.cash -= num_of_shares*present_price

                    if(self.cash < (self.initial_capital/self.max_positions)):
                        break

                self.cash -= self.transaction_cost_per_trade * math.floor(self.cash/(self.current_account_size/self.max_positions))
                self.current_account_size -= self.transaction_cost_per_trade* math.floor(self.cash/(self.current_account_size/self.max_positions))
        
        def liquidate():
            for i in self.position_list:
                self.after_trade_profits += i[4]*i[2]
            self.after_trade_profits += self.cash

        def log_pnl():
            self.pnl_list.append(self.current_account_size)

        def logging(day_count):
            print("Day: " + str(day_count) + "\n")
            ctr = 0
            open_interest = 0
            for i in self.position_list:
                print("Ticker: " + i[0])
                print("Position Type: " + i[1])
                print("Number of shares: " + str(i[2]))
                print("Entry Price: " + str(i[3]))
                print("Max Price: " + str(i[4]))
                print("Position Size: " + str(i[5]))
                print("Days Held: " + str(i[6]))
                open_interest += i[5]
                print("++++++++++++++++++++++++++")
                ctr += 1
            print("Cash: " + str(self.cash))
            print("Account Size: " + str(self.current_account_size))
            print("PnL: " + str(self.after_trade_profits))
            print("Number of positions: " + str(ctr))
            print("Underestimated Open Interest: " + open_interest)
            print('==============================')

        def graphing():
            pass

        def dictionary_grafting(in_dict, start_val, end_val):
            list_tickers = list(in_dict.keys())
            out_dict = {}
            for i in list_tickers:
                out_dict[i] = in_dict[i].iloc[start_val: end_val]
            return out_dict

        train1_dict = dictionary_grafting(self.input_dict, 0, self.training_period)
        initial_generate_positions(train1_dict)
        logging(0)
        print(self.cash)
        for i in range(self.test_period):
            train_dict = dictionary_grafting(self.input_dict, i+1, i+self.training_period)
            portfolio_maintenance(train_dict)
            logging(i+1)

        liquidate()
        logging(self.test_period)
        print(self.cash)
        print(self.current_account_size)


            
