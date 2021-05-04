from StockDataExtraction.StockData import SingleStockData
from IndicatorClasses.AccumulationDistribution import AccumulationDistribution
from IndicatorClasses.Aroon import Aroon
from IndicatorClasses.AverageTrueRange import AverageTrueRange
from IndicatorClasses.BalanceOfPower import BalanceOfPower
from IndicatorClasses.BollingerEMA import BollingerEMA
from IndicatorClasses.BollingerSMA import BollingerSMA
from IndicatorClasses.ChakinOscillator import ChaikinOscillator
from IndicatorClasses.ChoppinessIndex import ChoppinessIndex
from IndicatorClasses.CommodityChannelIndex import CommodityChannelIndex
from IndicatorClasses.ConnorsRSI import ConnorsRSI
from IndicatorClasses.CoppockCurve import CoppockCurve
from IndicatorClasses.CumulativeVolume import CumulativeVolume
from IndicatorClasses.DetrendedPriceOscillator import DetrendedPriceOscillator
from IndicatorClasses.DirectionalMovement import DirectionalMovement
from IndicatorClasses.DonchianChannels import DonchianChannels
from IndicatorClasses.EaseOfMovement import EaseOfMovement
from IndicatorClasses.EldersForce import EldersForce
from IndicatorClasses.EnvelopeEMA import EnvelopeEMA
from IndicatorClasses.EnvelopeSMA import EnvelopeSMA

stock_data = SingleStockData(4,True, 200)
stock_data.generate_dataframe()

obj = EnvelopeSMA(dataframe_input = stock_data.df, lookback_period = 6)
x,y = obj.run(8)
print(x)
print(y)