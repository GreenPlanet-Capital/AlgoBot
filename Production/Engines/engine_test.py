"""

Input: 
    dict_of_dataframes:
    base_lookback:
    width:
    reading_lookback:
    number_of_readings:

Output:
    dict

"""
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
from IndicatorClasses.ExponentialMovingAverage import ExponentialMovingAverage
from IndicatorClasses.SimpleMovingAverage import SimpleMovingAverage
from IndicatorClasses.FisherTransform import FisherTransform
from IndicatorClasses.FisherTransformReversal import FisherTransformReversal
from IndicatorClasses.McGinleyDynamic import McGinleyDynamic
from IndicatorClasses.HistoricalVolatility import HistoricalVolatility
from IndicatorClasses.KeltnerChannel import KeltnerChannel
from IndicatorClasses.LinearRegression import LinearRegression
from IndicatorClasses.LocalVolatility import LocalVolatility
from IndicatorClasses.MassIndex import MassIndex
from IndicatorClasses.MomentumOscillator import MomentumOscillator
from IndicatorClasses.MomentumOscillatorReversal import MomentumOscillatorReversal
from IndicatorClasses.MoneyFlowReversal import MoneyFlowReversal
from IndicatorClasses.MovingAverageConvergenceDivergence import MovingAverageConvergenceDivergence
from IndicatorClasses.OnBalanceVolume import OnBalanceVolume
from IndicatorClasses.PivotPoint import PivotPoint
from IndicatorClasses.PriceVolumeTrend import PriceVolumeTrend
from IndicatorClasses.PriceVolumeTrendReversal import PriceVolumeTrendReversal
from IndicatorClasses.RateOfChange import RateOfChange
from IndicatorClasses.RelativeStrengthIndex import RelativeStrengthIndex
from IndicatorClasses.SimpleMovingAverageOscillator import SimpleMovingAverageOscillator
from IndicatorClasses.SMIErgodic import SMIErgodic
from IndicatorClasses.StochasticOscillator import StochasticOscillator
from IndicatorClasses.WeightedMovingAverage import WeightedMovingAverage
from IndicatorClasses.StochasticOscillatorReversal import StochasticOscillatorReversal
from IndicatorClasses.TRIX import TRIX
from IndicatorClasses.TrueStrengthIndicator import TrueStrengthIndicator
from IndicatorClasses.Volume import Volume
from IndicatorClasses.VolumeOscillator import VolumeOscillator
from IndicatorClasses.VortexOscillator import VortexOscillator
from IndicatorClasses.WilliamsPercentR import WilliamsPercentR
from IndicatorClasses.TradingRange import TradingRange

class Engine1:
    def __init__(self, dict_of_dataframes, base_lookback, width, reading_lookback, number_of_readings):
        self.dict_of_dataframe = dict_of_dataframe
        self.base_lookback = base_lookback
        self.reading_lookback = reading_lookback
        self.number_of_readings = number_of_readings
        self.width = width

    def lookback_lexicon(self, base_lookback = self.base_lookback, width = self.width):
        """
        #Generator
        :params: base_lookback: the input that is passed through as lookback into each indicator
                width: the number added to the base lookback in order to determine the number of lookbacks above the base lookback that needs to be tested
        :returns: a list of lookbacks
        """
        # Generate the array of lookback Periods that we use based on the base lookback
        for i in range(width):
            yield (base_lookback + i + 1)


    def generate_weightedList(self, input_list):
        """
        :params: input_list: take the live signal list
        :returns: weighted sum
        """
        # Take a list of generated signums and make a weighted output based on most recent reading
        out_list = []

        denom = len(input_list)
        denom = denom*(denom+1)/2
        for count,val in enumerate(input_list):
            num = (count + 1)
            frac = num/denom
            append_val = frac*val
            out_list.append(append_val)
        weighted_sum = sum(out_list)
        return weighted_sum

    def weight_adjust(self, input_weight):
        """
        :params: input_weight: takes in the weight returned by the code and returns 0.01 if it is lower than that value
        :return: either 0.01 or input_weight
        """
        if (input_weight <= 0.01):
            return 0.01
        else:
            return input_weight



    def long_short_singlelexicon(self, df_input, lookback):
        """
        :params: dataframe with 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', lookback
        :returns: long/short weighted strength 
        """
        # Take a dataframe,single lookback period, and  and return the long short strength

        reading_lookback = self.reading_lookback

        acc_dist = AccumulationDistribution(dataframe_input = df_input, lookback_period = lookback)
        acc_dist_weight, acc_dist_liveSignal_list = acc_dist.run(reading_lookback)
        acc_dist_weightedSignal = generate_weightedList(acc_dist_liveSignal_list)
        acc_dist_weight = weight_adjust(acc_dist_weight)

        aroon = Aroon(dataframe_input = df_input, lookback_period = lookback)
        aroon_weight, aroon_liveSignal_list = aroon.run(reading_lookback)
        aroon_weightedSignal = generate_weightedList(aroon_liveSignal_list)
        aroon_weight = weight_adjust(aroon_weight)

        bop = BalanceOfPower(dataframe_input = df_input)
        bop_weight, bop_liveSignal_list = bop.run(reading_lookback)
        bop_weightedSignal = generate_weightedList(bop_liveSignal_list)
        bop_weight = weight_adjust(bop_weight)

        bol_ema = BollingerEMA(dataframe_input = df_input, lookback_period = lookback)
        bol_ema_weight, bol_ema_liveSignal_list = bol_ema.run(reading_lookback)
        bol_ema_weightedSignal = generate_weightedList(bol_ema_liveSignal_list)
        bol_ema_weight = weight_adjust(bol_ema_weight)

        bol_sma = BollingerSMA(dataframe_input, lookback_period)(dataframe_input = df_input, lookback_period = lookback)
        bol_sma_weight, bol_sma_liveSignal_list = bol_sma.run(reading_lookback)
        bol_sma_weightedSignal = generate_weightedList(bol_sma_liveSignal_list)
        bol_sma_weight = weight_adjust(bol_sma_weight)

        chaik_osc = ChaikinOscillator(dataframe_input = df_input, lookback_period = lookback)
        chaik_osc_weight, chaik_osc_liveSignal_list = chaik_osc.run(reading_lookback)
        chaik_osc_weightedSignal = generate_weightedList(chaik_osc_liveSignal_list)
        chaik_osc_weight = weight_adjust(chaik_osc_weight)

        cci = CommodityChannelIndex(dataframe_input = df_input, lookback_period = lookback)
        cci_weight, cci_liveSignal_list = cci.run(reading_lookback)
        cci_weightedSignal = generate_weightedList(cci_liveSignal_list)
        cci_weight = weight_adjust(cci_weight)

        con_rsi = ConnorsRSI(dataframe_input = df_input, lookback_period = lookback)
        con_rsi_weight, con_rsi_liveSignal_list = con_rsi.run(reading_lookback)
        con_rsi_weightedSignal = generate_weightedList(con_rsi_liveSignal_list)
        con_rsi_weight = weight_adjust(con_rsi_weight)

        acc_dist = AccumulationDistribution(dataframe_input = df_input, lookback_period = lookback)
        acc_dist_weight, acc_dist_liveSignal_list = acc_dist.run(reading_lookback)
        acc_dist_weightedSignal = generate_weightedList(acc_dist_liveSignal_list)
        acc_dist_weight = weight_adjust(acc_dist_weight)

        acc_dist = AccumulationDistribution(dataframe_input = df_input, lookback_period = lookback)
        acc_dist_weight, acc_dist_liveSignal_list = acc_dist.run(reading_lookback)
        acc_dist_weightedSignal = generate_weightedList(acc_dist_liveSignal_list)
        acc_dist_weight = weight_adjust(acc_dist_weight)

        

    def generate_longShortStrength():
    """
    :params: 
    :returns:
    """
        self.lookback_lexicon()
        self.long_short_singlelexicon()
    # take the generator of the lookback_lexicon and run it through the long 
    
    def generate_listOfTickers():
    """
    :params: 
    :returns:
    """
    # Generate the list of tickers by extracting from the dictionary that is passed into the function
     
    def generate(self):
    self.number_of_readings = 
    """
    :params: 
    :returns:
    """
    # Generate the dictionary based on order of precendence
    
     
