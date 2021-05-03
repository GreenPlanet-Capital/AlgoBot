from StockDataExtraction.StockData import SingleStockData
from IndicatorClasses.AccumulationDistribution import AccumulationDistribution
from IndicatorClasses.Aroon import Aroon
from IndicatorClasses.AverageTrueRange import AverageTrueRange
from IndicatorClasses.BalanceOfPower import BalanceOfPower
from IndicatorClasses.BollingerEMA import BollingerEMA
from IndicatorClasses.BollingerSMA import BollingerSMA
from IndicatorClasses.ChakinOscillator import ChaikinOscillator

stock_data = SingleStockData(4,True, 200)
stock_data.generate_dataframe()

obj = ChaikinOscillator(dataframe_input = stock_data.df, lookback_period = 6)
x,y = obj.run(100)
print(x)
print(y)