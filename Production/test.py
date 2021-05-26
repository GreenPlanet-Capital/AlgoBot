from StockDataExtraction.StockData import BasketStockData
import sys
from Backtesters.SwingBacktest import SwingBacktest


def main():
    list_stok = ['AAPL', 'MSFT', 'ETSY', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'TSLA', 'JPM', 'JNJ', 'V', 'UNH', 'HD', 'NVDA', 'PG', 'DIS', 'MA', 'BAC', 'PYPL', 'XOM', 'CMCSA', 'VZ', 'INTC', 'ADBE', 'T', 'CSCO', 'NFLX', 'PFE', 'KO', 'ABT', 'CVX', 'ABBV', 'PEP', 'CRM', 'MRK', 'WMT', 'WFC', 'TMO', 'ACN', 'AVGO', 'MCD', 'MDT', 'NKE', 'TXN', 'COST', 'DHR', 'HON', 'C', 'LIN', 'QCOM', 'UPS', 'LLY', 'UNP', 'PM', 'LOW', 'ORCL', 'AMGN', 'NEE', 'BMY', 'SBUX', 'IBM', 'MS', 'CAT', 'RTX', 'BA', 'GS', 'BLK', 'DE', 'AMAT', 'MMM', 'GE', 'CVS', 'AMT', 'INTU', 'SCHW', 'TGT', 'AXP', 'ISRG', 'CHTR', 'LMT', 'NOW', 'ANTM', 'MU', 'FIS', 'AMD', 'SPGI', 'BKNG', 'MO', 'CI', 'LRCX', 'MDLZ', 'TJX', 'PLD', 'PNC', 'USB', 'GILD', 'ADP', 'SYK', 'TFC', 'TMUS', 'ZTS', 'CSX', 'CCI', 'CB', 'DUK', 'FDX', 'COP', 'GM', 'CME', 'NSC', 'ATVI', 'COF', 'FISV', 'MMC', 'BDX', 'CL', 'SO', 'SHW', 'ITW', 'EL', 'APD', 'ICE', 'D', 'ADSK', 'EQIX', 'FCX', 'PGR', 'BSX', 'HUM', 'GPN', 'ETN', 'AON', 'NOC', 'ADI', 'EW', 'ECL', 'EMR', 'HCA', 'VRTX', 'WM', 'ILMN', 'NEM', 'DG', 'NXPI', 'MCO', 'REGN', 'DOW', 'MET', 'KLAC', 'ROP', 'JCI', 'KMB', 'ROST', 'F', 'IDXX', 'EOG', 'TEL', 'GD', 'LHX', 'IQV', 'BAX', 'DD', 'HPQ', 'AEP', 'SYY', 'EXC', 'AIG', 'TT', 'SLB', 'TWTR', 'TROW', 'PPG', 'ALGN', 'DLR', 'PRU', 'PSA', 'BK', 'BIIB', 'SRE', 'STZ', 'PH', 'EA', 'TRV', 'SPG', 'A', 'ALL', 'APH', 'INFO', 'CTSH', 'CMG', 'MCHP', 'ORLY', 'CMI', 'MSCI', 'WBA', 'GIS', 'MPC', 'APTV', 'EBAY', 'MAR', 'CNC', 'XEL', 'PSX', 'ALXN', 'ADM', 'IFF', 'YUM', 'SNPS', 'DFS', 'CARR', 'CTVA', 'ZBH', 'AFL', 'LUV', 'CDNS', 'MNST', 'GLW', 'SWK', 'WLTW', 'DXCM', 'KMI', 'DHI', 'PXD', 'HLT', 'AZO', 'VLO', 'TDG', 'FRC', 'PAYX', 'PCAR', 'OTIS', 'SBAC', 'MSI', 'PEG', 'AME', 'ROK', 'CTAS', 'WEC', 'AMP', 'STT', 'WELL', 'MTD', 'FAST', 'WMB', 'SIVB', 'XLNX', 'FITB', 'BLL', 'MCK', 'LYB', 'WY', 'LEN', 'SWKS', 'ES', 'EFX', 'AJG', 'ANSS', 'VFC', 'KR', 'DAL', 'CBRE', 'NUE', 'VRSK', 'RMD', 'FTNT', 'KHC', 'AWK', 'BBY', 'DTE', 'DLTR', 'LH', 'AVB', 'KSU', 'ED', 'KEYS', 'MXIM', 'CPRT', 'ODFL', 'VMC', 'EQR', 'O', 'ZBRA', 'NTRS', 'URI', 'HSY', 'FTV', 'WST', 'SYF', 'CDW', 'IP', 'HIG', 'FLT', 'OKE', 'RSG', 'CLX', 'MLM', 'TSN', 'CERN', 'TSCO', 'EXPE', 'MKC', 'ARE', 'VIAC', 'EIX', 'OXY', 'VRSN', 'HES', 'PPL', 'KEY', 'DOV', 'RF', 'CHD', 'ETR', 'XYL', 'WDC', 'CZR', 'HPE', 'AEE', 'KMX', 'GRMN', 'TER', 'QRVO', 'MTB', 'CFG', 'CCL', 'IT', 'FE', 'VTR', 'GWW', 'GNRC', 'COO', 'HAL', 'ETSY', 'EXPD', 'AMCR', 'TTWO', 'CE', 'WAT', 'GPC', 'BR', 'TRMB', 'TFX', 'EXR', 'NDAQ', 'LVS', 'CAG', 'CMS', 'ESS', 'DRI', 'DGX', 'IR', 'AVY', 'OMC', 'STX', 'PEAK', 'J', 'AKAM', 'STE', 'CINF', 'ANET', 'ULTA', 'MAA', 'ALB', 'NVR', 'RCL', 'CTLT', 'POOL', 'ABC', 'NTAP', 'K', 'IEX', 'DRE', 'AES', 'MAS', 'UAL', 'PFG', 'EMN', 'BKR', 'VTRS', 'HOLX', 'RJF', 'DPZ', 'MKTX', 'CAH', 'TYL', 'PHM', 'TDY', 'PAYC', 'HBAN', 'MGM', 'WRK', 'WHR', 'INCY', 'PKI', 'LB', 'ENPH', 'TXT', 'BXP', 'FBHS', 'FMC', 'SJM', 'DVN', 'CTXS', 'FANG', 'XRAY', 'JBHT', 'PKG', 'WAB', 'EVRG', 'MPWR', 'LNT', 'LDOS', 'PTC', 'LKQ', 'PWR', 'UDR', 'SNA', 'AAP', 'ABMD', 'CNP', 'HRL', 'MHK', 'LUMN', 'L', 'AAL', 'CHRW', 'ATO', 'TPR', 'BIO', 'WYNN', 'IPG', 'ALLE', 'HAS', 'HWM', 'FOXA', 'BWA', 'PENN', 'LNC', 'MOS', 'NLOK', 'HST', 'JKHY', 'UHS', 'IRM', 'CBOE', 'DISH', 'LW', 'HSIC', 'WRB', 'FFIV', 'TAP', 'PNR', 'CF', 'NWL', 'RE', 'CMA', 'LYV', 'IVZ', 'WU', 'NWSA', 'CPB', 'RHI', 'REG', 'NCLH', 'GL', 'NI', 'ZION', 'AOS', 'PNW', 'NLSN', 'AIZ', 'BEN', 'DISCK', 'MRO', 'KIM', 'DVA', 'JNPR', 'SEE', 'HII', 'DXC', 'NRG', 'ALK', 'ROL', 'PVH', 'APA', 'PBCT', 'FRT', 'FLIR', 'HBI', 'LEG', 'VNO', 'GPS', 'IPGP', 'COG', 'RL', 'NOV', 'UNM', 'DISCA']
    stock_data = BasketStockData(True, 1000)
    if len(sys.argv)>1:
        if sys.argv[1]=='--update':
            update_data = True
    else:
        update_data = False
    x = stock_data.generate_dict(list_stok,update_data=update_data)

    backtest_obj = SwingBacktest(input_dict = x, training_period = 70, test_period = 0, position_expiry = 10, max_positions = 10, stop_loss_percent = 0.03)
    backtest_obj.clean_dictionary()
    backtest_obj.test()

if __name__ == '__main__':
    main()