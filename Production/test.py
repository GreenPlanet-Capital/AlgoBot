import sys
from Backtesters.V1.Backtester import Backtester
import time
import sys
from SecuritySelection.Baskets import Markets

def main():
    basket = Markets.nse    
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--update':
            update_data = True
    else:
        update_data = False
    
    begin = time.time()
    backtest1 = Backtester(

        list_stock=basket,
        initial_capital=1000000, 
        base_lookback=5,
        multiplier1=1.5, 
        multiplier2=2, 
        lin_reg_filter_multiplier=0.5, 
        stop_loss_percent=0.05, 
        filter_percentile=65, 
        filter_activation_flag=True, 
        long_only_flag=True, 
        training_period=20, 
        current_account_size_csv='test_run_indian_long_only', 
        start_date="2015-01-01", 
        end_date="2021-06-01", 
        update_data=update_data, 
        percentRisk_PerTrade=0.05

        )
    backtest1.run()
    end = time.time()
    print(f'Time taken for the backtest: {end - begin}')

if __name__ == '__main__':
    main()
