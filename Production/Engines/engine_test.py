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
from numba import float64
from numba import jit
from numba.experimental import jitclass


class_data = [
    ('dict_of_dataframes', dict),
    ('base_lookback', int),
    ('reading_lookback', int),
    ('number_of_readings', int),
]

class Engine1:
    def __init__(self, dict_of_dataframes, base_lookback, reading_lookback, number_of_readings):
        self.dict_of_dataframes = dict_of_dataframes
        self.base_lookback = base_lookback
        self.reading_lookback = reading_lookback
        self.number_of_readings = number_of_readings

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

        #Accumulation Distribution
        acc_dist = AccumulationDistribution(dataframe_input = df_input, lookback_period = lookback)
        acc_dist_weight, acc_dist_liveSignal_list = acc_dist.run(reading_lookback)
        acc_dist_weightedSignal = self.generate_weightedList(acc_dist_liveSignal_list)
        acc_dist_weight = self.weight_adjust(acc_dist_weight)

        #Aroon
        aroon = Aroon(dataframe_input = df_input, lookback_period = lookback)
        aroon_weight, aroon_liveSignal_list = aroon.run(reading_lookback)
        aroon_weightedSignal = self.generate_weightedList(aroon_liveSignal_list)
        aroon_weight = self.weight_adjust(aroon_weight)

        #Balance Of Power
        bop = BalanceOfPower(dataframe_input = df_input)
        bop_weight, bop_liveSignal_list = bop.run(reading_lookback)
        bop_weightedSignal = self.generate_weightedList(bop_liveSignal_list)
        bop_weight = self.weight_adjust(bop_weight)

        #Bollinger Bands - EMA
        bol_ema = BollingerEMA(dataframe_input = df_input, lookback_period = lookback)
        bol_ema_weight, bol_ema_liveSignal_list = bol_ema.run(reading_lookback)
        bol_ema_weightedSignal = self.generate_weightedList(bol_ema_liveSignal_list)
        bol_ema_weight = self.weight_adjust(bol_ema_weight)

        #Bollinger Bands - SMA
        bol_sma = BollingerSMA(dataframe_input = df_input, lookback_period = lookback)
        bol_sma_weight, bol_sma_liveSignal_list = bol_sma.run(reading_lookback)
        bol_sma_weightedSignal = self.generate_weightedList(bol_sma_liveSignal_list)
        bol_sma_weight = self.weight_adjust(bol_sma_weight)

        #Chaikin Oscillator
        try:
            chaik_osc = ChaikinOscillator(dataframe_input = df_input, lookback_period = lookback)
            chaik_osc_weight, chaik_osc_liveSignal_list = chaik_osc.run(reading_lookback)
            chaik_osc_weightedSignal = self.generate_weightedList(chaik_osc_liveSignal_list)
            chaik_osc_weight = self.weight_adjust(chaik_osc_weight)
        except:
            chaik_osc_weight = 0
            chaik_osc_weightedSignal = 0

        #Commodity Channel Index 
        cci = CommodityChannelIndex(dataframe_input = df_input, lookback_period = lookback)
        cci_weight, cci_liveSignal_list = cci.run(reading_lookback)
        cci_weightedSignal = self.generate_weightedList(cci_liveSignal_list)
        cci_weight = self.weight_adjust(cci_weight)

        #Connors RSI
        con_rsi = ConnorsRSI(dataframe_input = df_input, lookback_period = lookback)
        con_rsi_weight, con_rsi_liveSignal_list = con_rsi.run(reading_lookback)
        con_rsi_weightedSignal = self.generate_weightedList(con_rsi_liveSignal_list)
        con_rsi_weight = self.weight_adjust(con_rsi_weight)

        #Coppock Curve
        cop_cur = CoppockCurve(dataframe_input = df_input, lookback_period = lookback)
        cop_cur_weight, cop_cur_liveSignal_list = cop_cur.run(reading_lookback)
        cop_cur_weightedSignal = self.generate_weightedList(cop_cur_liveSignal_list)
        cop_cur_weight = self.weight_adjust(cop_cur_weight)

        #Directional Movement
        dir_mov = DirectionalMovement(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2 = lookback + 3)
        dir_mov_weight, dir_mov_liveSignal_list = dir_mov.run(reading_lookback)
        dir_mov_weightedSignal = self.generate_weightedList(dir_mov_liveSignal_list)
        dir_mov_weight = self.weight_adjust(dir_mov_weight)

        #Donchian Channels
        donch = DonchianChannels(dataframe_input = df_input, lookback_period = lookback)
        donch_weight, donch_liveSignal_list = donch.run(reading_lookback)
        donch_weightedSignal = self.generate_weightedList(donch_liveSignal_list)
        donch_weight = self.weight_adjust(donch_weight)

        #Elders Force
        el_force = EldersForce(dataframe_input = df_input, lookback_period = lookback)
        el_force_weight, el_force_liveSignal_list = el_force.run(reading_lookback)
        el_force_weightedSignal = self.generate_weightedList(el_force_liveSignal_list)
        el_force_weight = self.weight_adjust(el_force_weight)

        #Envelope - EMA
        env_ema = EnvelopeEMA(dataframe_input = df_input, lookback_period = lookback)
        env_ema_weight, env_ema_liveSignal_list = env_ema.run(reading_lookback)
        env_ema_weightedSignal = self.generate_weightedList(env_ema_liveSignal_list)
        env_ema_weight = self.weight_adjust(env_ema_weight)

        #Envelope - SMA
        env_sma = EnvelopeSMA(dataframe_input = df_input, lookback_period = lookback)
        env_sma_weight, env_sma_liveSignal_list = env_sma.run(reading_lookback)
        env_sma_weightedSignal = self.generate_weightedList(env_sma_liveSignal_list)
        env_sma_weight = self.weight_adjust(env_sma_weight)

        #Exponential Moving Average
        ema = ExponentialMovingAverage(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2 = lookback + 3)
        ema_weight, ema_liveSignal_list = ema.run(reading_lookback)
        ema_weightedSignal = self.generate_weightedList(ema_liveSignal_list)
        ema_weight = self.weight_adjust(ema_weight)

        #Simple Moving Average
        sma = SimpleMovingAverage(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2 = lookback + 3)
        sma_weight, sma_liveSignal_list = sma.run(reading_lookback)
        sma_weightedSignal = self.generate_weightedList(sma_liveSignal_list)
        sma_weight = self.weight_adjust(sma_weight)

        #Fisher Transform
        fish_transform = FisherTransform(dataframe_input = df_input, lookback_period = lookback)
        fish_transform_weight, fish_transform_liveSignal_list = fish_transform.run(reading_lookback)
        fish_transform_weightedSignal = self.generate_weightedList(fish_transform_liveSignal_list)
        fish_transform_weight = self.weight_adjust(fish_transform_weight)

        #Fisher Transform Reversal 
        fish_trans_rev = FisherTransformReversal(dataframe_input = df_input, lookback_period = lookback)
        fish_trans_rev_weight, fish_trans_rev_liveSignal_list = fish_trans_rev.run(reading_lookback)
        fish_trans_rev_weightedSignal = self.generate_weightedList(fish_trans_rev_liveSignal_list)
        fish_trans_rev_weight = self.weight_adjust(fish_trans_rev_weight)

        #McGinley Dynamic
        mcg_dyn = McGinleyDynamic(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2 = lookback + 3)
        mcg_dyn_weight, mcg_dyn_liveSignal_list = mcg_dyn.run(reading_lookback)
        mcg_dyn_weightedSignal = self.generate_weightedList(mcg_dyn_liveSignal_list)
        mcg_dyn_weight = self.weight_adjust(mcg_dyn_weight)

        #Keltner Channel
        kelt_chnl = KeltnerChannel(dataframe_input = df_input, lookback_period = lookback)
        kelt_chnl_weight, kelt_chnl_liveSignal_list = kelt_chnl.run(reading_lookback)
        kelt_chnl_weightedSignal = self.generate_weightedList(kelt_chnl_liveSignal_list)
        kelt_chnl_weight = self.weight_adjust(kelt_chnl_weight)

        #Linear Regression
        lin_reg = LinearRegression(dataframe_input = df_input, lookback_period = lookback)
        lin_reg_weight, lin_reg_liveSignal_list = lin_reg.run(reading_lookback)
        lin_reg_weightedSignal = self.generate_weightedList(lin_reg_liveSignal_list)
        lin_reg_weight = self.weight_adjust(lin_reg_weight)

        #Mass Index
        # mass = MassIndex(dataframe_input = df_input, lookback_period = lookback)
        # mass_weight, mass_liveSignal_list = mass.run(reading_lookback)
        # mass_weightedSignal = self.generate_weightedList(mass_liveSignal_list)
        # mass_weight = self.weight_adjust(mass_weight)

        #Momentum Oscillator
        mom_osc = MomentumOscillator(dataframe_input = df_input, lookback_period = lookback)
        mom_osc_weight, mom_osc_liveSignal_list = mom_osc.run(reading_lookback)
        mom_osc_weightedSignal = self.generate_weightedList(mom_osc_liveSignal_list)
        mom_osc_weight = self.weight_adjust(mom_osc_weight)

        #Momentum Oscillator Reversal 
        mom_osc_rev = MomentumOscillatorReversal(dataframe_input = df_input, lookback_period = lookback)
        mom_osc_rev_weight, mom_osc_rev_liveSignal_list = mom_osc_rev.run(reading_lookback)
        mom_osc_rev_weightedSignal = self.generate_weightedList(mom_osc_rev_liveSignal_list)
        mom_osc_rev_weight = self.weight_adjust(mom_osc_rev_weight)

        #Money FLow Index
        mon_flo = MoneyFlowReversal(dataframe_input = df_input, lookback_period = lookback)
        mon_flo_weight, mon_flo_liveSignal_list = mon_flo.run(reading_lookback)
        mon_flo_weightedSignal = self.generate_weightedList(mon_flo_liveSignal_list)
        mon_flo_weight = self.weight_adjust(mon_flo_weight)

        #Moving Average Convergence Divergence
        macd = MovingAverageConvergenceDivergence(dataframe_input = df_input, lookback_period = lookback)
        macd_weight, macd_liveSignal_list = macd.run(reading_lookback)
        macd_weightedSignal = self.generate_weightedList(macd_liveSignal_list)
        macd_weight = self.weight_adjust(macd_weight)

        #On balance Volume
        obv = OnBalanceVolume(dataframe_input = df_input, lookback_period = lookback)
        obv_weight, obv_liveSignal_list = obv.run(reading_lookback)
        obv_weightedSignal = self.generate_weightedList(obv_liveSignal_list)
        obv_weight = self.weight_adjust(obv_weight)

        #Pivot Point
        pvt_pnt = PivotPoint(dataframe_input = df_input, lookback_period = lookback)
        pvt_pnt_weight, pvt_pnt_liveSignal_list = pvt_pnt.run(reading_lookback)
        pvt_pnt_weightedSignal = self.generate_weightedList(pvt_pnt_liveSignal_list)
        pvt_pnt_weight = self.weight_adjust(pvt_pnt_weight)

        #Price Volume Trend
        pvt = PriceVolumeTrend(dataframe_input = df_input, lookback_period = lookback)
        pvt_weight, pvt_liveSignal_list = pvt.run(reading_lookback)
        pvt_weightedSignal = self.generate_weightedList(pvt_liveSignal_list)
        pvt_weight = self.weight_adjust(pvt_weight)

        #Price Volume Reversal
        pvt_rev = PriceVolumeTrendReversal(dataframe_input = df_input, lookback_period = lookback)
        pvt_rev_weight, pvt_rev_liveSignal_list = pvt_rev.run(reading_lookback)
        pvt_rev_weightedSignal = self.generate_weightedList(pvt_rev_liveSignal_list)
        pvt_rev_weight = self.weight_adjust(pvt_rev_weight)

        #Rate of Change
        roc = RateOfChange(dataframe_input = df_input, lookback_period = lookback)
        roc_weight, roc_liveSignal_list = roc.run(reading_lookback)
        roc_weightedSignal = self.generate_weightedList(roc_liveSignal_list)
        roc_weight = self.weight_adjust(roc_weight)

        #Relative Strength Index 
        rsi = RelativeStrengthIndex(dataframe_input = df_input, lookback_period = lookback)
        rsi_weight, rsi_liveSignal_list = rsi.run(reading_lookback)
        rsi_weightedSignal = self.generate_weightedList(rsi_liveSignal_list)
        rsi_weight = self.weight_adjust(rsi_weight)

        #Simple Moving Average Oscillator
        sma_osc = SimpleMovingAverageOscillator(dataframe_input = df_input, lookback_period = lookback)
        sma_osc_weight, sma_osc_liveSignal_list = sma_osc.run(reading_lookback)
        sma_osc_weightedSignal = self.generate_weightedList(sma_osc_liveSignal_list)
        sma_osc_weight = self.weight_adjust(sma_osc_weight)

        #SMI Ergodic
        smi_erg = SMIErgodic(dataframe_input = df_input, lookback_period = lookback)
        smi_erg_weight, smi_erg_liveSignal_list = smi_erg.run(reading_lookback)
        smi_erg_weightedSignal = self.generate_weightedList(smi_erg_liveSignal_list)
        smi_erg_weight = self.weight_adjust(smi_erg_weight)

        #Stochastic Oscillator
        stoch_osc = StochasticOscillator(dataframe_input = df_input, lookback_period = lookback)
        stoch_osc_weight, stoch_osc_liveSignal_list = stoch_osc.run(reading_lookback)
        stoch_osc_weightedSignal = self.generate_weightedList(stoch_osc_liveSignal_list)
        stoch_osc_weight = self.weight_adjust(stoch_osc_weight)

        #Stochastic Oscillator Reversal
        stoch_osc_rev = StochasticOscillatorReversal(dataframe_input = df_input, lookback_period = lookback)
        stoch_osc_rev_weight, stoch_osc_rev_liveSignal_list = stoch_osc_rev.run(reading_lookback)
        stoch_osc_rev_weightedSignal = self.generate_weightedList(stoch_osc_rev_liveSignal_list)
        stoch_osc_rev_weight = self.weight_adjust(stoch_osc_rev_weight)

        #Weighted Moving Average
        wma = WeightedMovingAverage(dataframe_input = df_input, lookback_period1 = lookback, lookback_period2= lookback + 3)
        wma_weight, wma_liveSignal_list = wma.run(reading_lookback)
        wma_weightedSignal = self.generate_weightedList(wma_liveSignal_list)
        wma_weight = self.weight_adjust(wma_weight)

        #TRIX Index
        trix = TRIX(dataframe_input = df_input, lookback_period = lookback)
        trix_weight, trix_liveSignal_list = trix.run(reading_lookback)
        trix_weightedSignal = self.generate_weightedList(trix_liveSignal_list)
        trix_weight = self.weight_adjust(trix_weight)

        #True Strength Indicator
        tsi = TrueStrengthIndicator(dataframe_input = df_input, lookback_period = lookback)
        tsi_weight, tsi_liveSignal_list = tsi.run(reading_lookback)
        tsi_weightedSignal = self.generate_weightedList(tsi_liveSignal_list)
        tsi_weight = self.weight_adjust(tsi_weight)

        #Volume Oscillator
        vol_osc = VolumeOscillator(dataframe_input = df_input, lookback_period = lookback)
        vol_osc_weight, vol_osc_liveSignal_list = vol_osc.run(reading_lookback)
        vol_osc_weightedSignal = self.generate_weightedList(vol_osc_liveSignal_list)
        vol_osc_weight = self.weight_adjust(vol_osc_weight)

        #Vortex Oscillator
        vor_osc = VortexOscillator(dataframe_input = df_input, lookback_period = lookback)
        vor_osc_weight, vor_osc_liveSignal_list = vor_osc.run(reading_lookback)
        vor_osc_weightedSignal = self.generate_weightedList(vor_osc_liveSignal_list)
        vor_osc_weight = self.weight_adjust(vor_osc_weight)

        #Williams %R
        will_r = WilliamsPercentR(dataframe_input = df_input, lookback_period = lookback)
        will_r_weight, will_r_liveSignal_list = will_r.run(reading_lookback)
        will_r_weightedSignal = self.generate_weightedList(will_r_liveSignal_list)
        will_r_weight = self.weight_adjust(will_r_weight)

        total_weight = (
            acc_dist_weight + 
            aroon_weight +
            bop_weight +
            bol_ema_weight +
            bol_sma_weight +
            chaik_osc_weight +
            cci_weight + 
            con_rsi_weight + 
            cop_cur_weight +
            dir_mov_weight + 
            donch_weight + 
            el_force_weight + 
            env_ema_weight +
            env_sma_weight +
            ema_weight + 
            sma_weight + 
            fish_transform_weight + 
            fish_trans_rev_weight + 
            mcg_dyn_weight + 
            kelt_chnl_weight + 
            lin_reg_weight + 
            #mass_weight +
            mom_osc_weight + 
            mom_osc_rev_weight +
            mon_flo_weight + 
            macd_weight + 
            obv_weight + 
            pvt_pnt_weight + 
            pvt_weight + 
            pvt_rev_weight + 
            roc_weight + 
            rsi_weight + 
            sma_osc_weight + 
            smi_erg_weight + 
            stoch_osc_weight + 
            stoch_osc_rev_weight + 
            wma_weight + 
            trix_weight + 
            tsi_weight + 
            vol_osc_weight + 
            vor_osc_weight+ 
            will_r_weight
        )

        # Extra Variables for future research purposes 
        acc_dist_weight = acc_dist_weight/total_weight
        aroon_weight = aroon_weight/total_weight
        bop_weight = bop_weight/total_weight
        bol_ema_weight = bol_ema_weight/total_weight
        bol_sma_weight = bol_sma_weight/total_weight
        chaik_osc_weight = chaik_osc_weight/total_weight
        cci_weight = cci_weight/total_weight
        con_rsi_weight = con_rsi_weight/total_weight
        cop_cur_weight = cop_cur_weight/total_weight
        dir_mov_weight = dir_mov_weight/total_weight
        donch_weight = donch_weight/total_weight
        el_force_weight = el_force_weight/total_weight
        env_ema_weight = env_ema_weight/total_weight
        env_sma_weight = env_sma_weight/total_weight
        ema_weight = ema_weight/total_weight
        sma_weight = sma_weight/total_weight
        fish_transform_weight = fish_transform_weight/total_weight
        fish_trans_rev_weight = fish_trans_rev_weight/total_weight
        mcg_dyn_weight = mcg_dyn_weight/total_weight
        kelt_chnl_weight = kelt_chnl_weight/total_weight
        lin_reg_weight = lin_reg_weight/total_weight
        #mass_weight = mass_weight/total_weight
        mom_osc_weight = mom_osc_weight/total_weight
        mom_osc_rev_weight = mom_osc_rev_weight/total_weight
        mon_flo_weight = mon_flo_weight/total_weight
        macd_weight = macd_weight/total_weight
        obv_weight = obv_weight/total_weight
        pvt_pnt_weight = pvt_pnt_weight/total_weight
        pvt_weight = pvt_weight/total_weight
        pvt_rev_weight = pvt_rev_weight/total_weight
        roc_weight = roc_weight/total_weight
        rsi_weight = rsi_weight/total_weight
        sma_osc_weight = sma_osc_weight/total_weight
        smi_erg_weight = smi_erg_weight/total_weight
        stoch_osc_weight = stoch_osc_weight/total_weight
        stoch_osc_rev_weight = stoch_osc_rev_weight/total_weight
        wma_weight = wma_weight/total_weight
        trix_weight = trix_weight/total_weight
        tsi_weight = tsi_weight/total_weight
        vol_osc_weight = vol_osc_weight/total_weight
        vor_osc_weight = vor_osc_weight/total_weight
        will_r_weight = will_r_weight/total_weight

        final_reading = (
            acc_dist_weight * acc_dist_weightedSignal + 
            aroon_weight * aroon_weightedSignal +
            bop_weight * bop_weightedSignal +
            bol_ema_weight * bol_ema_weightedSignal +
            bol_sma_weight * bol_sma_weightedSignal +
            chaik_osc_weight * chaik_osc_weightedSignal + 
            cci_weight * cci_weightedSignal +
            con_rsi_weight * con_rsi_weightedSignal +
            cop_cur_weight * cop_cur_weightedSignal +
            dir_mov_weight * dir_mov_weightedSignal + 
            donch_weight * donch_weightedSignal + 
            el_force_weight * el_force_weightedSignal + 
            env_ema_weight * env_ema_weightedSignal + 
            env_sma_weight * env_sma_weightedSignal + 
            ema_weight * ema_weightedSignal + 
            sma_weight * sma_weightedSignal + 
            fish_transform_weight * fish_transform_weightedSignal + 
            fish_trans_rev_weight * fish_trans_rev_weightedSignal + 
            mcg_dyn_weight * mcg_dyn_weightedSignal + 
            kelt_chnl_weight * kelt_chnl_weightedSignal + 
            lin_reg_weight * lin_reg_weightedSignal + 
            #mass_weight * mass_weightedSignal + 
            mom_osc_weight * mom_osc_weightedSignal + 
            mom_osc_rev_weight * mom_osc_rev_weightedSignal + 
            mon_flo_weight * mon_flo_weightedSignal + 
            macd_weight * macd_weightedSignal + 
            obv_weight * obv_weightedSignal + 
            pvt_pnt_weight * pvt_pnt_weightedSignal + 
            pvt_weight * pvt_weightedSignal + 
            pvt_rev_weight * pvt_rev_weightedSignal + 
            roc_weight * roc_weightedSignal + 
            rsi_weight * rsi_weightedSignal + 
            sma_osc_weight * sma_osc_weightedSignal + 
            smi_erg_weight * smi_erg_weightedSignal + 
            stoch_osc_weight * stoch_osc_weightedSignal + 
            stoch_osc_rev_weight * stoch_osc_rev_weightedSignal + 
            wma_weight * wma_weightedSignal + 
            trix_weight * trix_weightedSignal + 
            tsi_weight * tsi_weightedSignal + 
            vol_osc_weight * vol_osc_weightedSignal + 
            vor_osc_weight * vor_osc_weightedSignal + 
            will_r_weight * will_r_weightedSignal 
        )

        return final_reading


    def generate_longShortStrength(self, df_input):
        """
        :params: df_input is dataframe for a single security with cols - 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME' 
        :returns: long/short strength based on the lexicon of the lookback_period
        """
        #strength = self.long_short_singlelexicon(df_input, self.base_lookback)
        range_ticker = TradingRange(df_input, 30)
        x = range_ticker.run()
        strength = self.long_short_singlelexicon(df_input, self.base_lookback)
        strength = strength*x
        #strength += self.long_short_singlelexicon(df_input, self.base_lookback - 1)

        return strength
        # take the generator of the lookback_lexicon and run it through the long 
    
    def generate_listOfTickers(self):
        """
        :params: dictionary_input for the basket of securities
        :returns: the list of tickers used 
        """
        # Generate the list of tickers by extracting from the dictionary that is passed into the function
        in_dict = self.dict_of_dataframes
        ticker_list = []
        for ticker in in_dict:
            ticker.append(ticker)
        
        return ticker_list

    def generate(self): 
        """
        :params: dictionary_input for the basket of securities, 
        :returns: The recommendations for the trained period
        """
        # Generate the dictionary based on order of precendence
        
        num = self.number_of_readings
        in_dict = self.dict_of_dataframes
        num = self.number_of_readings
        generated_dict = {}

        for ticker, data in in_dict.items():
            generated_dict[ticker] = self.generate_longShortStrength(data)

        copy_dict_list = generated_dict.items()

        copy_dict = {}
        for ticker, data in copy_dict_list:
            copy_dict[ticker] = abs(data)

        sorted_dictionary = sorted(copy_dict.items(), key = lambda kv: kv[1])
        sorted_dict = dict(sorted_dictionary)

        ticker_list = [i for i in sorted_dict] 

        out_dict = {}
        for i in reversed(ticker_list[-num:]):
            out_dict[i] = generated_dict[i]

        return out_dict





        

     
