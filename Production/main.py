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
import yfinance as yf
from StockDataExtraction.StockData import BasketStockData
from Engines.engine_test import Engine1
from StockDataExtraction.yfinanceDataPull import extract
import time

# stock_data = BasketStockData(True, 200)
# dict1 = stock_data.generate_dict(['AAPL', 'MSFT', 'JPM', 'GS', 'GM', 'TSLA', 'FB', 'GOOGL', 'JNJ', 'DIS', 'CSCO', 'INTC', 'ABT', 'KO', 'ABBV'])
def main():
    list_stok = ['AAPL', 'MSFT', 'ETSY', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'TSLA', 'JPM', 'JNJ', 'V', 'UNH', 'HD', 'NVDA', 'PG', 'DIS', 'MA', 'BAC', 'PYPL', 'XOM', 'CMCSA', 'VZ', 'INTC', 'ADBE', 'T', 'CSCO', 'NFLX', 'PFE', 'KO', 'ABT', 'CVX', 'ABBV', 'PEP', 'CRM', 'MRK', 'WMT', 'WFC', 'TMO', 'ACN', 'AVGO', 'MCD', 'MDT', 'NKE', 'TXN', 'COST', 'DHR', 'HON', 'C', 'LIN', 'QCOM', 'UPS', 'LLY', 'UNP', 'PM', 'LOW', 'ORCL', 'AMGN', 'NEE', 'BMY', 'SBUX', 'IBM', 'MS', 'CAT', 'RTX', 'BA', 'GS', 'BLK', 'DE', 'AMAT', 'MMM', 'GE', 'CVS', 'AMT', 'INTU', 'SCHW', 'TGT', 'AXP', 'ISRG', 'CHTR', 'LMT', 'NOW', 'ANTM', 'MU', 'FIS', 'AMD', 'SPGI', 'BKNG', 'MO', 'CI', 'LRCX', 'MDLZ', 'TJX', 'PLD', 'PNC', 'USB', 'GILD', 'ADP', 'SYK', 'TFC', 'TMUS', 'ZTS', 'CSX', 'CCI', 'CB', 'DUK', 'FDX', 'COP', 'GM', 'CME', 'NSC', 'ATVI', 'COF', 'FISV', 'MMC', 'BDX', 'CL', 'SO', 'SHW', 'ITW', 'EL', 'APD', 'ICE', 'D', 'ADSK', 'EQIX', 'FCX', 'PGR', 'BSX', 'HUM', 'GPN', 'ETN', 'AON', 'NOC', 'ADI', 'EW', 'ECL', 'EMR', 'HCA', 'VRTX', 'WM', 'ILMN', 'NEM', 'DG', 'NXPI', 'MCO', 'REGN', 'DOW', 'MET', 'KLAC', 'ROP', 'JCI', 'KMB', 'ROST', 'F', 'IDXX', 'EOG', 'TEL', 'GD', 'LHX', 'IQV', 'BAX', 'DD', 'HPQ', 'AEP', 'SYY', 'EXC', 'AIG', 'TT', 'SLB', 'TWTR', 'TROW', 'PPG', 'ALGN', 'DLR', 'PRU', 'PSA', 'BK', 'BIIB', 'SRE', 'STZ', 'PH', 'EA', 'TRV', 'SPG', 'A', 'ALL', 'APH', 'INFO', 'CTSH', 'CMG', 'MCHP', 'ORLY', 'CMI', 'MSCI', 'WBA', 'GIS', 'MPC', 'APTV', 'EBAY', 'MAR', 'CNC', 'XEL', 'PSX', 'ALXN', 'ADM', 'IFF', 'YUM', 'SNPS', 'DFS', 'CARR', 'CTVA', 'ZBH', 'AFL', 'LUV', 'CDNS', 'MNST', 'GLW', 'SWK', 'WLTW', 'DXCM', 'KMI', 'DHI', 'PXD', 'HLT', 'AZO', 'VLO', 'TDG', 'FRC', 'PAYX', 'PCAR', 'OTIS', 'SBAC', 'MSI', 'PEG', 'AME', 'ROK', 'CTAS', 'WEC', 'AMP', 'STT', 'WELL', 'MTD', 'FAST', 'WMB', 'SIVB', 'XLNX', 'FITB', 'BLL', 'MCK', 'LYB', 'WY', 'LEN', 'SWKS', 'ES', 'EFX', 'AJG', 'ANSS', 'VFC', 'KR', 'DAL', 'CBRE', 'NUE', 'VRSK', 'RMD', 'FTNT', 'KHC', 'AWK', 'BBY', 'DTE', 'DLTR', 'LH', 'AVB', 'KSU', 'ED', 'KEYS', 'MXIM', 'CPRT', 'ODFL', 'VMC', 'EQR', 'O', 'ZBRA', 'NTRS', 'URI', 'HSY', 'FTV', 'WST', 'SYF', 'CDW', 'IP', 'HIG', 'FLT', 'OKE', 'RSG', 'CLX', 'MLM', 'TSN', 'CERN', 'TSCO', 'EXPE', 'MKC', 'ARE', 'VIAC', 'EIX', 'OXY', 'VRSN', 'HES', 'PPL', 'KEY', 'DOV', 'RF', 'CHD', 'ETR', 'XYL', 'WDC', 'CZR', 'HPE', 'AEE', 'KMX', 'GRMN', 'TER', 'QRVO', 'MTB', 'CFG', 'CCL', 'IT', 'FE', 'VTR', 'GWW', 'GNRC', 'COO', 'HAL', 'ETSY', 'EXPD', 'AMCR', 'TTWO', 'CE', 'WAT', 'GPC', 'BR', 'TRMB', 'TFX', 'EXR', 'NDAQ', 'LVS', 'CAG', 'CMS', 'ESS', 'DRI', 'DGX', 'IR', 'AVY', 'OMC', 'STX', 'PEAK', 'J', 'AKAM', 'STE', 'CINF', 'ANET', 'ULTA', 'MAA', 'ALB', 'NVR', 'RCL', 'CTLT', 'POOL', 'ABC', 'NTAP', 'K', 'IEX', 'DRE', 'AES', 'MAS', 'UAL', 'PFG', 'EMN', 'BKR', 'VTRS', 'HOLX', 'RJF', 'DPZ', 'MKTX', 'CAH', 'TYL', 'PHM', 'TDY', 'PAYC', 'HBAN', 'MGM', 'WRK', 'WHR', 'INCY', 'PKI', 'LB', 'ENPH', 'TXT', 'BXP', 'FBHS', 'FMC', 'SJM', 'DVN', 'CTXS', 'FANG', 'XRAY', 'JBHT', 'PKG', 'WAB', 'EVRG', 'MPWR', 'LNT', 'LDOS', 'PTC', 'LKQ', 'PWR', 'UDR', 'SNA', 'AAP', 'ABMD', 'CNP', 'HRL', 'MHK', 'LUMN', 'L', 'AAL', 'CHRW', 'ATO', 'TPR', 'BIO', 'WYNN', 'IPG', 'ALLE', 'HAS', 'HWM', 'FOXA', 'BWA', 'PENN', 'LNC', 'MOS', 'NLOK', 'HST', 'JKHY', 'UHS', 'IRM', 'CBOE', 'DISH', 'LW', 'HSIC', 'WRB', 'FFIV', 'TAP', 'PNR', 'CF', 'NWL', 'RE', 'CMA', 'LYV', 'IVZ', 'WU', 'NWSA', 'CPB', 'RHI', 'REG', 'NCLH', 'GL', 'NI', 'ZION', 'AOS', 'PNW', 'NLSN', 'AIZ', 'BEN', 'DISCK', 'MRO', 'KIM', 'DVA', 'JNPR', 'SEE', 'HII', 'DXC', 'NRG', 'ALK', 'ROL', 'PVH', 'APA', 'PBCT', 'FRT', 'FLIR', 'HBI', 'LEG', 'VNO', 'GPS', 'IPGP', 'COG', 'RL', 'NOV', 'UNM', 'DISCA']
    begin = time.time()
    #x = extract(list_stok)
    stock_data = BasketStockData(True, 100)
    x = stock_data.generate_dict(list_stok)
    end = time.time()
    print(f"Time taken to extract data: {end - begin}")

    begin1 = time.time()
    dict_of_dataframes = x
    base_lookback = 5
    reading_lookback = 1
    number_of_readings = 5

    eng_obj = Engine1(dict_of_dataframes = dict_of_dataframes, base_lookback = base_lookback, reading_lookback = reading_lookback, number_of_readings = number_of_readings)
    longs, shorts = eng_obj.generate()
    print ("Metrics " + '\n' + "Base Lookback: " + str(base_lookback) + '\n' + "Reading Lookback: " + str(reading_lookback) + '\n' + "Number of Readings: " + str(number_of_readings))
    print("Longs: ")
    print(longs)
    print()
    print("Shorts: ")
    print(shorts)
    print()

    end1 = time.time()
    print(f"Time taken to compute data: {end1 - begin1}")

if __name__ == '__main__':
    main()
# ['FB'])
# print(dict1)