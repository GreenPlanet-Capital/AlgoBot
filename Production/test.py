from StockDataExtraction.StockData import BasketStockData
import sys
from Backtesters.SwingBacktest import SwingLongShortBacktest
from Backtesters.OptimisedBackTester import OptimisedBackTester
from Backtesters.V1.Backtester import Backtester
import time
import sys

def main():
    #list_stok = ['AUDCAD=X', 'AUDCHF=X', 'AUDCZK=X', 'AUDDKK=X', 'AUDHKD=X', 'AUDHUF=X', 'AUDJPY=X', 'AUDMXN=X', 'AUDNOK=X', 'AUDNZD=X', 'AUDPLN=X', 'AUDSEK=X', 'AUDSGD=X', 'AUDUSD=X', 'AUDZAR=X', 'CADCHF=X', 'CADCZK=X', 'CADDKK=X', 'CADHKD=X', 'CADHUF=X', 'CADJPY=X', 'CADMXN=X',  'CADNOK=X', 'CADPLN=X', 'CADSEK=X', 'CADSGD=X', 'CADZAR=X', 'CHFCZK=X', 'CHFDKK=X', 'CHFHKD=X', 'CHFHUF=X', 'CHFJPY=X', 'CHFMXN=X', 'CHFNOK=X', 'CHFPLN=X', 'CHFSEK=X', 'CHFSGD=X', 'CHFTRY=X', 'CHFZAR=X', 'DKKCZK=X', 'DKKHKD=X', 'DKKHUF=X', 'DKKMXN=X', 'DKKNOK=X',  'DKKPLN=X', 'DKKSEK=X', 'DKKSGD=X', 'DKKZAR=X', 'EURAUD=X', 'EURCAD=X', 'EURCHF=X', 'EURCZK=X', 'EURDKK=X', 'EURGBP=X', 'EURHKD=X',  'EURHUF=X', 'EURJPY=X', 'EURMXN=X', 'EURNOK=X', 'EURNZD=X', 'EURPLN=X', 'EURSEK=X', 'EURSGD=X', 'EURTRY=X', 'EURUSD=X', 'EURZAR=X', 'GBPAUD=X', 'GBPCAD=X', 'GBPCHF=X', 'GBPCZK=X', 'GBPDKK=X', 'GBPHKD=X', 'GBPHUF=X', 'GBPJPY=X', 'GBPMXN=X', 'GBPNOK=X', 'GBPNZD=X',  'GBPPLN=X', 'GBPSEK=X','GBPSGD=X', 'GBPUSD=X', 'GBPZAR=X', 'JPYCZK=X', 'JPYDKK=X', 'JPYHKD=X', 'JPYHUF=X', 'JPYMXN=X', 'JPYNOK=X', 'JPYPLN=X', 'JPYSEK=X', 'JPYSGD=X', 'JPYZAR=X', 'NOKCZK=X', 'NOKHKD=X', 'NOKHUF=X', 'NOKMXN=X', 'NOKPLN=X', 'NOKSEK=X', 'NOKSGD=X', 'NOKZAR=X', 'NZDCAD=X', 'NZDCHF=X', 'NZDCZK=X', 'NZDDKK=X', 'NZDHKD=X', 'NZDHUF=X', 'NZDJPY=X', 'NZDMXN=X', 'NZDNOK=X', 'NZDPLN=X', 'NZDSEK=X',  'NZDSGD=X', 'NZDUSD=X', 'NZDZAR=X', 'USDCAD=X', 'USDCHF=X', 'USDCZK=X', 'USDDKK=X', 'USDHKD=X', 'USDHUF=X','USDJPY=X', 'USDMXN=X', 'USDNOK=X', 'USDPLN=X', 'USDSEK=X', 'USDSGD=X', 'USDTRY=X','USDZAR=X']
    #list_stok = ['AAPL', 'MSFT', 'ETSY', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'TSLA', 'JPM', 'JNJ', 'V', 'UNH', 'HD', 'NVDA', 'PG', 'DIS', 'MA', 'BAC', 'PYPL', 'XOM', 'CMCSA', 'VZ', 'INTC', 'ADBE', 'T', 'CSCO', 'NFLX', 'PFE', 'KO', 'ABT', 'CVX', 'ABBV', 'PEP', 'CRM', 'MRK', 'WMT', 'WFC', 'TMO', 'ACN', 'AVGO', 'MCD', 'MDT', 'NKE', 'TXN', 'COST', 'DHR', 'HON', 'C', 'LIN', 'QCOM', 'UPS', 'LLY', 'UNP', 'PM', 'LOW', 'ORCL', 'AMGN', 'NEE', 'BMY', 'SBUX', 'IBM', 'MS', 'CAT', 'RTX', 'BA', 'GS', 'BLK', 'DE', 'AMAT', 'MMM', 'GE', 'CVS', 'AMT', 'INTU', 'SCHW', 'TGT', 'AXP', 'ISRG', 'CHTR', 'LMT', 'NOW', 'ANTM', 'MU', 'FIS', 'AMD', 'SPGI', 'BKNG', 'MO', 'CI', 'LRCX', 'MDLZ', 'TJX', 'PLD', 'PNC', 'USB', 'GILD', 'ADP', 'SYK', 'TFC', 'TMUS', 'ZTS', 'CSX', 'CCI', 'CB', 'DUK', 'FDX', 'COP', 'GM', 'CME', 'NSC', 'ATVI', 'COF', 'FISV', 'MMC', 'BDX', 'CL', 'SO', 'SHW', 'ITW', 'EL', 'APD', 'ICE', 'D', 'ADSK', 'EQIX', 'FCX', 'PGR', 'BSX', 'HUM', 'GPN', 'ETN', 'AON', 'NOC', 'ADI', 'EW', 'ECL', 'EMR', 'HCA', 'VRTX', 'WM', 'ILMN', 'NEM', 'DG', 'NXPI', 'MCO', 'REGN', 'DOW', 'MET', 'KLAC', 'ROP', 'JCI', 'KMB', 'ROST', 'F', 'IDXX', 'EOG', 'TEL', 'GD', 'LHX', 'IQV', 'BAX', 'DD', 'HPQ', 'AEP', 'SYY', 'EXC', 'AIG', 'TT', 'SLB', 'TWTR', 'TROW', 'PPG', 'ALGN', 'DLR', 'PRU', 'PSA', 'BK', 'BIIB', 'SRE', 'STZ', 'PH', 'EA', 'TRV', 'SPG', 'A', 'ALL', 'APH', 'INFO', 'CTSH', 'CMG', 'MCHP', 'ORLY', 'CMI', 'MSCI', 'WBA', 'GIS', 'MPC', 'APTV', 'EBAY', 'MAR', 'CNC', 'XEL', 'PSX', 'ALXN', 'ADM', 'IFF', 'YUM', 'SNPS', 'DFS', 'CTVA', 'ZBH', 'AFL', 'LUV', 'CDNS', 'MNST', 'GLW', 'SWK', 'WLTW', 'DXCM', 'KMI', 'DHI', 'PXD', 'HLT', 'AZO', 'VLO', 'TDG', 'FRC', 'PAYX', 'PCAR', 'SBAC', 'MSI', 'PEG', 'AME', 'ROK', 'CTAS', 'WEC', 'AMP', 'STT', 'WELL', 'MTD', 'FAST', 'WMB', 'SIVB', 'XLNX', 'FITB', 'BLL', 'MCK', 'LYB', 'WY', 'LEN', 'SWKS', 'ES', 'EFX', 'AJG', 'ANSS', 'VFC', 'KR', 'DAL', 'CBRE', 'NUE', 'VRSK', 'RMD', 'FTNT', 'KHC', 'AWK', 'BBY', 'DTE', 'DLTR', 'LH', 'AVB', 'KSU', 'ED', 'KEYS', 'MXIM', 'CPRT', 'ODFL', 'VMC', 'EQR', 'O', 'ZBRA', 'NTRS', 'URI', 'HSY', 'FTV', 'WST', 'SYF', 'CDW', 'IP', 'HIG', 'FLT', 'OKE', 'RSG', 'CLX', 'MLM', 'TSN', 'CERN', 'TSCO', 'EXPE', 'MKC', 'ARE', 'VIAC', 'EIX', 'OXY', 'VRSN', 'HES', 'PPL', 'KEY', 'DOV', 'RF', 'CHD', 'ETR', 'XYL', 'WDC', 'CZR', 'HPE', 'AEE', 'KMX', 'GRMN', 'TER', 'QRVO', 'MTB', 'CFG', 'CCL', 'IT', 'FE', 'VTR', 'GWW', 'GNRC', 'COO', 'HAL', 'ETSY', 'EXPD', 'AMCR', 'TTWO', 'CE', 'WAT', 'GPC', 'BR', 'TRMB', 'TFX', 'EXR', 'NDAQ', 'LVS', 'CAG', 'CMS', 'ESS', 'DRI', 'DGX', 'IR', 'AVY', 'OMC', 'STX', 'PEAK', 'J', 'AKAM', 'STE', 'CINF', 'ANET', 'ULTA', 'MAA', 'ALB', 'NVR', 'RCL', 'CTLT', 'POOL', 'ABC', 'NTAP', 'K', 'IEX', 'DRE', 'AES', 'MAS', 'UAL', 'PFG', 'EMN', 'BKR', 'VTRS', 'HOLX', 'RJF', 'DPZ', 'MKTX', 'CAH', 'TYL', 'PHM', 'TDY', 'PAYC', 'HBAN', 'MGM', 'WRK', 'WHR', 'INCY', 'PKI', 'LB', 'ENPH', 'TXT', 'BXP', 'FBHS', 'FMC', 'SJM', 'DVN', 'CTXS', 'FANG', 'XRAY', 'JBHT', 'PKG', 'WAB', 'EVRG', 'MPWR', 'LNT', 'LDOS', 'PTC', 'LKQ', 'PWR', 'UDR', 'SNA', 'AAP', 'ABMD', 'CNP', 'HRL', 'MHK', 'L', 'AAL', 'CHRW', 'ATO', 'TPR', 'BIO', 'WYNN', 'IPG', 'ALLE', 'HAS', 'HWM', 'FOXA', 'BWA', 'PENN', 'LNC', 'MOS', 'NLOK', 'HST', 'JKHY', 'UHS', 'IRM', 'CBOE', 'DISH', 'LW', 'HSIC', 'WRB', 'FFIV', 'TAP', 'PNR', 'CF', 'NWL', 'RE', 'CMA', 'LYV', 'IVZ', 'WU', 'NWSA', 'CPB', 'RHI', 'REG', 'NCLH', 'GL', 'NI', 'ZION', 'AOS', 'PNW', 'NLSN', 'AIZ', 'BEN', 'DISCK', 'MRO', 'KIM', 'DVA', 'JNPR', 'SEE', 'HII', 'DXC', 'NRG', 'ALK', 'ROL', 'PVH', 'APA', 'PBCT', 'FRT', 'FLIR', 'HBI', 'LEG', 'VNO', 'GPS', 'IPGP', 'COG', 'RL', 'NOV', 'UNM', 'DISCA']
    list_stok = ['ADANIPORTS.NS', 'APEX.NS', 'SRF.NS', 'JMFINANCIL.NS', 'SBICARD.NS', 'VIDHIING.NS', 'ASTRAL.NS', 'PGHH.NS', 'FIEMIND.NS', 'BATAINDIA.NS', 'SUNCLAYLTD.NS', 'NETWORK18.NS', 'CGCL.NS', 'BFUTILITIE.NS', 'CENTURYTEX.NS', 'INDIACEM.NS', 'MMP.NS', 'SOMANYCERA.NS', 'HATSUN.NS', 'MAYURUNIQ.NS', 'KRBL.NS', 'KINGFA.NS', 'NRAIL.NS', 'NAVINFLUOR.NS', 'DCBBANK.NS', 'KOKUYOCMLN.NS', 'ZUARI.NS', 'GALAXYSURF.NS', 'KICL.NS', 'IOB.NS', 'ASTRAZEN.NS', 'ITDC.NS', 'CHEMFAB.NS', 'HMT.NS', 'TCS.NS', 'DIVISLAB.NS', 'MAJESCO.NS', 'QUESS.NS', 'DWARKESH.NS', 'BHEL.NS', 'PRAJIND.NS', 'GKWLIMITED.NS', 'MPHASIS.NS', 'KUANTUM.NS', 'FSL.NS', 'POLYCAB.NS', 'GRSE.NS', 'WHEELS.NS', 'TVTODAY.NS', 'INDIAGLYCO.NS', 'IGARASHI.NS', 'PNBGILTS.NS', 'AHLWEST.NS', 'DRREDDY.NS', 'SOLARA.NS', 'KSL.NS', 'RELAXO.NS', 'PETRONET.NS', 'HINDALCO.NS', 'ITDCEM.NS', 'MAHSCOOTER.NS', 'GMBREW.NS', 'RBL.NS', 'MSPL.NS', 'CAPLIPOINT.NS', 'NRBBEARING.NS', 'EIHAHOTELS.NS', 'SWARAJENG.NS', 'MEGH.NS', 'COLPAL.NS', 'NIPPOBATRY.NS', 'ASTRAMICRO.NS', 'AMBIKCO.NS', 'OLECTRA.NS', 'LTI.NS', 'SANGHIIND.NS', 'SPIC.NS', 'RANEHOLDIN.NS', 'WSTCSTPAPR.NS', 'BRIGADE.NS', 'HDFCBANK.NS', 'HCG.NS', 'BEPL.NS', 'ENGINERSIN.NS', 'NBIFIN.NS', 'GREAVESCOT.NS', 'BORORENEW.NS', 'JAICORPLTD.NS', 'PRABHAT.NS', 'MAITHANALL.NS', 'RALLIS.NS', 'POWERGRID.NS', 'COCHINSHIP.NS', 'KIRLOSENG.NS', 'SHARDAMOTR.NS', 'SUPRAJIT.NS', 'MCL.NS', 'DFMFOODS.NS', 'FLFL.NS', 'MPSLTD.NS', 'TIRUMALCHM.NS', 'JBCHEPHARM.NS', 'ANUP.NS', 'DICIND.NS', 'BINDALAGRO.NS', 'PFS.NS', 'DECCANCE.NS', 'TRIVENI.NS', 'GODREJAGRO.NS', 'HAVELLS.NS', 'SMLISUZU.NS', 'SHRIRAMEPC.NS', 'JBMA.NS', 'NESCO.NS', 'INTELLECT.NS', 'UNIONBANK.NS', 'CENTRALBK.NS', 'UNIENTER.NS', 'TATAMETALI.NS', 'RTNPOWER.NS', 'EMAMILTD.NS', 'SUBROS.NS', 'GRINDWELL.NS', 'LAURUSLABS.NS', 'POLYPLEX.NS', 'POWERINDIA.NS', 'SDBL.NS', 'ADANITRANS.NS', 'MEP.NS', 'FINCABLES.NS', 'GEPIL.NS', 'GANECOS.NS', 'VESUVIUS.NS', 'NAUKRI.NS', 'ARMANFIN.NS', 'TCI.NS', 'RAMCOCEM.NS', 'GHCL.NS', 'ASHOKLEY.NS', 'NATIONALUM.NS', 'HEIDELBERG.NS', 'CENTURYPLY.NS', 'CENTENKA.NS', 'TATAINVEST.NS', 'HINDCOPPER.NS', 'GLOBUSSPR.NS', 'INDUSINDBK.NS', 'VENKEYS.NS', 'KSCL.NS', 'UPL.NS', 'BLUESTARCO.NS', 'NATHBIOGEN.NS', 'NDTV.NS', 'HGINFRA.NS', 'ADORWELD.NS', 'QUICKHEAL.NS', 'PRAKASH.NS', 'KSB.NS', 'CHALET.NS', 'SHRIPISTON.NS', 'FRETAIL.NS', 'TATASTLLP.NS', 'CENTUM.NS', 'DEEPAKNTR.NS', 'JAYAGROGN.NS', 'GVKPIL.NS', 'ATFL.NS', 'REPRO.NS', 'TATACOMM.NS', 'BHARTIARTL.NS', 'TITAN.NS', 'ZYDUSWELL.NS', 'JSWSTEEL.NS', 'NMDC.NS', 'NHPC.NS', 'VGUARD.NS', 'SOBHA.NS', 'ALKEM.NS', 'TVSSRICHAK.NS', 'JAYBARMARU.NS', 'EQUITAS.NS', 'VIPULLTD.NS', 'VMART.NS', 'MANINFRA.NS', 'GMRINFRA.NS', 'NTPC.NS', 'INDOCO.NS', 'ALICON.NS', 'ZOTA.NS', 'KIRIINDUS.NS', 'ALEMBICLTD.NS', 'SAIL.NS', 'SYMPHONY.NS', 'JINDWORLD.NS', 'WABCOINDIA.NS', 'EIDPARRY.NS', 'KEI.NS', 'NILKAMAL.NS', 'OCCL.NS', 'SHRIRAMCIT.NS', 'THEINVEST.NS', 'NAGAFERT.NS', 'DCW.NS', 'RAMCOSYS.NS', 'DREDGECORP.NS', 'BAJAJ-AUTO.NS', 'VINDHYATEL.NS', 'LGBBROSLTD.NS', 'VARDHACRLC.NS', 'TRENT.NS', 'HINDNATGLS.NS', 'ATULAUTO.NS', 'NOCIL.NS', 'L&TFH.NS', 'DLF.NS', 'BDL.NS', 'DELTACORP.NS', 'CEATLTD.NS', 'EICHERMOT.NS', 'GSFC.NS', 'BPCL.NS', 'ARVINDFASN.NS', 'APARINDS.NS', 'KAJARIACER.NS', 'MANGCHEFER.NS', 'ELGIEQUIP.NS', 'RGL.NS', 'TTKPRESTIG.NS', 'AMARAJABAT.NS', 'JSL.NS', 'DYNAMATECH.NS', 'BEL.NS', 'TNPL.NS', 'SHREECEM.NS', 'BAJAJCON.NS', 'CROMPTON.NS', 'SARDAEN.NS', 'LIBERTSHOE.NS', 'KOLTEPATIL.NS', 'DHAMPURSUG.NS', 'CANFINHOME.NS', 'IDEA.NS', 'HINDCOMPOS.NS', 'TEXRAIL.NS', 'HITECHGEAR.NS', 'MAHINDCIE.NS', 'UNICHEMLAB.NS', 'EVERESTIND.NS', 'ADANIENT.NS', 'VAKRANGEE.NS', 'RUPA.NS', 'PFOCUS.NS', 'HSCL.NS', 'RSYSTEMS.NS', 'GABRIEL.NS', 'LAKSHVILAS.NS', 'SOLARINDS.NS', 'UFO.NS', 'LUXIND.NS', 'KNRCON.NS', 'BLISSGVS.NS', 'AARTIDRUGS.NS', 'JTEKTINDIA.NS', 'HSIL.NS', 'UNIVCABLES.NS', 'BRNL.NS', 'KITEX.NS', 'MINDAIND.NS', 'GILLETTE.NS', 'RUBYMILLS.NS', 'GUJALKALI.NS', 'MUTHOOTCAP.NS', 'BHARATFORG.NS', 'JYOTHYLAB.NS', 'METROPOLIS.NS', 'HONDAPOWER.NS', 'FDC.NS', 'PENIND.NS', 'BEML.NS', 'PHILIPCARB.NS', 'CIGNITITEC.NS', 'PGIL.NS', 'TV18BRDCST.NS', 'DPSCLTD.NS', 'INSECTICID.NS', 'BAJFINANCE.NS', 'SADBHIN.NS', 'IFGLEXPOR.NS', 'AVTNPL.NS', 'PCJEWELLER.NS', 'ECLERX.NS', 'SUZLON.NS', 'ESABINDIA.NS', 'SPARC.NS', 'AEGISCHEM.NS', 'KIRLOSBROS.NS', 'LTTS.NS', 'SCHAEFFLER.NS', 'CONCOR.NS', 'SCI.NS', 'BOMDYEING.NS', 'PRESTIGE.NS', 'GDL.NS', 'ASHAPURMIN.NS', 'CONFIPET.NS', 'EXPLEOSOL.NS', 'TVSMOTOR.NS', 'IOC.NS', 'ATUL.NS', 'MINDACORP.NS', 'HINDOILEXP.NS', 'BIOCON.NS', 'PARAGMILK.NS', 'VADILALIND.NS', 'ERIS.NS', 'PRSMJOHNSN.NS', 'ELECTCAST.NS', 'UNITECH.NS', 'RIIL.NS', 'SATIA.NS', 'PTL.NS', 'WONDERLA.NS', 'CREST.NS', 'BLS.NS', 'MARICO.NS', 'NFL.NS', 'RSWM.NS', 'FEDERALBNK.NS', 'ABB.NS', 'DAAWAT.NS', 'ALANKIT.NS', 'SADBHAV.NS', 'IIFLSEC.NS', 'RELIANCE.NS', 'VAIBHAVGBL.NS', 'DATAMATICS.NS', 'MSTCLTD.NS', 'TECHNOE.NS', 'CLNINDIA.NS', 'VTL.NS', 'DEN.NS', 'JINDALSAW.NS', 'DIAMONDYD.NS', 'SBIN.NS', 'ABFRL.NS', 'JSLHISAR.NS', 'BHARATRAS.NS', 'PTC.NS', 'CANTABIL.NS', 'JETAIRWAYS.NS', 'GPIL.NS', 'JUSTDIAL.NS', 'LINCOLN.NS', 'EXCELINDUS.NS', 'GFLLIMITED.NS', 'JPASSOCIAT.NS', 'EIFFL.NS', 'AAVAS.NS', 'BHAGERIA.NS', 'ASHOKA.NS', 'BOSCHLTD.NS', 'GOLDIAM.NS', 'ASIANTILES.NS', 'HEG.NS', 'IBREALEST.NS', 'GEOJITFSL.NS', 'NAVKARCORP.NS', 'RPGLIFE.NS', 'SHAKTIPUMP.NS', 'RKFORGE.NS', 'PGHL.NS', 'YESBANK.NS', 'GREENLAM.NS', 'FSC.NS', 'OAL.NS', 'ASTEC.NS', 'SANGHVIMOV.NS', 'EIHOTEL.NS', 'DEEPAKFERT.NS', 'JMCPROJECT.NS', 'DHFL.NS', 'FCL.NS', 'MFSL.NS', 'CERA.NS', 'JKLAKSHMI.NS', 'SAGCEM.NS', 'BRITANNIA.NS', 'BANARISUG.NS', 'VOLTAS.NS', 'PLASTIBLEN.NS', 'GET&D.NS', 'SHREEPUSHK.NS', 'BASF.NS', 'MAHSEAMLES.NS', 'NIACL.NS', 'HGS.NS', 'SUTLEJTEX.NS', 'MANAKSIA.NS', 'ENIL.NS', 'TATAPOWER.NS', 'VSSL.NS', 'KALPATPOWR.NS', 'INOXWIND.NS', 'BAJAJFINSV.NS', 'IMPAL.NS', 'CGPOWER.NS', 'IDFCFIRSTB.NS', 'AMBUJACEM.NS', 'SUNTECK.NS', 'WELSPUNIND.NS', 'SUVENPHAR.NS', 'TEJASNET.NS', 'NITINSPIN.NS', 'BCG.NS', 'MTNL.NS', 'SUMMITSEC.NS', 'SANGAMIND.NS', 'APLAPOLLO.NS', 'NAVNETEDUL.NS', 'POLYMED.NS', 'STARCEMENT.NS', 'PUNJABCHEM.NS', 'IFCI.NS', 'ICICIGI.NS', 'HUDCO.NS', 'SASKEN.NS', 'REPCOHOME.NS', 'DHANBANK.NS', 'SUNPHARMA.NS', 'GUJGASLTD.NS', 'RAMCOIND.NS', 'PANAMAPET.NS', 'NLCINDIA.NS', 'HTMEDIA.NS', 'GULFPETRO.NS', 'HDFC.NS', 'KARURVYSYA.NS', 'TI.NS', 'ALBERTDAVD.NS', 'GSKCONS.NS', 'OIL.NS', 'SHILPAMED.NS', 'AMBER.NS', 'FACT.NS', 'STERTOOLS.NS', 'AUBANK.NS', 'MRF.NS', 'BODALCHEM.NS', 'ORIENTPPR.NS', 'AVADHSUGAR.NS', 'DLINKINDIA.NS', '3IINFOTECH.NS', 'ACC.NS', 'BGRENERGY.NS', 'RVNL.NS', 'ARSHIYA.NS', 'DIXON.NS', '63MOONS.NS', 'GAEL.NS', 'APOLLOTYRE.NS', 'GNFC.NS', 'ZEEL.NS', 'VINATIORGA.NS', 'BIRLACORPN.NS', 'HEXAWARE.NS', 'KARDA.NS', 'AUROPHARMA.NS', 'AMRUTANJAN.NS', 'ULTRACEMCO.NS', 'UJJIVAN.NS', 'MINDTREE.NS', 'TATAMOTORS.NS', 'FORTIS.NS', 'SUNTV.NS', 'INDIANHUME.NS', 'WABAG.NS', 'GRAVITA.NS', 'ESTER.NS', 'TAJGVK.NS', 'ICIL.NS', 'LALPATHLAB.NS', 'GATI.NS', 'HIRECT.NS', 'ARTEMISMED.NS', 'ASTERDM.NS', 'RAIN.NS', 'SBILIFE.NS', 'SPAL.NS', 'MARUTI.NS', 'HATHWAY.NS', 'ADANIPOWER.NS', 'GREENPANEL.NS', 'JSWHL.NS', 'BFINVEST.NS', 'TDPOWERSYS.NS', 'MENONBE.NS', 'MAHESHWARI.NS', 'DALBHARAT.NS', 'TATASTEEL.NS', 'TNPETRO.NS', 'GAYAPROJ.NS', 'KEC.NS', 'SMSPHARMA.NS', 'TCIEXP.NS', 'PIDILITIND.NS', 'GMMPFAUDLR.NS', 'PSPPROJECT.NS', 'ICICIBANK.NS', 'ANANTRAJ.NS', 'RITES.NS', 'BALAMINES.NS', 'WELENT.NS', 'MAHABANK.NS', 'ICICIPRULI.NS', 'HIMATSEIDE.NS', 'SRIPIPES.NS', 'ELECON.NS', 'STAR.NS', 'IRCON.NS', 'OBEROIRLTY.NS', 'KANSAINER.NS', 'GALLISPAT.NS', 'HLVLTD.NS', 'AXISBANK.NS', 'M&M.NS', 'MARKSANS.NS', 'ADVANIHOTR.NS', 'VIPIND.NS', 'HDFCAMC.NS', 'VSTIND.NS', 'INDOSTAR.NS', 'AIAENG.NS', 'SUVEN.NS', 'SIYSIL.NS', 'TANLA.NS', 'TWL.NS', 'MUNJALAU.NS', 'GMDCLTD.NS', 'IOLCP.NS', 'HDFCLIFE.NS', 'IEX.NS', 'GODREJCP.NS', 'MASFIN.NS', 'INFY.NS', 'IIFL.NS', 'LUMAXTECH.NS', 'TORNTPHARM.NS', 'VBL.NS', 'GSPL.NS', 'RADIOCITY.NS', 'SAFARI.NS', 'BBTC.NS', 'BAJAJHIND.NS', 'UJJIVANSFB.NS', 'ALLSEC.NS', 'TEAMLEASE.NS', 'IFBIND.NS', 'ONMOBILE.NS', 'GRASIM.NS', '5PAISA.NS', 'RENUKA.NS', 'INEOSSTYRO.NS', 'AARTIIND.NS', 'NEOGEN.NS', 'INDIGO.NS', 'CASTROLIND.NS', 'CAMLINFINE.NS', 'SPANDANA.NS', 'HARITASEAT.NS', 'ENDURANCE.NS', 'CHAMBLFERT.NS', 'NBCC.NS', 'THEJO.NS', 'GALLANTT.NS', 'CONTROLPR.NS', 'SANDHAR.NS', 'SESHAPAPER.NS', 'INDIAMART.NS', 'MIDHANI.NS', 'WELCORP.NS', 'MUKANDLTD.NS', 'NH.NS', 'FOSECOIND.NS', 'CRISIL.NS', 'LUPIN.NS', 'ONGC.NS', 'LAOPALA.NS', 'SHK.NS', 'LUMAXIND.NS', 'AVANTIFEED.NS', 'J&KBANK.NS', 'CAPACITE.NS', 'LINCPEN.NS', 'ARVSMART.NS', 'APOLLOHOSP.NS', 'IPCALAB.NS', 'NEWGEN.NS', 'JKPAPER.NS', 'GICRE.NS', 'SJVN.NS', 'CARERATING.NS', 'NUCLEUS.NS', 'RAMANEWS.NS', 'KOTAKBANK.NS', 'KTKBANK.NS', 'UBL.NS', 'CUB.NS', 'CIPLA.NS', 'TATASTLBSL.NS', 'SHANKARA.NS', 'BUTTERFLY.NS', 'CUMMINSIND.NS', 'JSWENERGY.NS', 'OMAXE.NS', 'DBCORP.NS', 'PILANIINVS.NS', 'WHIRLPOOL.NS', 'ASALCBR.NS', 'ACE.NS', 'ABCAPITAL.NS', 'PEL.NS', 'APCOTEXIND.NS', 'ORISSAMINE.NS', 'BANKINDIA.NS', 'FMGOETZE.NS', 'DISHTV.NS', 'WIPRO.NS', 'AKZOINDIA.NS', 'TIMKEN.NS', 'RADICO.NS', 'BALMLAWRIE.NS', 'JINDALPOLY.NS', 'CHOLAFIN.NS', 'SANOFI.NS', 'BANCOINDIA.NS', 'TATAELXSI.NS', 'BALKRISIND.NS', 'THANGAMAYL.NS', 'NSIL.NS', 'TAKE.NS', 'CADILAHC.NS', 'ADVENZYMES.NS', 'AGCNET.NS', 'IGPL.NS', 'ICRA.NS', 'CHOLAHLDNG.NS', 'PNBHOUSING.NS', 'MAGMA.NS', 'NELCO.NS', 'MBAPL.NS', 'CHENNPETRO.NS', 'GLAXO.NS', 'TIDEWATER.NS', 'DOLLAR.NS', 'DABUR.NS', 'MUNJALSHOW.NS', 'COALINDIA.NS', 'ZENTEC.NS', 'CANBK.NS', 'APCL.NS', 'TTML.NS', 'CEREBRAINT.NS', 'NACLIND.NS', 'TCNSBRANDS.NS', 'SEAMECLTD.NS', 'LAXMIMACH.NS', 'TCPLPACK.NS', 'GOCLCORP.NS', 'COSMOFILMS.NS', 'GLENMARK.NS', 'XCHANGING.NS', 'MARATHON.NS', 'JKTYRE.NS', 'KCP.NS', 'MAXVIL.NS', 'KIOCL.NS', 'HONAUT.NS', 'MANGLMCEM.NS', 'INDRAMEDCO.NS', 'GTLINFRA.NS', 'GIRRESORTS.NS', 'NATCOPHARM.NS', 'IBULHSGFIN.NS', 'VISHWARAJ.NS', 'MRPL.NS', 'NIITLTD.NS', 'AHLUCONT.NS', 'POKARNA.NS', 'SCHNEIDER.NS', 'ZEELEARN.NS', 'SHALBY.NS', 'TORNTPOWER.NS', 'SASTASUNDR.NS', 'RATNAMANI.NS', 'KKCL.NS', 'SWANENERGY.NS', 'CDSL.NS', 'POWERMECH.NS', 'RECLTD.NS', 'PDSMFL.NS', 'BALRAMCHIN.NS', 'SKIPPER.NS', 'MANAPPURAM.NS', 'WOCKPHARMA.NS', 'GANDHITUBE.NS', 'HFCL.NS', 'JCHAC.NS', 'RCF.NS', 'GUFICBIO.NS', 'GPPL.NS', 'MARINE.NS', 'PNCINFRA.NS', 'ORICONENT.NS', 'VSTTILLERS.NS', 'CAREERP.NS', 'JKIL.NS', 'ANDHRAPAP.NS', 'SUNDARMFIN.NS', 'SANDESH.NS', 'SUPREMEIND.NS', 'PHOENIXLTD.NS', 'BANKBARODA.NS', 'SUNDRMFAST.NS', 'PSB.NS', '3RDROCK.NS', 'IIFLWAM.NS', 'SUDARSCHEM.NS', 'INOXLEISUR.NS', 'HIL.NS', 'APLLTD.NS', 'THYROCARE.NS', 'GRANULES.NS', 'DMART.NS', 'SIEMENS.NS', 'ISEC.NS', 'ZENSARTECH.NS', 'INGERRAND.NS', 'UCALFUEL.NS', 'RBLBANK.NS', 'SOUTHBANK.NS', 'HESTERBIO.NS', 'SNOWMAN.NS', 'HAL.NS', 'RESPONIND.NS', 'CENTRUM.NS', 'SONATSOFTW.NS', 'EXIDEIND.NS', 'PATELENG.NS', 'FCONSUMER.NS', 'IRCTC.NS', 'MOREPENLAB.NS', 'HINDUNILVR.NS', 'SOTL.NS', 'NBVENTURES.NS', 'JINDALSTEL.NS', 'FEL.NS', 'HMVL.NS', 'SREINFRA.NS', 'VARROC.NS', 'ACCELYA.NS', 'KPRMILL.NS', 'BANDHANBNK.NS', 'SUMICHEM.NS', 'GODREJIND.NS', 'MOTILALOFS.NS', 'DVL.NS', 'ADFFOODS.NS', 'CSBBANK.NS', 'MHRIL.NS', 'JAIBALAJI.NS', 'IRB.NS', 'HINDPETRO.NS', 'RELIGARE.NS', 'CREDITACC.NS', 'EVEREADY.NS', 'SHALPAINTS.NS', 'KESORAMIND.NS', 'SHANTIGEAR.NS', 'INFIBEAM.NS', 'MUTHOOTFIN.NS', 'SATIN.NS', 'SURYAROSNI.NS', 'BAJAJELEC.NS', 'MANALIPETC.NS', 'TASTYBITE.NS', 'SIS.NS', 'SFL.NS', 'CARBORUNIV.NS', 'ORIENTHOT.NS', 'HERITGFOOD.NS', 'RAJESHEXPO.NS', 'UCOBANK.NS', 'GULFOILLUB.NS', 'THERMAX.NS', 'IGL.NS', 'FINEORG.NS', 'RAYMOND.NS', 'ALLCARGO.NS', 'GODREJPROP.NS', 'GODFRYPHLP.NS', 'GUJAPOLLO.NS', 'VEDL.NS', 'GOKEX.NS', 'ITI.NS', 'PRINCEPIPE.NS', 'TIMETECHNO.NS', 'RML.NS', 'NCLIND.NS', 'SIRCA.NS', 'RPOWER.NS', 'PFIZER.NS', 'INDIANB.NS', 'MOLDTKPAC.NS', 'SPENCERS.NS', 'HCC.NS', 'FLUOROCHEM.NS', 'BBL.NS', 'MMTC.NS', 'GICHSGFIN.NS', 'NECLIFE.NS', 'SYNGENE.NS', 'CUPID.NS', 'CCL.NS', 'WENDT.NS', 'SHARDACROP.NS', 'HBLPOWER.NS', 'TTKHLTCARE.NS', 'MAHEPC.NS', 'KAYA.NS', 'PNB.NS', 'FINPIPE.NS', 'THOMASCOOK.NS', 'ARVIND.NS', 'PVR.NS', 'TATACHEM.NS', 'BALAJITELE.NS', 'VHL.NS', 'MONTECARLO.NS', 'JISLJALEQS.NS', 'DHANUKA.NS', 'GENUSPOWER.NS', 'GARFIBRES.NS', 'SAREGAMA.NS', 'SUPPETRO.NS', 'ALKYLAMINE.NS', 'PIIND.NS', 'TATACONSUM.NS', 'ESCORTS.NS', 'LEMONTREE.NS', 'ORIENTCEM.NS', 'TINPLATE.NS', 'ASAHIINDIA.NS', 'NAM-INDIA.NS', 'UTTAMSUGAR.NS', 'AHLEAST.NS', 'IFBAGRO.NS', 'JKCEMENT.NS', 'ADANIGREEN.NS', 'IMFA.NS', 'KCPSUGIND.NS', 'MIRZAINT.NS', 'USHAMART.NS', 'RICOAUTO.NS', 'LICHSGFIN.NS', 'RCOM.NS', 'JAGRAN.NS', 'AUTOAXLES.NS', 'KIRLOSIND.NS', 'ORIENTREF.NS', 'SWSOLAR.NS', 'PFC.NS', 'EDELWEISS.NS', 'JAMNAAUTO.NS', 'JPPOWER.NS', 'ORIENTELEC.NS', 'AJMERA.NS', 'GRAPHITE.NS', 'STCINDIA.NS', 'ASIANPAINT.NS', 'HEROMOTOCO.NS', 'TRITURBINE.NS', 'VRLLOG.NS', 'MAHLIFE.NS', 'LT.NS', 'MADRASFERT.NS', 'AJANTPHARM.NS', 'SEQUENT.NS', 'MGL.NS', 'NELCAST.NS', 'VISAKAIND.NS', 'PURVA.NS', 'CHEMBOND.NS', 'GESHIP.NS', 'DCMSHRIRAM.NS', 'SSWL.NS', 'DCAL.NS', 'FILATEX.NS', 'UFLEX.NS', 'SHIL.NS', 'OFSS.NS', 'MASTEK.NS', 'PANACEABIO.NS', 'SREEL.NS', 'SRTRANSFIN.NS', 'MMFL.NS', 'JUBLFOOD.NS', 'SHOPERSTOP.NS', 'COROMANDEL.NS', 'APOLLOPIPE.NS', 'ZEEMEDIA.NS', 'INDNIPPON.NS', 'M&MFIN.NS', 'PAGEIND.NS', 'RAJTV.NS', 'NEULANDLAB.NS', 'SUNDARMHLD.NS', 'PERSISTENT.NS', 'TIINDIA.NS', 'PRICOLLTD.NS', 'LINDEINDIA.NS', 'ORBTEXP.NS', 'ITC.NS', 'APTECHT.NS', 'VOLTAMP.NS', 'BSOFT.NS', 'MOTHERSUMI.NS', 'NXTDIGITAL.NS', 'GIPCL.NS', 'THEMISMED.NS', 'INFOBEAN.NS', 'INDHOTEL.NS', 'ASHIANA.NS', 'RELINFRA.NS', 'BLUEDART.NS', 'GTPL.NS', 'IDBI.NS', 'MATRIMONY.NS', 'SHREDIGCEM.NS', 'PPAP.NS', 'GNA.NS', 'MCDOWELL-N.NS', 'BERGEPAINT.NS', 'TIIL.NS', 'SUNFLAG.NS', 'ZODIACLOTH.NS', 'CYIENT.NS', 'PRECWIRE.NS', 'TFCILTD.NS', 'RAMKY.NS', '3MINDIA.NS', 'HCLTECH.NS', 'HIKAL.NS', 'TATACOFFEE.NS', 'SKFINDIA.NS', 'IDFC.NS', 'GREENPLY.NS', 'AFFLE.NS', 'PRECAM.NS', 'TECHM.NS', 'MOIL.NS', 'GAIL.NS', 'TRIDENT.NS', 'INDORAMA.NS', 'HINDZINC.NS', 'NCC.NS', 'HERCULES.NS', 'REDINGTON.NS', 'DBL.NS', 'TEXINFRA.NS', 'V2RETAIL.NS', 'EBIXFOREX.NS', 'DALMIASUG.NS', 'ANDHRSUGAR.NS', 'MANINDS.NS', 'BAJAJHLDNG.NS', 'MAHLOG.NS', 'CESC.NS']

    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--update':
            update_data = True
    else:
        update_data = False
    
    begin = time.time()
    backtest1 = Backtester(
        list_stock = list_stok, 
        initial_capital = 1000000, 
        base_lookback = 5,
        multiplier1 = 1.5, 
        multiplier2 = 2, 
        lin_reg_filter_multiplier = 0.5, 
        stop_loss_percent = 0.05, 
        filter_percentile = 70, 
        filter_activation_flag = True, 
        long_only_flag = False, 
        training_period = 20, 
        current_account_size_csv = 'Intraday1Test', 
        update_data=update_data, 
        percentRisk_PerTrade=0.2
        )
    backtest1.run()
    end = time.time()
    print(f'Time taken for the backtest: {end - begin}')

if __name__ == '__main__':
    main()
