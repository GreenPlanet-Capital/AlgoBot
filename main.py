from StockDataExtraction.StockData import SingleStockData
from IndicatorClasses.AccumulationDistribution import AccumulationDistribution
from IndicatorClasses.Aroon import Aroon

stock_data = SingleStockData(8,True, 100)
stock_data.generate_dataframe()

obj = Aroon(dataframe_input = stock_data.df, lookback_period = 7)
x,y = obj.run(9)
print (x)
print(y)