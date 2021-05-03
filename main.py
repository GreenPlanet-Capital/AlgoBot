from StockDataExtraction.StockData import SingleStockData
from IndicatorClasses.AccumulationDistribution import AccumulationDistribution
from IndicatorClasses.Aroon import Aroon
from IndicatorClasses.AverageTrueRange import AverageTrueRange

stock_data = SingleStockData(8,True, 200)
stock_data.generate_dataframe()

obj = AverageTrueRange(dataframe_input = stock_data.df, lookback_period = 5)
y = obj.run(9)
print(y)