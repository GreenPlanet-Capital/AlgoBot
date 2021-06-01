from Engines.OptimisedModel import OptimisedModel
import numpy as np
import pandas as pd
import math   
import time     

'''
data structure for portfolio maintenance: Dataframe
Columns: LONG/SHORT, Number Of Shares, Entry Price, Max/Min Price, Present Price, Entry Day

Positions Book:
Columns: Ticker, LONG/SHORT, Number Of Shares, Entry Price, Max/Min Price, Exit Price, Entry Day, Exit Days
'''

class OptimisedBackTester:
    initial_capital = 1000000
    cash = initial_capital
    day_count = 0
    #positions_book = pd.DataFrame(columns = ['Ticker','LONG/SHORT' , 'NumOfShares', 'EntryPrice', 'Max/MinPrice', 'ExitPrice', 'EntryDay', 'ExitDay'])
    portfolio = pd.DataFrame(columns = ['Ticker','LONG/SHORT' , 'NumOfShares', 'EntryPrice', 'Max/MinPrice', 'PresentPrice', 'EntryDay'])
    current_account_size = 0
    pnl_list = []
    
    def __init__(self, dict_of_dataframes, base_lookback, training_period = 30, test_period = 100, number_of_readings = 20, transaction_cost_per_trade = 20, percentRisk_PerTrade = 0.1):
        self.dict_of_dataframes = dict_of_dataframes
        self.base_lookback = base_lookback
        self.number_of_readings = number_of_readings
        self.transaction_cost_per_trade = transaction_cost_per_trade
        self.percentRisk_PerTrade = percentRisk_PerTrade
        self.training_period= training_period
        self.test_period = test_period

    def clean_dictionary(self):
        dict_of_dataframes = self.dict_of_dataframes
        list_tickers = list(dict_of_dataframes.keys())

        requirement_length = self.training_period + self.test_period
        for i in list_tickers:
            if (len(dict_of_dataframes[i]) <= requirement_length):
                print(len(dict_of_dataframes[i]))
                print("Deleting Ticker: " + i + " due to insufficient data")
                del self.dict_of_dataframes[i]
                continue
            self.dict_of_dataframes[i] = self.dict_of_dataframes[i].iloc[-requirement_length:]


    def dictionary_grafting(self, in_dict, start_val, end_val):
        day_val = self.day_count
        list_tickers = list(in_dict.keys())
        out_dict = {}
        for i in list_tickers:
            out_dict[i] = in_dict[i].iloc[start_val: end_val]
        self.day_count += 1
        return out_dict

    #columns = ['Ticker','LONG/SHORT' , 'NumOfShares', 'EntryPrice', 'Max/MinPrice', 'PresentPrice', 'EntryDay']
    def newPosition(self, dict_of_dataframes, number_of_required_positions):
        max_position_size = self.initial_capital*self.percentRisk_PerTrade
        print(max_position_size)
        obj = OptimisedModel(dict_of_dataframes = dict_of_dataframes, base_lookback = self.base_lookback, multiplier1 = 1.5, multiplier2 = 2, lin_reg_filter_multiplier = 0.5, number_of_readings = self.number_of_readings, filter_percentile = 70, filter_activation_flag = True, long_only_flag = False)
        position_list = obj.run()

        for i in range(number_of_required_positions):
            ticker,strength_val = position_list[i]
            temp_df = dict_of_dataframes[ticker] 
            try: 
                temp_df['Typical Price'] = (temp_df['HIGH'] + temp_df['LOW'] + temp_df['CLOSE'])/3
                price_list = list(temp_df['Typical Price'])
                present_price = price_list[-1]
                present_price = round((present_price), 3)
            except ValueError:
                continue

            try:
                num_of_shares = math.floor(max_position_size/present_price)
            except ValueError:
                number_of_required_positions += 1
                continue

            position_type = ""
            if(strength_val > 0):
                position_type = "LONG"
            elif(strength_val < 0):
                position_type = "SHORT"

            unique_id = str(ticker) + str(self.day_count)

            self.cash -= self.transaction_cost_per_trade
            self.cash -= num_of_shares*present_price
            self.portfolio.loc[unique_id] = [ticker, position_type, num_of_shares, present_price, present_price, present_price, self.day_count]
            #DATAFRAME NOT UPDATING IN THE LINE ABOVE

    #columns = ['Ticker','LONG/SHORT' , 'NumOfShares', 'EntryPrice', 'Max/MinPrice', 'PresentPrice', 'EntryDay']
    def portfolio_update(self, dict_of_dataframes):
        max_position_size = self.initial_capital*self.percentRisk_PerTrade
        self.current_account_size = 0

        def exit_position(unique_id):
            if(self.portfolio.loc[unique_id,'LONG/SHORT'] == "LONG"):
                self.cash += self.portfolio.loc[unique_id,'NumOfShares']*self.portfolio.loc[unique_id,'PresentPrice']
            elif(self.portfolio.loc[unique_id,'LONG/SHORT'] == "SHORT"):
                self.cash += self.portfolio.loc[unique_id,'NumOfShares']*(2*(self.portfolio.loc[unique_id,'EntryPrice']) - self.portfolio.loc[unique_id,'PresentPrice'])
            number_of_days = self.day_count - self.portfolio.loc[unique_id,'EntryDay']
            self.cash -= self.transaction_cost_per_trade
            print("Ticker: " + str(unique_id) + "|Type: " + self.portfolio.loc[unique_id,'LONG/SHORT'] + "|Entry: " + str(self.portfolio.loc[unique_id,'EntryPrice']) + "|Exit: " + str(self.portfolio.loc[unique_id,'PresentPrice']) + "|Days Held: " + str(number_of_days))
            self.portfolio.drop(unique_id,  inplace=True)

        uid_list = list(self.portfolio.index.values)
        for i in uid_list:
            uid = i

            try: 
                ticker = self.portfolio.loc[uid, 'Ticker']
                temp_df = dict_of_dataframes[ticker]
                temp_df['Typical Price'] = (temp_df['HIGH'] + temp_df['LOW'] + temp_df['CLOSE'])/3
                price_list = list(temp_df['Typical Price'])
            except ValueError:
                continue

            present_price = price_list[-1]
            present_price = round((present_price), 3)
            #Present Price Update
            self.portfolio.loc[uid,'PresentPrice'] = present_price

            #Max/Min Price Update
            if (self.portfolio.loc[uid,'LONG/SHORT'] == 'LONG'):
                self.portfolio.loc[uid,'Max/MinPrice'] = max(present_price,  self.portfolio.loc[uid,'EntryPrice'])
                self.current_account_size += self.portfolio.loc[uid,'NumOfShares']*self.portfolio.loc[uid,'PresentPrice']
            elif (self.portfolio.loc[uid,'LONG/SHORT'] == 'SHORT'):
                self.portfolio.loc[uid,'Max/MinPrice'] = min(present_price,  self.portfolio.loc[uid,'EntryPrice'])
                self.current_account_size += self.portfolio.loc[uid,'NumOfShares']*(2*(self.portfolio.loc[uid,'EntryPrice']) - self.portfolio.loc[uid,'PresentPrice'])

            #Checking for Long Exits
            if(self.portfolio.loc[uid,'LONG/SHORT'] == 'LONG'):
                envma_val = sum(price_list[(-self.base_lookback):])/(self.base_lookback)
                #envma_val = (envma_val + envma_val*0.1)

                trading_range = max(price_list) - min(price_list)
                stop_loss_trigger = max((self.portfolio.loc[uid,'Max/MinPrice'] - trading_range*0.2), (0.96*self.portfolio.loc[uid,'Max/MinPrice']))

                if(present_price < envma_val):
                    #Closing Position for Trend Slowing
                    print("Closing Position for Trend Slowing")
                    exit_position(uid)

                elif(present_price < stop_loss_trigger):
                    #Closing Position for stop loss trigger
                    print("Closing Position for Stop Loss")
                    exit_position(uid)

            #Checking for Short Exits
            elif(self.portfolio.loc[uid,'LONG/SHORT'] == 'SHORT'):
                envma_val = sum(price_list[-self.base_lookback:])/self.base_lookback
                #envma_val = (envma_val - envma_val*0.1)

                trading_range = max(price_list) - min(price_list)
                stop_loss_trigger = min((self.portfolio.loc[uid,'Max/MinPrice'] + trading_range*0.2), (1.04*self.portfolio.loc[uid,'Max/MinPrice']))

                if(present_price > envma_val):
                    #Closing Position for Trend Slowing
                    print("Closing Position for Trend Slowing")
                    exit_position(uid)

                elif(present_price > stop_loss_trigger):
                    #Closing Position for stop loss trigger
                    print("Closing Position for Stop Loss")
                    exit_position(uid)

        if (self.cash > max_position_size):
            # SOME ERROR IN THE LINE BELOW
            number_of_required_positions = math.floor((self.cash/max_position_size))
            print("NUMER OF NEW POSITIONS: " + str(number_of_required_positions))
            self.newPosition(dict_of_dataframes = dict_of_dataframes, number_of_required_positions = number_of_required_positions)

        self.current_account_size += self.cash 
        self.pnl_list.append(self.current_account_size)

    def logging(self):
        print("=============================================")
        print("-------")
        print("DAY: " + str(self.day_count))
        print("-------")
        print(self.portfolio)
        print("-------")
        print("Portfolio Value: " + str(self.current_account_size))
        print("Cash: " + str(self.cash))

    def test(self):
        self.clean_dictionary()

        start_val = 0
        end_val = self.training_period

        initial_position_size = self.initial_capital*self.percentRisk_PerTrade
        initial_num_of_pos = math.floor(self.initial_capital/initial_position_size)

        out_dict = self.dictionary_grafting(self.dict_of_dataframes, start_val, end_val)
        self.newPosition(out_dict,initial_num_of_pos)
        self.logging()

        for i in range(self.test_period - 1):
            start_val += 1
            end_val += 1
            out_dict = self.dictionary_grafting(self.dict_of_dataframes, start_val, end_val)
            self.portfolio_update(out_dict)
            self.logging()





        




