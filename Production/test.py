import sys
from Backtesters.V1.Livetester import Livetester
import time
import sys
from SecuritySelection.Baskets import Markets

def main():
    basket = Markets.snp    
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--update':
            update_data = True
    else:
        update_data = False
    
    with open('livetest_day.txt', 'r+') as f:
        livetest_day = int(f.readlines()[-1]) + 1
        f.write(f'{livetest_day}\n')

    print(f'Welcome to Day {livetest_day}. Happy Trading!')
    begin = time.time()
    backtest1 = Livetester(

        list_stock=basket,
        initial_capital=215705, 
        base_lookback=5,
        multiplier1=1.5, 
        multiplier2=2, 
        lin_reg_filter_multiplier=0.5, 
        stop_loss_percent=0.1, 
        filter_percentile=60, 
        filter_activation_flag=True, 
        long_only_flag=False, 
        training_period=20, 
        current_account_size_csv='livetest-account-size', 
        livetest_day=livetest_day,
        update_data=False, 
        percentRisk_PerTrade=0.25
        
        )
    backtest1.run()
    end = time.time()
    print(f'Time taken for the backtest: {end - begin}')

if __name__ == '__main__':
    main()
