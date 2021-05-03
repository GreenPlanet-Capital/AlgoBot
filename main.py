from StockDataExtraction.StockData import SingleStockData
from IndicatorClasses.AccumulationDistribution import AccumulationDistribution
from IndicatorClasses.Aroon import Aroon
from IndicatorClasses.AverageTrueRange import AverageTrueRange
from IndicatorClasses.BalanceOfPower import BalanceOfPower

stock_data = SingleStockData(8,True, 200)
stock_data.generate_dataframe()

obj = BalanceOfPower(dataframe_input = stock_data.df)
x,y = obj.run(9)
print(x)
print(y)