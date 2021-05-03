from StockDataExtraction.StockData import SingleStockData
from IndicatorClasses.AccumulationDistribution import AccumulationDistribution

stock_data = SingleStockData(8,True, 100)
stock_data.generate_dataframe()

acc_dist_obj = AccumulationDistribution(dataframe_input = stock_data.df, lookback_period = 7)
x,y = acc_dist_obj.run()
print (x)
print(y)