class Position:
    def __init__(self, *, unique_id, ticker, entry_price, number_of_shares, entry_date, position_type) -> None:
        self.unique_id = unique_id
        self.ticker = ticker
        self.prices = [entry_price]
        self.dates = [entry_date]
        self.number_of_shares = number_of_shares
        self.position_type = position_type

    def update(self, current_price, current_date):
        self.prices.append(current_price)
        self.dates.append(current_date)

    def string_position(self, pnl):
        output_string = ''
        output_string+= f'TICKER: {self.ticker}\t\t\t| UNIQUE ID: {self.unique_id}\n'
        output_string+= f'TYPE: {self.position_type}\t\t\t| SHARES: {self.number_of_shares}\n'
        output_string+= f'ENTRY DATE: {self.dates[0]}\t| CURRENT DATE: {self.dates[-1]}\n'
        output_string+= f'ENTRY PRICE: {self.prices[0]}\t\t| CURRENT PRICE: {self.prices[-1]}\n'
        output_string+= f'P&L %: {pnl}%\n'
        return output_string

    def get_current_position_status(self):
        pnl = ((self.prices[-1] - self.prices[0])/self.prices[0])*100
        return self.string_position(pnl)

    def get_current_value(self):
        if self.position_type=="LONG":
            return self.prices[-1]*self.number_of_shares
        elif self.position_type=="SHORT":
            return (2*self.prices[0] - self.prices[-1])*self.number_of_shares
        else:
            raise ValueError(f'POSITION_TYPE MUST BE LONG OR SHORT | CURRENT VALUE: {self.position_type}')

