from OptimisedIndicatorClasses.BollingerSMA import BollingerSMA
from OptimisedIndicatorClasses.BollingerWMA import BollingerWMA
from OptimisedIndicatorClasses.BollingerMcG import BollingerMcG
from OptimisedIndicatorClasses.EnvelopeMcG import EnvelopeMcG
from OptimisedIndicatorClasses.EnvelopeSMA import EnvelopeSMA
import yfinance as yf
import numpy as np

extract_obj = yf.Ticker("AAPL")
data = extract_obj.history(period="1y")
data['Typical Price'] = ((data['High'] + data['Low'] + data['Close']) / 3).round(2)
data = data.iloc[-50:]
price_list = np.array(data['Typical Price'])

indic_obj = EnvelopeSMA(price_list, 5, 0.02)
x = indic_obj.run()
print(x)
indic_obj.graphing()