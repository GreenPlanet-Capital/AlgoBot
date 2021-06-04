<<<<<<< HEAD
=======
import pandas as pd

a = pd.DataFrame(columns = ['a','b'])
a.loc['AAPL'] = ['1','b']
a.loc['MSFT'] = ['a','b']
a.loc['XLXX'] = ['a','b']

a.loc['AAPL','a'] = 3
print(a)
>>>>>>> 946797fce87afd8099f14ade2fdca754c23539d0
