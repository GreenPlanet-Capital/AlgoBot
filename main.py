from StockDataExtraction.StockData import SingleStockData
from IndicatorClasses.AccumulationDistribution import AccumulationDistribution
from IndicatorClasses.Aroon import Aroon
from IndicatorClasses.AverageTrueRange import AverageTrueRange
from IndicatorClasses.BalanceOfPower import BalanceOfPower
from IndicatorClasses.BollingerEMA import BollingerEMA

stock_data = SingleStockData(8,True, 150)
stock_data.generate_dataframe()

obj = BollingerEMA(dataframe_input = stock_data.df, lookback_period = 6)
x,y = obj.run(4)
print(x)
print(y)