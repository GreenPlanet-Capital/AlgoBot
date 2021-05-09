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

        cop_cur = CoppockCurve(dataframe_input = df_input, lookback_period = lookback)
        cop_cur_weight, cop_cur_liveSignal_list = cop_cur.run(reading_lookback)
        cop_cur_weightedSignal = generate_weightedList(cop_cur_liveSignal_list)
        cop_cur_weight = weight_adjust(cop_cur_weight)

        dir_mov = DirectionalMovement(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2 = lookback + 3)
        dir_mov_weight, _liveSignal_list = dir_mov.run(reading_lookback)
        dir_mov_weightedSignal = generate_weightedList(dir_mov_liveSignal_list)
        dir_mov_weight = weight_adjust(dir_mov_weight)

        donch = DonchianChannels(dataframe_input = df_input, lookback_period = lookback)
        donch_weight, donch_liveSignal_list = donch.run(reading_lookback)
        donch_weightedSignal = generate_weightedList(donch_liveSignal_list)
        donch_weight = weight_adjust(donch_weight)

        el_force = EldersForce(dataframe_input = df_input, lookback_period = lookback)
        el_force_weight, el_force_liveSignal_list = el_force.run(reading_lookback)
        el_force_weightedSignal = generate_weightedList(el_force_liveSignal_list)
        el_force_weight = weight_adjust(el_force_weight)

        env_ema = EnvelopeEMA(dataframe_input = df_input, lookback_period = lookback)
        env_ema_weight, _liveSignal_list = env_ema.run(reading_lookback)
        env_ema_weightedSignal = generate_weightedList(env_ema_liveSignal_list)
        env_ema_weight = weight_adjust(env_ema_weight)

        env_sma = EnvelopeSMA(dataframe_input = df_input, lookback_period = lookback)
        env_sma_weight, env_sma_liveSignal_list = env_sma.run(reading_lookback)
        env_sma_weightedSignal = generate_weightedList(env_sma_liveSignal_list)
        env_sma_weight = weight_adjust(env_sma_weight)

        ema = ExponentialMovingAverage(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2 = lookback + 3)
        ema_weight, ema_liveSignal_list = ema.run(reading_lookback)
        ema_weightedSignal = generate_weightedList(ema_liveSignal_list)
        ema_weight = weight_adjust(ema_weight)

        sma = SimpleMovingAverage(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2 = lookback + 3)
        sma_weight, sma_liveSignal_list = sma.run(reading_lookback)
        sma_weightedSignal = generate_weightedList(sma_liveSignal_list)
        sma_weight = weight_adjust(sma_weight)

        fish_transform = FisherTransform(dataframe_input = df_input, lookback_period = lookback)
        fish_transform_weight, fish_transform_liveSignal_list = fish_transform.run(reading_lookback)
        fish_transform_weightedSignal = generate_weightedList(fish_transform_liveSignal_list)
        fish_transform_weight = weight_adjust(fish_transform_weight)

        fish_trans_rev = FisherTransformReversal(dataframe_input = df_input, lookback_period = lookback)
        fish_trans_rev_weight, fish_trans_rev_liveSignal_list = fish_trans_rev.run(reading_lookback)
        fish_trans_rev_weightedSignal = generate_weightedList(fish_trans_rev_liveSignal_list)
        fish_trans_rev_weight = weight_adjust(fish_trans_rev_weight)

        mcg_dyn = McGinleyDynamic(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2 = lookback + 3)
        mcg_dyn_weight, mcg_dyn_liveSignal_list = mcg_dyn.run(reading_lookback)
        mcg_dyn_weightedSignal = generate_weightedList(mcg_dyn_liveSignal_list)
        mcg_dyn_weight = weight_adjust(mcg_dyn_weight)

        kelt_chnl = KeltnerChannel(dataframe_input = df_input, lookback_period = lookback)
        kelt_chnl_weight, kelt_chnl_liveSignal_list = kelt_chnl.run(reading_lookback)
        kelt_chnl_weightedSignal = generate_weightedList(kelt_chnl_liveSignal_list)
        kelt_chnl_weight = weight_adjust(kelt_chnl_weight)

        lin_reg = LinearRegression(dataframe_input = df_input, lookback_period = lookback)
        lin_reg_weight, lin_reg_liveSignal_list = lin_reg.run(reading_lookback)
        lin_reg_weightedSignal = generate_weightedList(lin_reg_liveSignal_list)
        lin_reg_weight = weight_adjust(lin_reg_weight)

        mass = MassIndex(dataframe_input = df_input, lookback_period = lookback)
        mass_weight, mass_liveSignal_list = mass.run(reading_lookback)
        mass_weightedSignal = generate_weightedList(mass_liveSignal_list)
        mass_weight = weight_adjust(mass_weight)

        mom_osc = MomentumOscillator(dataframe_input = df_input, lookback_period = lookback)
        mom_osc_weight, mom_osc_liveSignal_list = mom_osc.run(reading_lookback)
        mom_osc_weightedSignal = generate_weightedList(mom_osc_liveSignal_list)
        mom_osc_weight = weight_adjust(mom_osc_weight)

        mom_osc_rev = MomentumOscillatorReversal(dataframe_input = df_input, lookback_period = lookback)
        mom_osc_rev_weight, mom_osc_rev_liveSignal_list = mom_osc_rev.run(reading_lookback)
        mom_osc_rev_weightedSignal = generate_weightedList(mom_osc_rev_liveSignal_list)
        mom_osc_rev_weight = weight_adjust(mom_osc_rev_weight)

        mon_flo = MoneyFlowReversal(dataframe_input = df_input, lookback_period = lookback)
        mon_flo_weight, mon_flo_liveSignal_list = mon_flo.run(reading_lookback)
        mon_flo_weightedSignal = generate_weightedList(mon_flo_liveSignal_list)
        mon_flo_weight = weight_adjust(mon_flo_weight)

        macd = MovingAverageConvergenceDivergence(dataframe_input = df_input, lookback_period = lookback)
        macd_weight, macd_liveSignal_list = macd.run(reading_lookback)
        macd_weightedSignal = generate_weightedList(macd_liveSignal_list)
        macd_weight = weight_adjust(macd_weight)

        obv = OnBalanceVolume(dataframe_input = df_input, lookback_period = lookback)
        obv_weight, obv_liveSignal_list = obv.run(reading_lookback)
        obv_weightedSignal = generate_weightedList(obv_liveSignal_list)
        obv_weight = weight_adjust(_weight)

        pvt_pnt = PivotPoint(dataframe_input = df_input, lookback_period = lookback)
        pvt_pnt_weight, pvt_pnt_liveSignal_list = pvt_pnt.run(reading_lookback)
        pvt_pnt_weightedSignal = generate_weightedList(pvt_pnt_liveSignal_list)
        pvt_pnt_weight = weight_adjust(pvt_pnt_weight)

        pvt = PriceVolumeTrend(dataframe_input = df_input, lookback_period = lookback)
        pvt_weight, pvt_liveSignal_list = pvt.run(reading_lookback)
        pvt_weightedSignal = generate_weightedList(pvt_liveSignal_list)
        pvt_weight = weight_adjust(pvt_weight)

        pvt_rev = PriceVolumeTrendReversal(dataframe_input = df_input, lookback_period = lookback)
        pvt_rev_weight, _liveSignal_list = pvt_rev.run(reading_lookback)
        pvt_rev_weightedSignal = generate_weightedList(pvt_rev_liveSignal_list)
        pvt_rev_weight = weight_adjust(pvt_rev_weight)

        roc = RateOfChange(dataframe_input = df_input, lookback_period = lookback)
        roc_weight, _liveSignal_list = roc.run(reading_lookback)
        roc_weightedSignal = generate_weightedList(roc_liveSignal_list)
        roc_weight = weight_adjust(roc_weight)

        rsi = RelativeStrengthIndex(dataframe_input = df_input, lookback_period = lookback)
        rsi_weight, rsi_liveSignal_list = rsi.run(reading_lookback)
        rsi_weightedSignal = generate_weightedList(rsi_liveSignal_list)
        rsi_weight = weight_adjust(rsi_weight)

        sma_osc = SimpleMovingAverageOscillator(dataframe_input = df_input, lookback_period = lookback)
        sma_osc_weight, sma_osc_liveSignal_list = sma_osc.run(reading_lookback)
        sma_osc_weightedSignal = generate_weightedList(sma_osc_liveSignal_list)
        sma_osc_weight = weight_adjust(sma_osc_weight)

        smi_erg = SMIErgodic(dataframe_input = df_input, lookback_period = lookback)
        smi_erg_weight, smi_erg_liveSignal_list = smi_erg.run(reading_lookback)
        smi_erg_weightedSignal = generate_weightedList(smi_erg_liveSignal_list)
        smi_erg_weight = weight_adjust(smi_erg_weight)

        stoch_osc = StochasticOscillator(dataframe_input = df_input, lookback_period = lookback)
        stoch_osc_weight, stoch_osc_liveSignal_list = stoch_osc.run(reading_lookback)
        stoch_osc_weightedSignal = generate_weightedList(stoch_osc_liveSignal_list)
        stoch_osc_weight = weight_adjust(stoch_osc_weight)

        stoch_osc_rev = StochasticOscillatorReversal(dataframe_input = df_input, lookback_period = lookback)
        stoch_osc_rev_weight, stoch_osc_rev_liveSignal_list = stoch_osc_rev.run(reading_lookback)
        stoch_osc_rev_weightedSignal = generate_weightedList(stoch_osc_rev_liveSignal_list)
        stoch_osc_rev_weight = weight_adjust(stoch_osc_rev_weight)

        wma = WeightedMovingAverage(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2= lookback + 3)
        wma_weight, wma_liveSignal_list = wma.run(reading_lookback)
        wma_weightedSignal = generate_weightedList(wma_liveSignal_list)
        wma_weight = weight_adjust(wma_weight)

        trix = TRIX(dataframe_input = df_input, lookback_period = lookback)
        trix_weight, trix_liveSignal_list = trix.run(reading_lookback)
        trix_weightedSignal = generate_weightedList(trix_liveSignal_list)
        trix_weight = weight_adjust(trix_weight)

        tsi = TrueStrengthIndicator(dataframe_input = df_input, lookback_period = lookback)
        tsi_weight, tsi_liveSignal_list = tsi.run(reading_lookback)
        tsi_weightedSignal = generate_weightedList(tsi_liveSignal_list)
        tsi_weight = weight_adjust(tsi_weight)

        vol_osc = VolumeOscillator(dataframe_input = df_input, lookback_period = lookback)
        _weight, _liveSignal_list = .run(reading_lookback)
        _weightedSignal = generate_weightedList(_liveSignal_list)
        _weight = weight_adjust(_weight)

        vor_osc = VortexOscillator(dataframe_input = df_input, lookback_period = lookback)
        vor_osc_weight, vor_osc_liveSignal_list = vor_osc.run(reading_lookback)
        vor_osc_weightedSignal = generate_weightedList(vor_osc_liveSignal_list)
        vor_osc_weight = weight_adjust(vor_osc_weight)

        will_r = WilliamsPercentR(dataframe_input = df_input, lookback_period = lookback)
        will_r_weight, will_r_liveSignal_list = will_r.run(reading_lookback)
        will_r_weightedSignal = generate_weightedList(will_r_liveSignal_list)
        will_r_weight = weight_adjust(will_r_weight)

        


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
    
     
