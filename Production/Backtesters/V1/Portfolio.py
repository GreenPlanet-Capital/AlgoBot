from Production.Backtesters.V1.Position import Position
class Portfolio:

    def __init__(self,*,initial_capital) -> None:
        self.wallet = initial_capital
        self.positions = {str: Position}
        self.exits = []

    def enter(self, *, unique_id, position: Position):
        self.positions[unique_id] = position
        self.wallet -= position.number_of_shares * position.prices[0]

    def exit(self, *, unique_id):
        position = self.positions[unique_id]
        if position.position_type=="LONG":
            self.wallet += position.number_of_shares * position.prices[-1]
        elif position.position_type=="SHORT":
            self.wallet += position.number_of_shares * (position.prices[0] - position.prices[-1])
        self.exits.append(unique_id)

    def update_portfolio(self, *, NewStockDataDict: dict, current_date):
        for unique_id, position in self.positions.items():
            do_we_abort = False
            if unique_id in self.exits:
                continue
            ticker = position.ticker
            ma_list = list(NewStockDataDict[ticker]['TYPICAL PRICE'])
            current_price = ma_list[-1]
            position.update(current_price=current_price, current_date=current_date)
            moving_average_value = ma_list[-self.base_lookback]/self.base_lookback

            # Moving Average Triggers
            if position.position_type == "LONG":
                if current_price<moving_average_value:
                    do_we_abort = True
            elif position.position_type == "SHORT":
                if current_price>moving_average_value:
                    do_we_abort = True

            # Stoploss Triggers
            max_val = max(list(NewStockDataDict[ticker]['TYPICAL PRICE']))
            min_val = min(list(NewStockDataDict[ticker]['TYPICAL PRICE']))
            trading_range = max_val - min_val
            
            if position.position_type == "LONG":
                stop_loss_trigger = max_val - (0.1 * trading_range)
                if current_price<stop_loss_trigger:
                    do_we_abort = True
            elif position.position_type == "SHORT":
                stop_loss_trigger = min_val + (0.1 * trading_range)
                if current_price>stop_loss_trigger:
                    do_we_abort = True

            if do_we_abort:
                self.exit(unique_id=unique_id)
        
        self.update_register(current_date)

    def get_current_account_size(self):
        current_account_size = 0
        for unique_id, position in self.positions.items():
            if unique_id in self.exits:
                continue
            current_account_size += position.get_current_value()
        return current_account_size + self.wallet

    def update_register(self, current_date):
        new_entry = ""
        new_entry += f'Positions on {current_date}\n\n'
        new_entry += f'Current Account Size: {self.get_currentAccountSize}\n'
        new_entry += f'Wallet: {self.wallet}\n\n'

        for unique_id, position_obj in self.positions.items():
            if unique_id in self.exits:
                continue
            new_entry += position_obj.get_current_position_status()
            new_entry += '\n\n'

        new_entry += "EXITS:\n"
        for unique_id in self.e= self.dictionary_grafting()xits:
            new_entry += self.positions[unique_id].get_current_position_status()
            new_entry += '\n\n'

        with open('backtest_results.txt', 'a') as f:
            f.write(new_entry)
