from OptimisedIndicatorClasses.BollingerSMA import BollingerSMA
from OptimisedIndicatorClasses.BollingerWMA import BollingerWMA
from OptimisedIndicatorClasses.BollingerMcG import BollingerMcG
from OptimisedIndicatorClasses.EnvelopeMcG import EnvelopeMcG
from OptimisedIndicatorClasses.EnvelopeSMA import EnvelopeSMA
from OptimisedIndicatorClasses.EnvelopeWMA import EnvelopeWMA
from OptimisedIndicatorClasses.SMA_SMA_Osc import SMA_SMA_Osc
from OptimisedIndicatorClasses.WMA_SMA_Osc import WMA_SMA_Osc
from OptimisedIndicatorClasses.WMA_WMA_Osc import WMA_WMA_Osc
from OptimisedIndicatorClasses.WMA_McG_Osc import WMA_McG_Osc
from OptimisedIndicatorClasses.SMA_McG_Osc import SMA_McG_Osc
from OptimisedIndicatorClasses.DM_DM_Osc import DM_DM_Osc
from OptimisedIndicatorClasses.Lin_Reg import Lin_Reg
import yfinance as yf
import numpy as np

extract_obj = yf.Ticker("AIZ")
data = extract_obj.history(period="1y")
data['Typical Price'] = ((data['High'] + data['Low'] + data['Close']) / 3).round(2)
data = data.iloc[-50:]
price_list = np.array(data['Typical Price'])

indic_obj = BollingerMcG(price_list,8, 1.2)
x = indic_obj.run()
print(x)
indic_obj.graphing()