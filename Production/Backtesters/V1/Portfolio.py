from Backtesters.V1.Position import Position
import csv
class Portfolio:

    def __init__(self, *, initial_capital, base_lookback) -> None:
        self.wallet = initial_capital
        self.base_lookback = base_lookback
        self.positions = {}
        self.exits = []

    def enter(self, *, unique_id, position: Position):
        self.positions[unique_id] = position
        self.wallet -= position.number_of_shares * position.prices[0]

    def exit(self, *, unique_id):
        position = self.positions[unique_id]
        if position.position_type=="LONG":
            self.wallet += position.number_of_shares * position.prices[-1]
        elif position.position_type=="SHORT":
            self.wallet += position.number_of_shares * (2*position.prices[0] - position.prices[-1])
        self.exits.append(unique_id)

    def update_portfolio(self, *, NewStockDataDict: dict, stop_loss_percent, current_date, current_account_size_csv):
        for unique_id, position in self.positions.items():
            do_we_abort = False
            if unique_id in self.exits:
                continue
            ticker = position.ticker
            ma_list = list(NewStockDataDict[ticker]['TYPICAL PRICE'])
            current_price = ma_list[-1]
            position.update(current_price=current_price, current_date=current_date)
            moving_average_value = sum(ma_list[-self.base_lookback:])/self.base_lookback

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
                stop_loss_trigger = max_val - (stop_loss_percent * trading_range)
                if current_price<stop_loss_trigger:
                    do_we_abort = True
            elif position.position_type == "SHORT":
                stop_loss_trigger = min_val + (stop_loss_percent * trading_range)
                if current_price>stop_loss_trigger:
                    do_we_abort = True

            if do_we_abort:
                self.exit(unique_id=unique_id)

        self.update_register(current_date=current_date,
                             current_account_size_csv=current_account_size_csv)
        
    def get_current_account_size(self):
        current_account_size = 0
        for unique_id, position in self.positions.items():
            if unique_id in self.exits:
                continue
            current_account_size += position.get_current_value()
        return current_account_size + self.wallet

    def update_register(self, *, current_date, current_account_size_csv):
        new_entry = ""
        new_entry += f'Positions on {current_date}\n\n'
        current_account_size = self.get_current_account_size()
        new_entry += f'Current Account Size: {current_account_size}\n'
        new_entry += f'Wallet: {self.wallet}\n\n'

        with open(f'{current_account_size_csv}.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([current_date, current_account_size])

        for unique_id, position_obj in self.positions.items():
            if unique_id in self.exits:
                continue
            new_entry += position_obj.get_current_position_status()
            new_entry += '\n\n'

        current_exits = []
        new_entry += "EXITS:\n"
        for unique_id in self.exits:
            new_entry += self.positions[unique_id].get_current_position_status()
            current_exits.append(unique_id)
            new_entry += '\n\n'

        for unique_id in current_exits:
            self.exits.remove(unique_id)
            del self.positions[unique_id]

        with open('livetest_results.txt', 'a') as f:
            f.write(new_entry)
